from packet import *
import sys
import time
import socket

def main(argv):
    if (len(argv) != 4):
        return "Does not have 4 arguments"
    emulator_addr = argv[0]
    emulator_port = int(argv[1])
    emulator_pair = (emulator_addr, emulator_port)
    receiver_port = int(argv[2])
    file_name = open(argv[3], "w+")
    arrival_log = open("arrival.log", "w+")
    #keeps all the data of packet seqnum at the index seqnum, "" for packets data that was not recevied
    packets = []
    #keep all the acked number 0 is not acked, 1 is acked
    acked = []
    for i in range(0, 30):
        packets[i] = ""
        acked[i] = 0
    
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiverSocket.bind(("", receiver_port))
    while True:
        try:
            info, addr = receiverSocket.recvfrom(1024)
        except:
            return "Something went wrong with receiving the packets"
        #pasrse the packet
        package = Packet.parseUDPdata(info)
        #get the packet info
        packet_data = str(package.getData())
        packet_seqnum = int(package.getSeqnum())
        packet_type = int(package.getType())
        #write the packet seqnum into the arrival log
        arrival_log.write(str(packet_seqnum) + "\n")
        #when receive the EOT from sender
        if (packet_type == 2):
            #set up EOT Packet and ready it for UDP transfer
            eot = pickle.dumps(Packet.createEOT(seqnum=packet_seqnum))
            #send the eot packet to the emulator
            receiverSocket.sendto(eot, emulator_pair)
            #end the loop since no more UDP to receive
            break
        #Data case
        elif (packet_type == 1):
            #packet data was not received before
            if (acked[packet_seqnum] == 0):
                #store the string data in index seqnum (buffer and put them into order)
                packets[packet_seqnum] = packet_data
                #ack the packet in index seqnum in list acked
                acked[packet_seqnum] = 1
            #packets was ack but got lost
            else:
                #create ack message
                ack_message = pickle.dumps(Packet.createACK(packet_seqnum))
                #send ack message
                receiverSocket.sendto(ack_message, emulator_pair)

    #After exited the while (EOT Received)
    #write to the file
    #go through the entire list
    for data in packets:
        #write all the string in the file
        file_name.write(data)
    
    #close open file, log and socket
    file_name.close()
    arrival_log.close()
    receiverSocket.close()

if __name__ == "__main__":
    main(sys.argv)