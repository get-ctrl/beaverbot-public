
import json

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

def msg_create_hello(token):
    data = WS_HELLO.copy()
    data["d"]["token"] = token
    return json.dumps(data)

def msg_create_heartbeat(token, sequence):
    data = WS_HEARTBEAT.copy()
    data["d"]["token"] = token
    data["d"]["s"] = sequence
    return json.dumps(data)