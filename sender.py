from packet import *
import sys
import time
import socket

def main(argv):
    #if less or more argument than 5 is inputed, return the program
    if (len(argv) != 5):
        return "Incorrect Number of Arguments"
    #setting up the arguments
    emulator_host_addr = argv[0]
    emulator_receive_port = int(argv[1])
    sender_receive_port = int(argv[2])
    emulator_pair = (emulator_host_addr, emulator_receive_port)
    timeout = int(argv[3])
    #open all files and logs
    file_name = open(argv[4], "w+")
    seqnum_log = open("seqnum.log", "w+")
    ack_log = open("ack.log", "w+")
    #Create UDP sender to send packets to emulator
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #open listen port
    senderSocket.bind(("", sender_receive_port))
    #put socket on non-blocking mode
    senderSocket.setblocking(0)
    #if timer is currently running
    timer_on = False
    #is EOT pack is ready (see if it's final ACK)
    eot_ready = False
    #Placeholder for EOT Packet in pickle.dump form
    eot = ""
    #max window package size
    window_max = 30
    #windows oldest send package unacked seqnum
    base = 0
    #next package to be sent
    nextseqnum = 0
    #create index of packets
    packets_range = []
    #keep all the acked number 0 is not acked, 1 is acked
    acked = []
    #creating a list of 30 Placeholder index to be replaced by sent Packets after pickled
    for i in range(0, 30):
        packets_range.append(i)
        #setting all the package to non-acked
        acked[i] = 0
    while True:
        #if all all package is sent and acked
        if (eot_ready and (base == nextseqnum)):
            senderSocket.sendto(eot, emulator_pair)
            seqnum_log.write(str(nextseqnum) + "\n")
            break
        try:
            #check for ack recevive
            ack, addr = senderSocket.recvfrom(1024)
            #unparsing Packet Object
            info = Packet.parseUDPdata(ack)
            #getting all the parameters
            packet_seqnum = int(info.getSeqnum())
            #log it
            ack_log.write(str(packet_seqnum) + "\n")
            acked[int(packet_seqnum)] = 1
            #find the lowest non acked packet seqnum as base
            if (base == packet_seqnum):
                original_base = base
                index = 0
                while (index < 30):
                    if (acked[index] == 0):
                        base = index
                        break
                    index = index + 1
                #if all are acked, end it
                if (original_base == base):
                    base = nextseqnum

            #All Acked
            if (base == nextseqnum):
                #close timer
                timer_on = False
            else:
                #turn on timer
                timer = time.time()
                timer_on = True
            continue
        #socket error pass
        except socket.error:
            pass
        #check if timed out
        if ((timer_on) and (time.time() - timer > timeout)):
            #restart timer
            timer = time.time()
            #temporary variable
            tempbase = base
            #retrasmit all the non-acked packets
            while (tempbase != nextseqnum):
                #if the packet is not acked
                if (acked[tempbase] == 0):
                    #send packet
                    senderSocket.sendto(packets_range[tempbase], emulator_pair)
                    #log seqnum sent
                    seqnum_log.write(str(tempbase) + "\n")
                    #increment to send next packet
                tempbase = tempbase + 1
        #check if the packet about to send is in the window
        elif (nextseqnum < base + window_max):
            #read max_length of characters from file
            send_data = file_name.read(max_length)
            #if no chacter to read, start EOT process
            if (len(send_data) == 0):
                #set eot
                eot = pickle.dumps(Packet.createEOT(nextseqnum))
                #set eot ready
                eot_ready = True
            else:
                #create the packet and process it for udp
                package = pickle.dumps(Packet.createPacket(seqnum=nextseqnum, data=send_data))
                #send the packet with nextsequm seqnum
                senderSocket.sendto(package, emulator_pair)
                #log the seqnum
                seqnum_log.write(str(nextseqnum) + "\n")
                #store the packet for retrasmite case
                packets_range[nextseqnum] = package
                #restart timer and to go to the next seqnum
                if (base == nextseqnum):
                    timer = time.time()
                    timer_on = True
                nextseqnum = nextseqnum + 1

    #All the Ack recevied besides the EOT
    #block the socket -  until receive the last EOT call back
    senderSocket.setblocking(1)
    #listen for udp
    eot, addr = senderSocket.recvfrom(1024)
    #Close all the Socket and file reads
    senderSocket.close()
    file_name.close()
    seqnum_log.close()
    ack_log.close()

if __name__ == "__main__":
    main(sys.argv)