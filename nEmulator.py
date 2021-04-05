from packet import *
import sys
import time
import socket
import random


def listen_to_sender(senderSocket, receiver_pair, pack_discard_probability, verbose_mode):
    try:
        # receive packet from sender
        sender_package, senderAddr = senderSocket.recvfrom(1024)
        # get info and type of packet
        info = Packet.parseUDPdata(sender_package)
        packet_type = info.getType()
        packet_seqnum = info.getSeqnum()
        # if the packet is EOT
        if (packet_type == 2):
            if (verbose_mode == 1):
                print("Receiving EOT From Sender with seqnum: " + str(packet_seqnum) + "\n")
            # send the packet
            senderSocket.sendto(sender_package, receiver_pair)
            if (verbose_mode == 1):
                print("Sending EOT To Receiver with seqnum: " + str(packet_seqnum) + "\n")
        # data packet
        elif (packet_type == 1):
            if (verbose_mode == 1):
                print("Received From Sender Packet, seqnum=" + str(packet_seqnum) + "\n")
            # randomly select to drop or send the packet, drop with prob discard_prob
            result = random.choices(population=["Drop", "Keep"], weights=[pack_discard_probability, (1 - pack_discard_probability)], k=1)
            # if the result was to keep
            if (result[0] == "Keep"):
                # send the packets to receiver
                senderSocket.sendto(sender_package, receiver_pair)
                if (verbose_mode == 1):
                    print("Sending Packet to Receiver, seqnum=" + str(packet_seqnum) + "\n")
            # drop the packet
            elif (result[0] == "Drop"):
                if (verbose_mode == 1):
                    print("Droped Packet from Sender, seqnum=" + str(packet_seqnum) + "\n")
    except socket.error:
        pass

def listen_to_receiver(receiverSocket, sender_pair, pack_discard_probability, verbose_mode):
    try:
        # receive packet from receiver
        receiver_package, receiverAddr = receiverSocket.recvfrom(1024)
        # get info and type of packet
        info = Packet.parseUDPdata(receiver_package)
        packet_type = info.getType()
        packet_seqnum = info.getSeqnum()
        # if the packet is EOT
        if (packet_type == 2):
            if (verbose_mode == 1):
                print("Receiving EOT From Receiver with seqnum " + str(packet_seqnum) + "\n")
            # send the packet
            receiverSocket.sendto(receiver_package, sender_pair)
            if (verbose_mode == 1):
                print("Sending EOT To Sender with seqnum: " + str(packet_seqnum) + "\n")
            return True
        # ack packet
        elif (packet_type == 0):
            if (verbose_mode == 1):
                print("Received From Sender ACK, seqnum=" + str(packet_seqnum) + "\n")
            # randomly select to drop or send the ACK, drop with prob discard_prob
            result = random.choices(population=["Drop", "Keep"], weights=[pack_discard_probability, (1 - pack_discard_probability)], k=1)
            # if the result was to keep
            if (result[0] == "Keep"):
                # send the packets to receiver
                receiverSocket.sendto(receiver_package, sender_pair)
                if (verbose_mode == 1):
                    print("Sending ACK to Sender, seqnum=" + str(packet_seqnum) + "\n")
            # if drop the ack
            elif (result[0] == "Drop"):
                if (verbose_mode == 1):
                    print("Droped ACK from Receiver, seqnum=" + str(packet_seqnum) + "\n")
            return False
    except socket.error:
        return False

def main(argv):
    emualtor_sender_udp_port = int(argv[1])
    receiver_addr = argv[2]
    receiver_port = int(argv[3])
    receiver_pair = (receiver_addr, receiver_port)
    emualtor_receiver_udp_port = int(argv[4])
    sender_addr = argv[5]
    sender_port = int(argv[6])
    sender_pair = (sender_addr, sender_port)
    pack_discard_probability = float(argv[7])
    verbose_mode = int(argv[8])
    # port to receive from the sender
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    senderSocket.bind(("", emualtor_sender_udp_port))
    senderSocket.setblocking(False)
    # port to receive from the receiver
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiverSocket.bind(("", emualtor_receiver_udp_port))
    receiverSocket.setblocking(False)

    last_eot_sent = False

    # start to listen:
    while True:
        #if the last EOT is sent by Receiver, we break
        if (last_eot_sent):
            break
        #listens to sender and receiver
        listen_to_sender(senderSocket=senderSocket, receiver_pair=receiver_pair, pack_discard_probability=pack_discard_probability, verbose_mode=verbose_mode)
        last_eot_sent = listen_to_receiver(receiverSocket=receiverSocket, sender_pair=sender_pair, pack_discard_probability=pack_discard_probability, verbose_mode=verbose_mode)

    #close sockets
    senderSocket.close()
    receiverSocket.close()

if __name__ == "__main__":
    main(sys.argv)
