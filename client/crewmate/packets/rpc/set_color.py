from scapy.fields import ByteField
from scapy.packet import Packet


class SetColorRPC(Packet):
    name = "SetColorRPC"
    fields_desc = [
        ByteField("colorId", None),
    ]

    def extract_padding(self, p):
        return "", p
