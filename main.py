import sqlite3
import discord
import os
from DBManager import DBManager

class Shokushu(discord.Client):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.db_manager = DBManager()

    async def on_ready(self):
        print("logged on as", self.user)

    async def on_message(self, message):

        # don't respond to ourselves
        if message.author == self.user:
            return
    
        self.db_manager.add_user_if_required(message.author.name)

        # Respond if we were mentioned
        if self.user.mentioned_in(message) and len(message.content.split(" ")) > 1:

            print("we were mentioned")
            command = message.content.split(" ")[1]
            message.content = " ".join(message.content.split(" ")[2:]) # Strip out the mention and command for easier message handling

        

game = discord.Game("with octopodes")
s = Shokushu(activity=game)
TOKEN = str(os.environ['ShokushuToken'])
print(TOKEN)
s.run(TOKEN)
