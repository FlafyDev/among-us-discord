from scapy.fields import (
    ByteEnumField,
    ShortField,
    ConditionalField,
    PacketField,
    IntField,
    PacketListField,
    LEShortField,
    ByteField,
    LESignedIntField)
from scapy.packet import Packet

from crewmate.packets.enums import (
    GameDataType,
    RoomMessageType,
    HazelType,
)
from crewmate.packets.rpc.rpc import RPC
from crewmate.utils import SizeAwarePacket, field_switch


class Data(Packet):
    name = "Data"
    fields_desc = [
    ]

    def extract_padding(self, p):
        return "", p


class Despawn(Packet):
    name = "Despawn"
    fields_desc = [
        ByteField("playerId", None),
    ]

    def extract_padding(self, p):
        return "", p


class GameData(SizeAwarePacket, Packet):
    name = "GameData"
    fields_desc = [
        LEShortField("contentSize", None),
        ByteEnumField("type", None, GameDataType.as_dict()),
        *field_switch({
            GameDataType.RPC: PacketField("rpc", None, RPC),
            GameDataType.DATA: PacketField("data", None, Data),
            GameDataType.DESPAWN: PacketField("despawn", None, Despawn),
        }, lambda pkt: pkt.type)
    ]


class RoomMessage(SizeAwarePacket, Packet):
    name = "RoomMessage"
    fields_desc = [
        LEShortField("contentSize", None),
        ByteEnumField("type", None, RoomMessageType.as_dict()),
        LESignedIntField("roomCode", None),
        PacketListField("messages", [], cls=GameData),
    ]


class Hazel(Packet):
    name = "Hazel"
    fields_desc = [
        ByteEnumField("type", None, HazelType.as_dict()),
        ConditionalField(
            ShortField("packetId", None),
            lambda packet: packet.type in HazelType.get_reliable()
        ),
        PacketField("content", None, RoomMessage),
    ]

    def extract_padding(self, p):
        return "", p
