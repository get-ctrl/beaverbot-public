

import asyncio
import json

import websockets
import requests


class DataMap:

    def __init__(self, data):
        self.__dict__["data"] = data
    
    def __getattr__(self, name):
        if not name in self.data: return None
        value = self.data[name]
        if isinstance(value, dict): return DataMap(value)
        else: return value
    
    def __setattr__(self, name, value):
        self.data[name] = value
    
    def __repr__(self):
        return repr(self.data)

class Meta(DataMap):

    op: int
    t: str
    s: int
    d: dict

    def __init__(self, data):
        super().__init__(data)

class Author(DataMap):

    id: str
    username: str
    global_name: str
    clan: str
    avatar: str

    def __init__(self, meta):
        super().__init__(meta.data)

class Message(DataMap):

    id: str
    channel_id: str
    guild_id: str
    content: str
    attachments: list
    mentions: list
    mention_roles: list
    mention_everyone: bool
    author: Author
    meta: Meta

    def __init__(self, meta):
        super().__init__(meta.d.data)
        self.author = Author(meta.d.author)
        self.meta = meta


WS_HELLO = {
   "op": 2,
   "d": {
      "token": "",
      "intents": 33280,
      "properties": {
         "os": "TempleOS",
         "browser": "HolyBrowser",
         "device": "ComputerOfGod"
      },
      "compress": False,
   }
}

WS_HEARTBEAT = {
    "op": 1,
    "d": {
        "token": "",
        "properties": {
            "os": "TempleOS",
            "browser": "HolyBrowser",
            "device": "ComputerOfGod"
        },
    }
}

HTTP_REPLY = {
    "content": "",
    "nonce": None,
    "tts": False,
    "message_reference":{
    },
    "allowed_mentions":{
        "parse":[
            "users",
            "roles",
            "everyone"
            ],
        "replied_user": True
    },
    "flags":0
}


class DiscordBot:

    def __init__(self, token):
        self.token = token
        self.client = None
        self.isalive = False
        self.running = False
        self.heartbeat_task = None
        self.heartbeat_interval = 40
        self.heartbeat_sequence = 0
        self.events = {}
        self.commands = {}
        self.prefix = "!"
        self.http = requests.Session()
        self.http.headers = { "Authorization": f"Bot {self.token}", "Content-Type": "application/json" }
    
    async def connect(self):
        self.running = True
        print("[~] Connect")
        if self.client: return
        self.client = await websockets.connect("wss://gateway.discord.gg/?v=10&encoding=json", max_size=5_000_000)
        await self.client.send(self.build_hello_msg())
        print("[~] Hello")
        self.heartbeat_task = asyncio.create_task(self.heartbeat())
        await asyncio.sleep(1)
    
    async def disconnect(self):
        print("[~] Disconnect")
        self.running = False
        if self.client:
            await self.client.close()
            self.client = None
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            self.heartbeat_task = None
        self.heartbeat_sequence = 0
        await asyncio.sleep(1)
    
    async def reconnect(self):
        print("[~] Reconnect")
        await self.disconnect()
        await self.connect()
    
    async def heartbeat(self): # cpu well
        print("[~] Heartbeat Start")
        while self.running and self.client:
            await asyncio.sleep(self.heartbeat_interval)
            if not self.running or not self.client: continue
            msg = self.build_heartbeat_msg()
            await self.client.send(msg)
            print("[~] Heartbeat")
    
    async def reply(self, msg, content):
        data = HTTP_REPLY.copy()
        if msg.guild_id:
            data["message_reference"]["guild_id"] = msg.guild_id
        data["message_reference"]["channel_id"] = msg.channel_id
        data["message_reference"]["message_id"] = msg.id
        data["content"] = content
        url = "https://discord.com/api/v9/channels/{0}/messages".format(msg.channel_id)
        req = self.http.post(url, data=json.dumps(data))
        return req
    
    def build_hello_msg(self):
        data = WS_HELLO.copy()
        data["d"]["token"] = self.token
        return json.dumps(data)
    
    def build_heartbeat_msg(self):
        data = WS_HEARTBEAT.copy()
        data["d"]["token"] = self.token
        data["d"]["s"] = self.heartbeat_sequence
        return json.dumps(data)

    async def core(self): # cpu well
        print("[~] Core")
        print(self.running)
        print(self.client)
        while self.running and self.client:
            try:
                meta = await self.recv_message()
                if meta == None: continue
                match meta.op:
                    case 7:
                        await self.reconnect()
                    case 9:
                        await self.reconnect()
                    case 10:
                        self.heartbeat_interval = meta.d.heartbeat_interval / 1000
                if meta.s: self.heartbeat_sequence = meta.s
                asyncio.create_task(self.on_message(meta))
            except Exception as ex:
                print("[!] Core exception\n{0}".format(ex))
                await self.reconnect()
        print("[~] Core exit")
    
    async def recv_message(self):
        if not self.client: return None
        try:
            recv = await self.client.recv()
            data = json.loads(recv)
            return Meta(data)
        except:
            return None
        print("[~] Recv message")
    
    async def on_message(self, meta):
        events = self.events.get(meta.t)
        if events:
            for event in events:
                try: await event(meta)
                except Exception as ex:
                    print("[!] Event exception\n{0}".format(ex))
        if meta.t == "MESSAGE_CREATE":
            await self.on_message_create(meta)
    
    async def on_message_create(self, meta):
        msg = Message(meta)
        if not msg.content.startswith(self.prefix): return
        for command in self.commands.keys():
            if msg.content.startswith(self.prefix + command):
                try: await self.commands[command](msg)
                except Exception as ex:
                    print("[!] Command failure: {0}".format(ex))
                break
    
    async def start(self): # cpu well
        self.isalive = True
        while self.isalive:
            print("[~] Core loop")
            await self.reconnect()
            await self.core()
            await asyncio.sleep(10)
    
    async def stop(self):
        self.isalive = False
        await self.disconnect()
