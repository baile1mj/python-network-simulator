# Represents a UDP datagram of a given size
class UdpDatagram(object):
    id = -1
    size = 0
    senderDepart = 0
    routerArrive = 0.0
    routerDepart = 0.0
    gatewayArrive = 0.0
    gatewayDepart = 0.0
    receiverArrive = 0.0
    delay = 0.0
    errors = 0
    routerDropped = False

    def __init__(self, id, size):
        self.id = id
        self.size = size

    def __str__(self):
        return "id: {0}, size: {1}, host dep: {2}, router arr: {3}, router dep: {4}, receiver arr: {5}" \
            .format(self.id, self.size, self.senderDepart, self.routerArrive, self.routerDepart,  self.receiverArrive)