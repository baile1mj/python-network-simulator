import Channel
import Hosts
import Router

class Simulation(object):
    packetsPerRun = 0
    minPacketSize = 0
    maxPacketSize = 0
    sender = None
    receiver = None
    channel = None
    router = None

    def __init__(self, packets, minPacketSize, maxPacketSize, channel, router):
        self.packetsPerRun = packets
        self.minPacketSize = minPacketSize
        self.maxPacketSize = maxPacketSize
        self.channel = channel
        self.router = router
        self.sender = Hosts.Sender()
        self.receiver = Hosts.Receiver()

    def RunSimulation(self):
        packets = self.sender.GeneratePackets(self.packetsPerRun, self.minPacketSize, self.maxPacketSize)
        packets = self.channel.TransmitPackets(packets)
        packets = self.router.TransmitPackets(packets)
        packets = self.receiver.ReceivePackets(packets)

        # Build the statistics.
        stats = {
            "sent": self.sender.GetPacketCount(),
            "received": self.receiver.GetPacketCount(),
            "dropped": self.router.GetDroppedCount(),
            "misorderedCount": 0,
            "totalDelay": 0.0,
            "avgDelay": 0.0,
            "bitsSent": 0.0,
            "transitTime": 0.0,
            "avgTransitTime": 0.0,
            "idealTransitTime": 0.0,
            "avgIdealTransitTime": 0.0,
            "erroredPackets": self.receiver.errorPackets,
            "totalBitErrors": self.receiver.totalErrors
        }

        for i in range(0, len(packets)):
            thisPacket = packets[i]
            stats["totalDelay"] += thisPacket.delay
            stats["bitsSent"] += thisPacket.size
            stats["transitTime"] = thisPacket.receiverArrive - thisPacket.senderDepart
            stats["idealTransitTime"] = stats["transitTime"] - thisPacket.delay

            if thisPacket.errors > 0:
                stats["erroredPackets"] += 1
                stats["totalBitErrors"] += thisPacket.errors

            if i < len(packets) - 1:
                nextPacket = packets[i + 1]

                if thisPacket.id > nextPacket.id:
                    stats["misorderedCount"] += 1

        stats["avgDelay"] = stats["totalDelay"] / stats["received"]
        stats["avgTransitTime"] = stats["transitTime"] / stats["bitsSent"]
        stats["avgIdealTransitTime"] = stats["idealTransitTime"] / stats["bitsSent"]

        return stats

    @staticmethod
    def GetRouter(speed, bottleneck, probLoss, probDelay, minDelay, maxDelay):
        return Router.Router(speed, bottleneck, probLoss, probDelay, minDelay, maxDelay)

    @staticmethod
    def GetChannel(pGoodError, pRemainGood, goodSpeed, pBadError, pRemainBad, badSpeed, pStartGood):
        goodState = Channel.ChannelState(pGoodError, pRemainGood, goodSpeed)
        badState = Channel.ChannelState(pBadError, pRemainBad, badSpeed)
        return Channel.GilbertElliotChannel(goodState, badState, pStartGood)