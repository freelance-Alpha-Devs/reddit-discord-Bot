import os
import random
import discord
import discord
import discordhelp

TOKEN = "NzM0MTI3Njk0NDE2OTY5NzMx.XxNLsQ.jxCFi9qI-BZ1U5-h-gmkfyudHdg"
prefix = "//"
defaultRole = "Visitors"

client = discord.Client()

embed=discord.Embed(title="Developer Bot", description="The best dev bot.", color=0x2196F3)
embed.set_author(name="Authors: Lads", url="https://www.patreon.com/unknownProjects")
#embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/marvelmovies/images/0/06/J.A.R.V.I.S..jpg/revision/latest?cb=20130421191808")
embed.add_field(name="Clean messages", value="#clean, deletes a number of message that you put in", inline= False)

TOKEN = "NzM0MTI3Njk0NDE2OTY5NzMx.XxNLsQ.jxCFi9qI-BZ1U5-h-gmkfyudHdg"

client = discord.Client()

incomingChannelID = 826009344315097089
unrelatedId = 826057178104070154
webhookId = 826045724809887774
botId = 734127694416969731
reachedOutId = 826058066448613427
turnedDownId = 826057917915987968

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
    if message.channel.id == incomingChannelID or message.channel.id == reachedOutId or message.channel.id == unrelatedId:
        if message.author.id == webhookId or message.author.id == botId:
            await message.add_reaction(discordhelp.getEmoteFromName(":green_circle:"))
            await message.add_reaction(discordhelp.getEmoteFromName(":red_circle:"))


@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id != botId and payload.channel_id == incomingChannelID:
        if payload.emoji.name == discordhelp.getEmoteFromName(":green_circle:"):
            channel = client.get_channel(incomingChannelID)
            message = await channel.fetch_message(payload.message_id)
            await client.get_channel(reachedOutId).send(embed = message.embeds[0])
            await message.delete()
        elif payload.emoji.name == discordhelp.getEmoteFromName(":red_circle:"):
            channel = client.get_channel(incomingChannelID)
            message = await channel.fetch_message(payload.message_id)
            await client.get_channel(turnedDownId).send(embed=message.embeds[0])
            await message.delete()

    elif payload.user_id != botId and payload.channel_id == unrelatedId:
        if payload.emoji.name == discordhelp.getEmoteFromName(":green_circle:"):
            channel = client.get_channel(unrelatedId)
            message = await channel.fetch_message(payload.message_id)
            await client.get_channel(reachedOutId).send(embed = message.embeds[0])
            await message.delete()
        elif payload.emoji.name == discordhelp.getEmoteFromName(":red_circle:"):
            channel = client.get_channel(unrelatedId)
            message = await channel.fetch_message(payload.message_id)
            await client.get_channel(turnedDownId).send(embed=message.embeds[0])
            await message.delete()

    elif payload.user_id != botId and payload.channel_id == reachedOutId:
        if payload.emoji.name == discordhelp.getEmoteFromName(":green_circle:"):
            channel = client.get_channel(reachedOutId)
            message = await channel.fetch_message(payload.message_id)
            guild = message.guild
            category = discord.utils.get(guild.categories, id=825995275477843999)
            name = str(message.embeds[0].author)[17:-2].replace("/", "-")
            roles = await guild.fetch_roles()

            member = await guild.fetch_member(payload.user_id)

            shouldCreateRole = True
            for role in roles:
                if role.name == name:
                    oldRole = role
                    shouldCreateRole = False
            if shouldCreateRole:
                newRole = await guild.create_role(name=name)
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    newRole: discord.PermissionOverwrite(read_messages=True),
                }
                await member.add_roles(newRole)
            else:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    oldRole: discord.PermissionOverwrite(read_messages=True),
                }
                await member.add_roles(oldRole)

            newChannel = await guild.create_text_channel(name, category= category, overwrites=overwrites)
            await newChannel.send(embed = message.embeds[0])
            await message.delete()
        elif payload.emoji.name == discordhelp.getEmoteFromName(":red_circle:"):
            channel = client.get_channel(reachedOutId)
            message = await channel.fetch_message(payload.message_id)
            await message.delete()

client.run(TOKEN)

