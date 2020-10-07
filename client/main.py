import threading
import webbrowser
from time import sleep
from scapy.layers.inet6 import UDP, IP
from scapy.sendrecv import sniff
import eel
from communicator import Communicator, valid_and_different_key
from crewmate.packets import RPC, RoomMessageType, RPCAction, RoomMessage, GameData, GameDataType
from utils import *

enable_sniff = False
secret_key = ""
comm_thread = None
record_data = None
game_players_data = None
state = None
communicator = None
current_room_code = None
meeting_end_mute_delay = 7
among_us_port = 22023
local_ip = get_local_ip()
eel.init("web")
app_utils = AppUtils(eel)

def change_state(state_: States):
    global state
    if state != state_:
        app_utils.output_print("State changed to:", state_.name)
        app_utils.set_current_state(state_.name)
        state = state_

def dissector(packet):
    global game_players_data, record_data, state, communicator, enable_sniff, current_room_code, among_us_port, meeting_end_mute_delay
    # print(bytes(packet).hex())

    if not enable_sniff:
        return

    if packet.haslayer(UDP) and packet.haslayer(IP):
        udp_layer = packet.getlayer(UDP)
        ip_layer = packet.getlayer(IP)
    else:
        return

    # print(dir(packet.payload.payload))
    data = bytes(udp_layer.payload)
    if  (len(data) == 22 and data.startswith(b'\x00\x12\x00\x05')) or \
        (len(data) == 23 and data.startswith(b'\x00\x13\x00\x05')):

        prev_port = among_us_port
        among_us_port = get_among_us_port(udp_layer, ip_layer, local_ip)
        if prev_port != among_us_port:
            app_utils.output_print("Found Among Us port:", among_us_port)

        room_code = int.from_bytes(data[4:8], byteorder="little", signed=True)
        room_code = int_to_room_code_v2(room_code)
        # print(message.type, new_code)
        if current_room_code != room_code and room_code != "QQQQQQ":
            change_state(States.joined)
            communicator.set_mute(0)
            current_room_code = room_code
            app_utils.output_print("Room code:", current_room_code)
            app_utils.set_room_code(current_room_code)
            communicator.set_code(room_code)

    isRoomMessage = RoomMessage in packet
    isRPC = RPC in packet

    is_among_us_packet = among_us_port == udp_layer.dport or among_us_port == udp_layer.sport

    if isRoomMessage:
        message = packet[RoomMessage]
        if is_among_us_packet:
            # print("RM type", message.type)
            if state != States.game_started and message.type == RoomMessageType.START_GAME:
                print("Game started")
                record_data = True
                change_state(States.game_started)
                communicator.set_mute(1)

            elif state != States.game_ended and message.type == RoomMessageType.END_GAME:
                print("Game ended")
                change_state(States.game_ended)
                communicator.set_mute(0)

    if isRPC:
        rpc = packet[RPC]
        # print("RPC type", rpc.rpcAction)
        if record_data and rpc.rpcAction == RPCAction.UPDATEGAMEDATA:
            print("Recoreded player data", rpc.updateGameData.players)
            game_players_data = rpc.updateGameData.players
            record_data = False

        if is_among_us_packet:
            if state != States.meeting_started and rpc.rpcAction == RPCAction.STARTMEETING:
                print("Meeting started")
                change_state(States.meeting_started)
                communicator.set_mute(0)

            elif state != States.meeting_ended and rpc.rpcAction == RPCAction.CLOSE:
                print("Meeting ended", isRPC, isRoomMessage)
                change_state(States.meeting_ended)
                sleep(meeting_end_mute_delay)
                communicator.set_mute(1)

# def get_ports(packet):
#     print(packet.getlayer(UDP).sport, '-->', packet.getlayer(UDP).dport)

def get_communicator():
    global communicator, enable_sniff, comm_thread, secret_key

    def check_abort():
        return comm_thread is not None and comm_thread != initial_comm_thread

    initial_comm_thread = comm_thread

    while True:
        app_utils.output_print("Connecting to the bot's server...")
        communicator = Communicator(secret_key)
        app_utils.set_bot_server(communicator.key.url)
        server_on, status_code = communicator.test_server()
        print("Server is working and key is valid:", server_on, status_code)
        if server_on:
            app_utils.set_current_key(secret_key)
            app_utils.output_remove_lines(1)
            app_utils.output_print("Connected to the bot's server!")
            enable_sniff = True
            communicator.set_mute(0)
            return
        else:
            print("Failed testing. Status code:", status_code)
            if check_abort():
                return
            app_utils.output_remove_lines(1)
            if status_code == 401:
                app_utils.output_print("Key is invalid!")
            else:
                app_utils.output_print("Bot's server is off!")

            app_utils.output_print("Trying again in a 10 seconds")
            sleep(10)
            if check_abort():
                return
            app_utils.output_remove_lines(2)

@eel.expose
def update_key(key):
    print(key)
    global secret_key, comm_thread, enable_sniff
    if valid_and_different_key(key, secret_key):
        secret_key = key
        app_utils.output_print(f"Set key: {secret_key}")
        enable_sniff = False
        comm_thread = threading.Thread(target=get_communicator)
        comm_thread.daemon = True
        comm_thread.start()

@eel.expose
def update_mute_delay_meeting(num):
    global meeting_end_mute_delay
    meeting_end_mute_delay = num

@eel.expose
def open_repo():
    webbrowser.open('https://github.com/FlafyDev/among-us-discord')

def main():
    sniffing_thread = threading.Thread(target=lambda:
    sniff(prn=dissector, filter=f"udp", store=False,
          started_callback=lambda: app_utils.output_print(f"listening to packets.")))
    sniffing_thread.daemon = True
    sniffing_thread.start()
    eel.start('main.html')

if __name__ == '__main__':
    main()

# class MyGrid(Widget):
#     input_key = ObjectProperty(None)
#     output = ObjectProperty(None)
#     label_room_code = ObjectProperty(None)
#     label_current_state = ObjectProperty(None)
#     label_bot_server = ObjectProperty(None)
#     label_current_key = ObjectProperty(None)
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         elements.output = self.output
#         elements.label_room_code = self.label_room_code
#         elements.label_current_state = self.label_current_state
#         elements.label_bot_server = self.label_bot_server
#         elements.label_current_key = self.label_current_key
#
#         sniffing_thread = threading.Thread(target=lambda:
#         sniff(prn=dissector, filter=f"udp", store=False,
#               started_callback=lambda: output_print(elements.output, f"listening to packets.")))
#         sniffing_thread.daemon = True
#         sniffing_thread.start()
#
#     def changed_key(self):
#         global secret_key, comm_thread, enable_sniff
#         self.input_key.text = self.input_key.text.strip()
#         if valid_and_different_key(self.input_key.text, secret_key):
#             secret_key = self.input_key.text.strip()
#             output_print(elements.output, f"Set key: {secret_key}")
#             enable_sniff = False
#             comm_thread = threading.Thread(target=get_communicator)
#             comm_thread.daemon = True
#             comm_thread.start()
#
#     def open_repo(self):
#         webbrowser.open('https://github.com/FlafyDev/among-us-discord')
