import sqlite3
import discord
import os
from DBManager import DBManager
from random import randint
from Anime import Anime

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


            if command == "add_anime":
                
                print("trying to add anime")
                a = Anime(randint(0, 1000), "test title", "test description", "test url")
                self.db_manager.add_anime(a)

                await message.channel.send("added anime: " + str(vars(a)))

            if command == "get_anime":
                
                anime = self.db_manager.get_anime_from_id(message.content.strip())

                if anime:
                    await message.channel.send("got anime: " + str(vars(anime)))
                else:
                    await message.channel.send("couldn't find that anime owo")



        

game = discord.Game("with octopodes")
s = Shokushu(activity=game)
TOKEN = str(os.environ['ShokushuToken'])
print(TOKEN)
s.run(TOKEN)
