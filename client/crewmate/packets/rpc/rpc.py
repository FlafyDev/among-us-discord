from scapy.fields import MSBExtendedField, ByteEnumField, PacketField
from scapy.packet import Packet

from crewmate.packets.enums import RPCAction
from crewmate.packets.rpc.complete_task import CompleteTaskRPC
from crewmate.packets.rpc.report_dead_body import ReportDeadBodyRPC
from crewmate.packets.rpc.send_chat import SendChatRPC
from crewmate.packets.rpc.send_chat_note import SendChatNoteRPC
from crewmate.packets.rpc.set_color import SetColorRPC
from crewmate.packets.rpc.set_hat import SetHatRPC
from crewmate.packets.rpc.set_name import SetNameRPC
from crewmate.packets.rpc.set_pet import SetPetRPC
from crewmate.packets.rpc.set_skin import SetSkinRPC
from crewmate.packets.rpc.set_start_counter import SetStartCounterRPC
from crewmate.packets.rpc.start_meeting import StartMeetingRPC
from crewmate.packets.rpc.update_game_data import UpdateGameDataRPC
from crewmate.packets.rpc.voting_complete import VotingCompleteRPC
from crewmate.packets.rpc.murder_player import MurderPlayerRPC
from crewmate.utils import field_switch


class RPC(Packet):
    name = "RPC"
    fields_desc = [
        MSBExtendedField("rpcTargetId", None),
        ByteEnumField("rpcAction", None, RPCAction.as_dict()),
        *field_switch({
            RPCAction.SENDCHAT: PacketField("sendChat", None, SendChatRPC),
            RPCAction.SETSTARTCOUNTER: PacketField("setStartCounter", None, SetStartCounterRPC),
            RPCAction.SETCOLOR: PacketField("setColor", None, SetColorRPC),
            RPCAction.SETHAT: PacketField("setHat", None, SetHatRPC),
            RPCAction.SETSKIN: PacketField("setSkin", None, SetSkinRPC),
            RPCAction.SETPET: PacketField("setPet", None, SetPetRPC),
            RPCAction.SETNAME: PacketField("setName", None, SetNameRPC),
            RPCAction.STARTMEETING: PacketField("startMeeting", None, StartMeetingRPC),
            RPCAction.VOTINGCOMPLETE: PacketField("votingComplete", None, VotingCompleteRPC),
            RPCAction.SENDCHATNOTE: PacketField("sendChatNote", None, SendChatNoteRPC),
            RPCAction.REPORTDEADBODY: PacketField("reportDeadBody", None, ReportDeadBodyRPC),
            RPCAction.UPDATEGAMEDATA: PacketField("updateGameData", None, UpdateGameDataRPC),
            RPCAction.COMPLETETASK: PacketField("completeTask", None, CompleteTaskRPC),
            RPCAction.MURDERPLAYER: PacketField("murderPlayer", None, MurderPlayerRPC)
        }, lambda pkt: pkt.rpcAction),
    ]

    def extract_padding(self, p):
        return "", p
