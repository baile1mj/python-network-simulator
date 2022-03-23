import random

# Represents a wired/wireless router.
class Router(object):
    speed = 0
    bottleneck = 0
    probLoss = None
    probDelay = 0
    maxDelay = 0
    dropped = None

    def __init__(self, speed, bottleneck, probLoss, probDelay, minDelay, maxDelay):
        self.speed = speed
        self.bottleneck = bottleneck
        self.probLoss = probLoss
        self.probDelay = probDelay
        self.minDelay = minDelay
        self.maxDelay = maxDelay
        self.dropped = list()

    # Simulates transmitting the packet via wired connection to the receiver.
    def TransmitPackets(self, packets):
        processed = list()
        lastDepart = 0

        while len(packets) > 0:
            packet = packets.pop(0)
            overflowMetric = random.random()

            # See if packet is dropped due to overflow.
            if overflowMetric < self.probLoss:
                self.dropped.append(packet)
            else:
                propagateTime = packet.size / self.speed
                delayMetric = random.random()

                # Add delay if necessary.
                if delayMetric < self.probDelay:
                    delay = (random.random() * (self.maxDelay - self.minDelay)) + self.minDelay
                    packet.delay += delay

                # Get optimistic depart time.
                depart = packet.routerArrive + propagateTime

                # If last packet is still being transmitted, this packet must wait.
                if depart < lastDepart:
                    packet.delay += lastDepart - depart
                    depart = lastDepart + propagateTime

                # Update departure times.
                packet.routerDepart = depart
                lastDepart = depart
                processed.append(packet)

                # Calculate arrival at receiver's gateway.
                packet.gatewayArrive = packet.routerDepart + packet.delay

        # Calculate last mile times.
        processed = sorted(processed, key=lambda p : p.gatewayArrive)
        lastDepart = 0

        for packet in processed:
            propagateTime = packet.size / self.bottleneck
            depart = packet.gatewayArrive + propagateTime

            if depart < lastDepart:
                depart = lastDepart + propagateTime

            packet.gatewayDepart = depart
            packet.receiverArrive = depart
            lastDepart = depart

        return processed

    def GetDroppedCount(self):
        return len(self.dropped)