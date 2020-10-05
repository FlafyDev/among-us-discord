from scapy.fields import MSBExtendedField
from scapy.packet import Packet


class SetSkinRPC(Packet):
    name = "SetSkinRPC"
    fields_desc = [
        MSBExtendedField("skinId", None),
    ]

    def extract_padding(self, p):
        return "", p
