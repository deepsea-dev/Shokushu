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

        try:
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


                if command == "add_to_queue":

                    anime = self.db_manager.get_anime_from_id(message.content.strip())

                    if not anime:
                        await message.channel.send("That anime doesn't exist :(")
                    else:
                        # Returns true if the anime was successfully added
                        if self.db_manager.add_to_queue(str(message.channel.id), anime.id):
                            await message.channel.send("Anime \"{0}\" added (✿◠‿◠)".format(anime.title))


                if command == "get_queue":

                    animes = self.db_manager.get_anime_in_queue(str(message.channel.id)) # Get the anime in this channel's queue

                    if animes: # If anime were returned
                        
                        # Build the anime string

                        STRING_TEMPLATE = "***Title: {0}*** \n Description: {1}"

                        message_string = "（っ＾▿＾） I found these animes: \n"

                        for anime in animes:

                            message_string += STRING_TEMPLATE.format(anime.title, anime.description) + "\n"


                        await message.channel.send(message_string)
                    else:

                        await message.channel.send("（ つ︣﹏╰） no anime in that queue")

        except Exception as e:
            print(str(e))
            await message.channel.send("oh no ; _ ; something went wrong")


        

game = discord.Game("with octopodes")
s = Shokushu(activity=game)
TOKEN = str(os.environ['ShokushuToken'])
print(TOKEN)
s.run(TOKEN)
