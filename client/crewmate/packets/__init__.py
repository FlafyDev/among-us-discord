from scapy.layers.inet import UDP
from scapy.packet import bind_layers

from .base import *
from .enums import *
from .rpc.rpc import RPC


bind_layers(UDP, Hazel)
