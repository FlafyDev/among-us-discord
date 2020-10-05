from scapy.fields import ByteField
from scapy.packet import Packet


class StartMeetingRPC(Packet):
    name = "StartMeetingRPC"
    fields_desc = [
        ByteField("playerId", None),
    ]

    def extract_padding(self, p):
        return "", p
