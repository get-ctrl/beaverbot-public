

import asyncio
import websockets
import json
from discordstructs import msg_create_heartbeat, msg_create_hello
from discordmeta import Meta, Author, Message

class DiscordBot:

    def __init__(self, token):
        self.token = token
        self.client = None
        self.running = False
        self.heartbeat_task = None
        self.heartbeat_interval = 40
        self.heartbeat_sequence = 0
        self.events = {}
    
    async def connect(self):
        print("[~] Connect")
        if self.client: return
        self.client = await websockets.connect("wss://gateway.discord.gg/?v=10&encoding=json", max_size=5_000_000)
        await self.client.send(msg_create_hello(self.token))
        print("[~] Hello")
        self.heartbeat_task = asyncio.create_task(self.heartbeat())
        self.running = True
    
    async def disconnect(self):
        print("[~] Disconnect")
        if self.client: await self.client.close()
        if self.heartbeat_task: self.heartbeat_task.cancel()
        self.running = False
    
    async def reconnect(self):
        print("[~] Reconnect")
        await self.disconnect()
        await asyncio.sleep(1)
        await self.connect()
    
    async def heartbeat(self): # cpu well
        print("[~] Heartbeat Start")
        while self.running and self.client:
            await asyncio.sleep(self.heartbeat_interval)
            if not self.running or not self.client: continue
            msg = msg_create_heartbeat(self.token, self.heartbeat_sequence)
            await self.client.send(msg)
            print("[~] Heartbeat")
    
    async def core(self): # cpu well
        while self.running and self.client:
            try:
                meta = await self.recv_message()
                match meta.op:
                    case 7:
                        await self.reconnect()
                    case 9:
                        await self.reconnect()
                    case 10:
                        self.heartbeat_interval = meta.d["heartbeat_interval"] / 1000
                if meta.s: self.heartbeat_sequence = meta.s
                asyncio.create_task(self.on_message(meta))
            except Exception as ex:
                print("[!] Core exception\n{0}".format(ex.Message))
                await self.reconnect()
    
    async def recv_message(self):
        if not self.client: return None
        try:
            recv = await self.client.recv()
            data = json.loads(recv)
            return Meta(data)
        except:
            return None
    
    async def on_message(self, meta):
        events = self.events.get(meta.t)
        if not events: return
        for event in events:
            try: await event(meta)
            except Exception as ex:
                print("[!] Event exception\n{0}".format(ex.Message))
    
    async def start(self): # cpu well
        self.running = True
        while self.running:
            await self.reconnect()
            await asyncio.sleep(1)
            await self.core()
    
    async def stop(self):
        await self.disconnect()
