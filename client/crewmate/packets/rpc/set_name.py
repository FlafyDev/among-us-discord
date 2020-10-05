from scapy.fields import StrLenField, IntField, ByteField
from scapy.packet import Packet

from crewmate.utils import MSBExtendedFieldLenField


class SetNameRPC(Packet):
    name = "SetNameRPC"
    fields_desc = [
        MSBExtendedFieldLenField("playerNameLen", None, "playerName"),
        StrLenField(
            "playerName",
            None,
            length_from=lambda packet: packet.playerNameLen
        )
    ]

    def extract_padding(self, p):
        return "", p
