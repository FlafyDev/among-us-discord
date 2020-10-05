from scapy.fields import ByteField, ByteEnumField
from scapy.packet import Packet

from crewmate.packets.enums import ChatNoteTypes


class SendChatNoteRPC(Packet):
    name = "SendChatNoteRPC"
    fields_desc = [
        ByteField("playerId", None),
        ByteEnumField("chatNoteType", None, ChatNoteTypes.as_dict()),
    ]

    def extract_padding(self, p):
        return "", p
