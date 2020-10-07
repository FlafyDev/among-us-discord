import socket
from enum import Enum

_V2 = "QWXRTYLPESDFGHUJKZOCVBINMA"

class States(Enum):
    game_started = 0
    meeting_started = 1
    meeting_ended = 2
    game_ended = 3
    joined = 4

def int_to_room_code_v2(code):
    if isinstance(code, bytes):
        code = int.from_bytes(code, byteorder='little')
    a = code & 0x3FF
    b = (code >> 10) & 0xFFFFF

    return  _V2[a % 26] + \
            _V2[a // 26] + \
            _V2[b % 26] + \
            _V2[b // 26 % 26] + \
            _V2[b // (26 * 26) % 26] + \
            _V2[b // (26 * 26 * 26) % 26]

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "0.0.0.0"

def get_among_us_port(udp_layer, ip_layer, local_ip):
    if 20000 <= udp_layer.dport <= 29999 and ip_layer.src == local_ip:
        port = udp_layer.dport
    else:
        port = udp_layer.sport
    return port

class AppUtils:
    def __init__(self, eel=None):
        self.eel = eel

    def output_print(self, *args, sep=' ', end='\n'):
        self.eel.add_output(sep.join(str(x) for x in args) + end)

    def output_remove_lines(self, lines=1):
        self.eel.output_remove_lines(lines)

    def set_room_code(self, text):
        self.eel.set_room_code(text)

    def set_current_state(self, text):
        self.eel.set_current_state(text)

    def set_bot_server(self, text):
        self.eel.set_bot_server(text)

    def set_current_key(self, text):
        self.eel.set_current_key(text)
