import socket
from enum import Enum

_V2 = "QWXRTYLPESDFGHUJKZOCVBINMA"

class States(Enum):
    game_started = 0
    meeting_started = 1
    meeting_ended = 2
    game_ended = 3
    joined = 4

class Elements:
    output = None
    label_room_code = None
    label_current_state = None
    label_bot_server = None
    label_current_key = None

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
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def get_among_us_port(udp_layer, ip_layer, local_ip):
    if 20000 <= udp_layer.dport <= 29999 and ip_layer.src == local_ip:
        port = udp_layer.dport
    else:
        port = udp_layer.sport
    return port

def output_print(output, *args, sep=' ', end='\n'):
    output.text += sep.join(str(x) for x in args) + end

def output_delete_lines(output, lines=1):
    for _ in range(lines+1):
        output.text = output.text[:output.text.rfind('\n')]
    output_print(output)

def change_label_text(label, text):
    label.text = f"{label.text.split('[/b]')[0]}[/b] {text}"