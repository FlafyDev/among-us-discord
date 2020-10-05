from scapy.fields import StrLenField
from scapy.packet import Packet

from crewmate.utils import MSBExtendedFieldLenField


class SendChatRPC(Packet):
    name = "SendChatRPC"
    fields_desc = [
        MSBExtendedFieldLenField("rpcChatLen", None, "rpcChatMessage"),
        StrLenField(
            "rpcChatMessage",
            None,
            length_from=lambda packet: packet.rpcChatLen
        ),
    ]

    def extract_padding(self, p):
        return "", p
