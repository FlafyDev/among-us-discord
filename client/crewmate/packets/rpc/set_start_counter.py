from scapy.packet import Packet


class SetStartCounterRPC(Packet):
    name = "SetStartCounterRPC"
    fields_desc = [
    ]

    def extract_padding(self, p):
        return "", p
