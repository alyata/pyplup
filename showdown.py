import websockets
import parser

class Showdown:
    def __init__(self, username, password = None):
        self.uri = "ws://sim.smogon.com:8000/showdown/websocket"
        self.username = username
        self.password = password
        self.open = False

    async def connect(self):
        self.connection = await websockets.connect(self.uri)
        self.open = True

    async def close(self):
        if self.open:
            await self.connection.close()
            self.open = False

    async def consumer_handler(self):
        async for messages in self.connection:
            await self.consumer(messages)

    async def consumer(self, messages):
        for message in messages.split('\n'):
            parsed_message = self.parse(message)
            print(parsed_message)

    def parse(self, message):
        split_message = message.split('|')
        #"|messageTag|..." will always have an empty string as first element
        # after split by '|'
        split_message.remove('')
        #Switch-Case on the first word in the list
        return {
            "updateuser" : parser.updateuser,
            "formats" : parser.formats,
            "challstr" : parser.challstr
        }[split_message[0]](split_message)
