import pickle

max_length = 500

class Packet:
    def __init__(self, type, seqnum, data):
        self.type = type
        self.seqnum = seqnum
        self.data = data
        self.length = len(data)
        try:
            if (self.length > max_length):
                raise NameError("Data string length > 500")
        except NameError:
            print("Error Occured")
            raise
    @staticmethod
    def createACK(seqnum):
        return Packet(type=0, seqnum=seqnum, data="")
    @staticmethod
    def createPacket(seqnum, data):
        return Packet(type=1, seqnum=seqnum, data=data)
    @staticmethod
    def createEOT(seqnum):
        return Packet(type=2, seqnum=seqnum, data="")

    def __repr__(self):
        return "type: " + str(self.type) + " seqnum: " + str(self.seqnum) + " length: " + str(self.length) + " data: " + str(self.data)

    def getType(self):
        return self.data

    def getSeqnum(self):
        return self.seqnum

    def getLength(self):
        return self.length
    
    def getData(self):
        return self.data

    @staticmethod
    def parseUDPdata(UDPdata):
        info = pickle.loads(UDPdata)
        return info