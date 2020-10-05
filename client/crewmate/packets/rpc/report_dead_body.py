from scapy.fields import ByteField
from scapy.packet import Packet


class ReportDeadBodyRPC(Packet):
    name = "ReportDeadBodyRPC"
    fields_desc = [
        ByteField("playerId", None),
    ]

    def extract_padding(self, p):
        return "", p
