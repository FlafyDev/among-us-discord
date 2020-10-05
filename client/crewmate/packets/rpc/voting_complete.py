from scapy.fields import ByteField, LEShortField, StrLenField
from scapy.packet import Packet

class VotingCompleteRPC(Packet):
    name = "VotingCompleteRPC"
    fields_desc = [
        # LEShortField("statesLen", None),
        # StrLenField(
        #     "statesArray",
        #     None,
        #     length_from=lambda packet: packet.playerNameLen
        # ),
        # ByteField("playerId", None),  # 0xFF if nobody
        # ByteField("votingTie", None),
    ]

    def extract_padding(self, p):
        return "", p
