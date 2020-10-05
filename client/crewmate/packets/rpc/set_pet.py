from scapy.fields import MSBExtendedField
from scapy.packet import Packet


class SetPetRPC(Packet):
    name = "SetPetRPC"
    fields_desc = [
        MSBExtendedField("petId", None),
    ]

    def extract_padding(self, p):
        return "", p
