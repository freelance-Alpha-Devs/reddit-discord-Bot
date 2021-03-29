import os
import random
import discord

TOKEN = "NzM0MTI3Njk0NDE2OTY5NzMx.XxNLsQ.jxCFi9qI-BZ1U5-h-gmkfyudHdg"
prefix = "//"
defaultRole = "Visitors"

client = discord.Client()

embed=discord.Embed(title="Developer Bot", description="The best dev bot.", color=0x2196F3)
embed.set_author(name="Authors: Lads", url="https://www.patreon.com/unknownProjects")
#embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/marvelmovies/images/0/06/J.A.R.V.I.S..jpg/revision/latest?cb=20130421191808")
embed.add_field(name="Clean messages", value="#clean, deletes a number of message that you put in", inline= False)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    print("message")
    print(message)
    global queue
    global voice
    global pause
    global loop
    global source
    global volume
    channel = client.get_channel(message.channel.id)
    text = str(message.content)
    if message.author.bot == False and text[:5] == str(prefix + "help"):
        await channel.send(embed=embed)
    if message.author.bot == False and text[:6] == str(prefix + "clean"):
        number = int(text[6:].replace(" ", ""))
        print(number)
        await channel.purge(limit = number)
        await channel.send(f"```I've deleted {number} messages my lad.```")

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=defaultRole)
    await member.add_roles(role)

@client.event
async def on_message(message):
    global queue
    global voice
    global pause
    global loop
    global source
    global volume
    channel = client.get_channel(message.channel.id)
    text = str(message.content)
    if message.author.bot == False and text[:6] == str(prefix + "help"):
        await channel.send(embed=embed)
    if message.author.bot == False and text[:7] == str(prefix + "clean"):
        number = int(text[7:].replace(" ", ""))
        print(number)
        await channel.purge(limit = number)
        await channel.send(f"```I've deleted {number} messages my dev.```")


client.run(TOKEN)

