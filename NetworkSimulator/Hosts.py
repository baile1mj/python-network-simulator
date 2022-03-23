import random
from UdpDatagram import UdpDatagram

# Generates data to sent.
class Sender(object):
    packets = None

    def GeneratePackets(self, number, minSize, maxSize):
        self.packets = list()

        for count in range(number):
            size = random.randint(minSize, maxSize)
            self.packets.append(UdpDatagram(count + 1, size))

        return self.packets

    def GetPacketCount(self):
        return len(self.packets)

# Builds statistics on transmitted packets.
class Receiver(object):
    received = None
    errorPackets = 0
    totalErrors = 0
    misorderedPacket = 0

    # Receives packets in order of arrival time.
    def ReceivePackets(self, packets):
        self.received = list()

        # Count errors.
        for packet in packets:
            self.received.append(packet)

            if packet.errors > 0:
                self.errorPackets += 1
                self.totalErrors += packet.errors

        return self.received

    def GetPacketCount(self):
        return len(self.received)