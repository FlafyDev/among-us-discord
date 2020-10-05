from scapy.fields import MSBExtendedField
from scapy.packet import Packet


class CompleteTaskRPC(Packet):
    name = "CompleteTaskRPC"
    fields_desc = [
        MSBExtendedField("taskId", None),
    ]

    def extract_padding(self, p):
        return "", p
