import sqlite3
import discord
import os

from jikanpy import Jikan


from DBManager import DBManager
from random import randint
from Anime import Anime

class Shokushu(discord.Client):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.db_manager = DBManager()

        self.jikan = Jikan()

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

                    id = message.content.strip()

                    try:
                        anime_info = self.jikan.anime(int(id))

                    except Exception as e:

                        print(repr(e))
                        await message.channel.send("there was a problem getting that anime")
                        return

                    title = anime_info['title_english']
                    description = anime_info['synopsis']
                    url = anime_info['url']

                    a = Anime(id, title, description, url)

                    self.db_manager.add_anime(a)                   

                    await message.channel.send("Added: ***{0}*** \n {1}".format(title, url))

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

                        STRING_TEMPLATE = "***{0}*** \n {1}"

                        message_string = "（っ＾▿＾） I found these animes: \n"

                        for i, anime in enumerate(animes):

                            message_string += STRING_TEMPLATE.format(i, anime.my_anime_list_url) + "\n"


                        await message.channel.send(message_string)
                    else:

                        await message.channel.send("（ つ︣﹏╰） no anime in that queue")

        except Exception as e:
            print(repr(e))
            await message.channel.send("oh no ; _ ; something went wrong")


        

game = discord.Game("with octopodes")
s = Shokushu(activity=game)
TOKEN = str(os.environ['ShokushuToken'])
print(TOKEN)
s.run(TOKEN)
