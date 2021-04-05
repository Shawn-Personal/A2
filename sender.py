from packet import *
import sys
import time
import socket

def main(argv):
    #setting up the arguments
    emulator_host_addr = argv[1]
    emulator_receive_port = int(argv[2])
    sender_receive_port = int(argv[3])
    emulator_pair = (emulator_host_addr, emulator_receive_port)
    timeout = int(argv[4])
    timeout = float(timeout/1000)
    #open all files and logs
    file_name = open(argv[5], "r")
    seqnum_log = open("seqnum.log", "w+")
    ack_log = open("ack.log", "w+")
    #Create UDP sender to send packets to emulator
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #open listen port
    senderSocket.bind(("", sender_receive_port))
    #max window package size
    window_max = 30
    all_acked = False
    #windows oldest send package unacked seqnum
    base = 0
    #create index of packets
    packets = []
    #keep all the acked number 0 is not acked, 1 is acked
    acked = []
    #creating a list of n Placeholder index to be replaced by sent Packets after pickled
    data = file_name.read(max_length)
    index = 0
    #create all the packets and set all the acks to 0
    while (data):
        packets.append(pickle.dumps(Packet.createPacket(seqnum=index, data=data)))
        acked.append(0)
        index = index + 1
        data = file_name.read(max_length)
        print("finished setup packets")
    #read file done, close it
    file_name.close()
    #send all the acks
    counter = 0
    print("Before sending all packets")
    for send_data in packets:
        #check if the window is 
        if (counter <= window_max):
            #send all the packets
            senderSocket.sendto(send_data, emulator_pair)
            seqnum_log.write(str(counter) + "\n")
        counter = counter + 1
    print("After sending all packets")

    while True:
        print("In Loop")
        #if all packets are acked
        if (all_acked):
            print("In all Acked Case")
            #create and prepare EOT for send
            eot = pickle.dumps(Packet.createEOT(index))
            #send to emulator
            senderSocket.sendto(eot, emulator_pair)
            break
        try:
            print("In try case")
            #check for ack recevive
            senderSocket.settimeout(timeout)
            ack, addr = senderSocket.recvfrom(1024)
            #unparsing Packet Object
            info = Packet.parseUDPdata(ack)
            #getting all the parameters
            packet_seqnum = int(info.getSeqnum())
            #log it
            ack_log.write(str(packet_seqnum) + "\n")
            acked[packet_seqnum] = 1
            #find the lowest non acked packet seqnum as base
            if (base == packet_seqnum):
                #if all are acked, end it
                all_ack = True
                for pos in range(0, index):
                    if (acked[pos] == 0):
                        all_ack = False
                        base = pos
                        break
                if (all_ack):
                    base = index

            #All Acked
            if (base == index):
                all_acked = True
            print("After acked")
        #socket error pass
        except socket.error:
            print("In except case")
            tempbase = base
            #resend all packets
            while (tempbase != index):
                #check if the window size is enough
                if (window_max - base <= window_max):
                    #if the packet is not acked
                    if (acked[tempbase] == 0):
                        #send packet
                        senderSocket.sendto(packets[tempbase], emulator_pair)
                        #log seqnum sent
                        seqnum_log.write(str(tempbase) + "\n")
                tempbase = tempbase + 1
    
    #waiting for last ACK
    print("At the end")
    senderSocket.settimeout(None)
    eot, addr = senderSocket.recvfrom(1024)
    #close all sockets and files
    senderSocket.close()
    seqnum_log.close()
    ack_log.close()

if __name__ == "__main__":
    main(sys.argv)
