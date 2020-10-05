from scapy.fields import MSBExtendedField
from scapy.packet import Packet


class SetHatRPC(Packet):
    name = "SetHatRPC"
    fields_desc = [
        MSBExtendedField("hatId", None),
    ]

    def extract_padding(self, p):
        return "", p
