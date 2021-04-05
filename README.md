# A2
Since this is all in python, no make file is needed.
The packet is Format is respected by the constructor function. However there is no way to set type to a in python that I know of. 
# Tested on and built on
Make sure to include the packet.py in the same folder as nEmulator.py, sender.py and receiver.py! otherwise the programs fails


Host1: ubuntu1804-008.student.cs.uwaterloo.ca
python3 nEmulator.py 9941 ubuntu1804-002.student.cs.uwaterloo.ca 9944 9943 ubuntu1804-004.student.cs.uwaterloo.ca 9942 0.2 1


Host2: ubuntu1804-002.student.cs.uwaterloo.ca
python3 receiver.py ubuntu1804-008.student.cs.uwaterloo.ca 9943 9944 result.txt


Host3: ubuntu1804-004.student.cs.uwaterloo.ca
python3 sender.py ubuntu1804-008.student.cs.uwaterloo.ca 9941 9942 50 number.txt

#How to Run the files
# 
nEmulator: python3 nEmulator.py <emulator's receiving UDP port number in the forward (sender) direction> <receiver’s network address> <receiver’s receiving UDP port number> <emulator's receiving UDP port number in the backward (receiver) direction> <sender’s network address> <sender’s receiving UDP port number> <packet discard probability (decimal eg. 0.50 for 50% packet drop)> <verbose-mode>
# 
Receiver: python3 receiver.py <hostname for the network emulator> <DP port number used by the link emulator to receive ACKs from the receiver> <UDP port number used by the receiver  to  receive  data  from  the  emulator> <name of the file into which the received data is written>
# 
sender: python3 sender.py <host  address  of  the  network  emulator> <UDP  port  number  used  by  the  emulator  to receive data from the sender> <UDP port number used by the sender to receive ACKs from the emulator> <timeout interval in units of millisecond> <name of the file to be transferred>
