import sqlite3
import discord
import os

class Shokushu(discord.Client):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.dcon = sqlite3.connect('shokushu.db') # Database connection
        dcursor = self.dcon.cursor()

        dcursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT)")
        dcursor.execute("CREATE TABLE IF NOT EXISTS anime (anime_id INTEGER PRIMARY KEY, anime_title TEXT, anime_description TEXT, anime_url TEXT)")
        dcursor.execute("CREATE TABLE IF NOT EXISTS scores (username score_id INTEGER PRIMARY KEY, user_id)")
        dcursor.close()

    async def on_ready(self):
        print("logged on as", self.user)

    async def on_message(self, message):

        # don't respond to ourselves
        if message.author == self.user:
            return
    
        dcursor = self.dcon.cursor()
        dcursor.execute("SELECT username FROM users WHERE username = ?", [message.author.name + message.author.discriminator])
        if dcursor.fetchone() is None:
            next_primary_key = dcursor.execute("SELECT MAX(user_id) FROM users").fetchone()[0] or 0
            next_primary_key += 1

            dcursor.execute("INSERT INTO users VALUES (?, ?)", [next_primary_key, message.author.name + message.author.discriminator])
            self.dcon.commit()
            dcursor.execute("SELECT username FROM users WHERE username = ?", [message.author.name + message.author.discriminator])

        # Respond if we were mentioned
        if self.user.mentioned_in(message) and len(message.content.split(" ")) > 1:
            command = message.content.split(" ")[1]
            message.content = " ".join(message.content.split(" ")[2:]) # Strip out the mention and command for easier message handling

        dcursor.close()

game = discord.Game("with octopodes")
s = Shokushu(activity=game)
TOKEN = str(os.environ['ShokushuToken'])
print(TOKEN)
s.run(TOKEN)
