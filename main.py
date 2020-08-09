import discord
import os

class Shokushu(discord.Client):

    async def on_ready(self):
        print("logged on as", self.user)

    async def on_message(self, message):

        # don't respond to ourselves
        if message.author == self.user:
            return
        
        if message.content.startswith('8ping'):
            await message.channel.send('pong')


game = discord.Game("with octopodes")
s = Shokushu(activity=game)
token = str(os.environ['ShokushuToken'])
print(token)
s.run(token)