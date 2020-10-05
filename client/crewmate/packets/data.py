from scapy.fields import MSBExtendedField, ByteField, StrLenField, PacketListField, LEShortField
from scapy.packet import Packet

from crewmate.utils import MSBExtendedFieldLenField, SizeAwarePacket


class TaskData(Packet):
    name = "TaskData"
    fields_desc = [
        MSBExtendedField("taskId", None),
        ByteField("complete", None),
    ]

    def extract_padding(self, p):
        return "", p


class PlayerData(SizeAwarePacket, Packet):
    name = "PlayerData"
    fields_desc = [
        LEShortField("playerDataLen", None),
        ByteField("playerId", None),
        MSBExtendedFieldLenField("playerNameLen", None, "playerName"),
        StrLenField(
            "playerName", None,
            length_from=lambda packet: packet.playerNameLen
        ),
        ByteField("colorId", None),
        MSBExtendedField("hatId", None),
        MSBExtendedField("petId", None),
        MSBExtendedField("skinId", None),
        ByteField("statusBitField", None),  # TODO: Convert to BitField
        ByteField("taskCount", None),
        PacketListField(
            "tasks", [], cls=TaskData,
            count_from=lambda packet: packet.taskCount,
        ),
    ]

    def get_expected_size(self):
        return self.playerDataLen + 3
