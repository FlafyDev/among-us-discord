from crewmate.utils import PacketFieldEnum


class HazelType(PacketFieldEnum):
    UNRELIABLE = 0
    RELIABLE = 1
    HELLO = 8
    DISCONNECT = 9
    ACK = 10
    FRAGMENT = 11
    PING = 12

    @classmethod
    def get_reliable(cls):
        return {cls.RELIABLE, cls.HELLO, cls.PING}

    @classmethod
    def get_unreliable(cls):
        return {cls.UNRELIABLE, cls.DISCONNECT, cls.ACK, cls.FRAGMENT}


class ChatNoteTypes(PacketFieldEnum):
    DIDVOTE = 0


class RPCAction(PacketFieldEnum):
    PLAYANIMATION = 0
    COMPLETETASK = 1
    SYNCSETTINGS = 2
    SETINFECTED = 3
    EXILED = 4
    CHECKNAME = 5
    SETNAME = 6
    CHECKCOLOR = 7
    SETCOLOR = 8
    SETHAT = 9
    SETSKIN = 10
    REPORTDEADBODY = 11
    MURDERPLAYER = 12
    SENDCHAT = 13
    STARTMEETING = 14
    SETSCANNER = 15
    SENDCHATNOTE = 16
    SETPET = 17
    SETSTARTCOUNTER = 18
    ENTERVENT = 19
    EXITVENT = 20
    SNAPTO = 21
    CLOSE = 22
    VOTINGCOMPLETE = 23
    CASTVOTE = 24
    CLEARVOTE = 25
    ADDVOTE = 26
    CLOSEDOORSOFTYPE = 27
    REPAIRSYSTEM = 28
    SETTASKS = 29
    UPDATEGAMEDATA = 30


class RoomMessageType(PacketFieldEnum):
    HOST_GAME = 0
    JOIN_GAME = 1
    START_GAME = 2
    REMOVE_GAME = 3
    REMOVE_PLAYER = 4
    GAME_DATA = 5
    GAME_DATA_TO = 6
    JOINED_GAME = 7
    END_GAME = 8
    GET_GAME_LIST = 9
    ALTER_GAME = 10
    KICK_PLAYER = 11
    WAIT_FOR_HOST = 12
    REDIRECT = 13
    RESELECT_SERVER = 14


class GameDataType(PacketFieldEnum):
    DATA = 1
    RPC = 2
    SPAWN = 4
    DESPAWN = 5
    SCENE_CHANGE = 6
    READY = 7
    CHANGE_SETTINGS = 8
