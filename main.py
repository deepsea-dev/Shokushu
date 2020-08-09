import discord
import os

class Shokushu(discord.Client):

    async def on_ready(self):
        print("logged on as", self.user)

    async def on_message(self, message):

        # don't respond to ourselves
        if message.author == self.user:
            return
    
        # Respond if we were mentioned
        if self.user.mentioned_in(message):
            await message.channel.send('pong')


game = discord.Game("with octopodes")
s = Shokushu(activity=game)
token = str(os.environ['ShokushuToken'])
print(token)
s.run(token)