# A2
# Tested on
Host1: ubuntu1804-008.student.cs.uwaterloo.ca
python3 nEmulator.py 9941 ubuntu1804-002.student.cs.uwaterloo.ca 9944 9943 ubuntu1804-004.student.cs.uwaterloo.ca 9942 0.2 1
# 
Host2: ubuntu1804-002.student.cs.uwaterloo.ca
python3 receiver.py ubuntu1804-008.student.cs.uwaterloo.ca 9943 9944 result.txt
# 
Host3: ubuntu1804-004.student.cs.uwaterloo.ca
python3 sender.py ubuntu1804-008.student.cs.uwaterloo.ca 9941 9942 50 number.txt
