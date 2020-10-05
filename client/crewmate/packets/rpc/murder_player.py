from scapy.fields import MSBExtendedField
from scapy.packet import Packet


class MurderPlayerRPC(Packet):
    name = "MurderPlayerRPC"
    fields_desc = [
        MSBExtendedField("playerNetId", None),
    ]

    def extract_padding(self, p):
        return "", p
