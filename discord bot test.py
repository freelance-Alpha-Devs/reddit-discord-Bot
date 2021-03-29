import os

import discord



TOKEN = "NzM0MTI3Njk0NDE2OTY5NzMx.XxNLsQ.jxCFi9qI-BZ1U5-h-gmkfyudHdg"


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    print("message")
    print(message)

client.run(TOKEN)

