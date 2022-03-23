import random

# Represents a transmission channel using the Gilbert-Elliot model.
class GilbertElliotChannel(object):
    goodState = None
    badState = None
    currentState = None

    def __init__(self, goodState, badState, pStartGood):
        self.goodState = goodState
        self.badState = badState

        # determine the starting state
        stateVal = random.random()

        if stateVal < 1 - pStartGood:
            self.currentState = self.goodState
        else:
            self.currentState = self.badState

    # Checks whether the current state should change.
    def CheckState(self):
        changeVal = random.random()
        if changeVal < self.currentState.probChange:
            self.ToggleState()

    # Toggles between good and bad states.
    def ToggleState(self):
        if self.currentState == self.goodState:
            self.currentState = self.badState
        else:
            self.currentState = self.goodState

    # Gets the probability of uncorrelated bit errors in the current state.
    def GetProbErrors(self):
        return self.currentState.probError

    # Gets the transmission speed in the current state.
    def GetChannelSpeed(self):
        return self.currentState.speed

    # Simulates transmission of packets through the wireless channel.
    def TransmitPackets(self, packets):
        transmitted = list()
        time = 0

        for packet in packets:
            transitTime = packet.size / self.GetChannelSpeed()
            packet.senderDepart = time

            # Check for random bit errors - loop needed because state may change any time.
            for bit in range(packet.size):
                self.CheckState()
                errorMetric = random.random()

                if errorMetric < self.GetProbErrors():
                    packet.payloadError = True
                    packet.errors += 1

            time += transitTime
            packet.routerArrive = time
            transmitted.append(packet)

        return transmitted

# Represents a channel state with some probability of packet loss and some probability of change to the next state.
class ChannelState(object):
    probError = 0
    probChange = 0
    speed = 0

    def __init__(self, pError, pChange, speed):
        self.probError = pError
        self.probChange = pChange
        self.speed = speed