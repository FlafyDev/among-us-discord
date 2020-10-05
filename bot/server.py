import asyncio
from http.server import BaseHTTPRequestHandler
import socketserver
from urllib.parse import urlparse, parse_qs
from room import *
import threading

add_room_to_refresh = None
add_room_to_set_code = None
discord_loop = None

class MyHandler(BaseHTTPRequestHandler):
    def send_text(self, status_code, text=""):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(text.encode("utf-8"))

    def do_POST(self):
        if self.path.startswith('/mute?'):
            o = urlparse(self.path)
            parameters = parse_qs(o.query)
            if {"mute", "secret"} <= parameters.keys():
                try:
                    mute = bool(int(parameters["mute"][0]))
                except:
                    self.send_text(400)
                    return
                secret_key = parameters["secret"][0]

                for room_ in rooms:
                    room_ = rooms[room_]
                    if room_.secret_key == secret_key:
                        room_.mute = mute
                        print(int(time()), "telling the bot to mute", mute)
                        add_room_to_refresh(room_)
                        self.send_text(200)
                        return

                self.send_text(401)

            else:
                self.send_text(400)
        elif self.path == '/mute':
            self.send_text(400)
        elif self.path.startswith("/check?"):
            o = urlparse(self.path)
            parameters = parse_qs(o.query)
            if {"secret"} <= parameters.keys():
                secret_key = parameters["secret"][0]

                for room_ in rooms:
                    room_ = rooms[room_]
                    if room_.secret_key == secret_key:
                        self.send_text(200)
                    else:
                        self.send_text(401)
            else:
                self.send_text(400)
        elif self.path == '/check':
            self.send_text(400)
        elif self.path.startswith('/roomCode?'):
            o = urlparse(self.path)
            parameters = parse_qs(o.query)
            if {"roomCode", "secret"} <= parameters.keys():
                try:
                    room_code = parameters["roomCode"][0]
                except:
                    self.send_text(400)
                    return
                secret_key = parameters["secret"][0]

                for room_ in rooms:
                    room_ = rooms[room_]
                    if room_.secret_key == secret_key:
                        add_room_to_set_code(room_, room_code)
                        self.send_text(200)
                        return

                self.send_text(401)
            else:
                self.send_text(400)
        elif self.path == '/code':
            self.send_text(400)

        else:
            self.send_text(404)

    def do_GET(self):
        if self.path == '/':
            self.send_text(200, "server is running")
        else:
            self.send_text(404)

def create_server(port, loop, add_room_to_refresh_func, add_room_to_set_code_func):
    global discord_loop, add_room_to_refresh, add_room_to_set_code
    discord_loop = loop
    add_room_to_refresh = add_room_to_refresh_func
    add_room_to_set_code = add_room_to_set_code_func
    httpd = socketserver.TCPServer(("", port), MyHandler)
    print("Server is ready.")
    httpd.serve_forever()
