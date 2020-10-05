from scapy.fields import PacketListField
from scapy.packet import Packet

from crewmate.packets.data import PlayerData


class UpdateGameDataRPC(Packet):
    name = "UpdateGameDataRPC"
    fields_desc = [
        PacketListField("players", [], cls=PlayerData)
    ]

    def extract_padding(self, p):
        return "", p
