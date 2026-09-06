
class Meta:
    op: int
    t: str
    s: int
    d: dict
    def __init__(self, data: dict):
        self.op = data.get("op")
        self.t = data.get("t")
        self.s = data.get("s")
        self.d = data.get("d")

class Author:
    id: str
    username: str
    global_name: str
    clan: str
    avatar: str
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.username = data.get("username")
        self.global_name = data.get("global_name")
        self.clan = data.get("clan")
        self.avatar = data.get("avatar")

class Message:
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
    def __init__(self, meta: Meta):
        data: dict = meta.d
        self.id = data.get("id")
        self.channel_id = data.get("channel_id")
        self.guild_id = data.get("guild_id")
        self.content = data.get("content")
        self.attachments = data.get("attachments")
        self.mentions = data.get("mentions")
        self.mention_roles = data.get("mention_roles")
        self.mention_everyone = data.get("mention_everyone")
        self.author = Author(data.get("author"))
        self.meta = meta
