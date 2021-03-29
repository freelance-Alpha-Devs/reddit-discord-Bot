import discord
import discordhelp

TOKEN = "NzM0MTI3Njk0NDE2OTY5NzMx.XxNLsQ.jxCFi9qI-BZ1U5-h-gmkfyudHdg"
prefix = "//"
defaultRole = "Visitors"

client = discord.Client()

embed = discord.Embed(title="Developer Bot", description="The best dev bot.", color=0x2196F3)
embed.set_author(name="Authors: Devs", url="https://www.patreon.com/unknownProjects")
embed.set_thumbnail(
    url="https://cdn.discordapp.com/avatars/734127694416969731/494a49a03df1d4c53d7d5c659d8328a3.png?size=128")
embed.add_field(name="Prefix", value="The bots prefix is //", inline=False)
embed.add_field(name="Clean messages", value="//clean, deletes a number of message that you put in, up to 50", inline=False)
embed.add_field(name="Help menu", value="//help, shows this menu", inline=False)

TOKEN = "NzM0MTI3Njk0NDE2OTY5NzMx.XxNLsQ.jxCFi9qI-BZ1U5-h-gmkfyudHdg"

client = discord.Client()

incomingChannelID = 826009344315097089
unrelatedId = 826057178104070154
webhookId = 826045724809887774
botId = 734127694416969731
reachedOutId = 826058066448613427
turnedDownId = 826057917915987968
generalId = 825980284243673119


@client.event
async def on_ready():
    await client.get_channel(generalId).send("I am back online and ready to serve you my devs.")


@client.event
async def on_message(message):
    channel = client.get_channel(message.channel.id)
    text = str(message.content)
    print(message)
    if message.author.bot == False and text[:6] == str(prefix + "help"):
        await channel.send(embed=embed)
    if message.author.bot == False and text[:7] == str(prefix + "clean"):
        splited = text.split()
        if len(splited) > 1:
            number = int(splited[1])
            if number <= 50:
                await channel.purge(limit=number)
                await channel.send(f"```I've deleted {number} messages my dev.```")
            else:
                await channel.send(f"```You can't delete that many messages.```")
        else:
            number = 10
            await channel.purge(limit=number)
            await channel.send(f"```I've deleted {number} messages my dev.```")
    if message.channel.id == incomingChannelID or message.channel.id == reachedOutId or message.channel.id == unrelatedId:
        if message.author.bot:
            await message.add_reaction(discordhelp.getEmoteFromName(":green_circle:"))
            await message.add_reaction(discordhelp.getEmoteFromName(":red_circle:"))


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=defaultRole)
    await member.add_roles(role)


@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id != botId and payload.channel_id == incomingChannelID:
        if payload.emoji.name == discordhelp.getEmoteFromName(":green_circle:"):
            channel = client.get_channel(incomingChannelID)
            message = await channel.fetch_message(payload.message_id)
            await client.get_channel(reachedOutId).send(embed=message.embeds[0])
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
            await client.get_channel(reachedOutId).send(embed=message.embeds[0])
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

            newChannel = await guild.create_text_channel(name, category=category, overwrites=overwrites)
            await newChannel.send(embed=message.embeds[0])
            await message.delete()
        elif payload.emoji.name == discordhelp.getEmoteFromName(":red_circle:"):
            channel = client.get_channel(reachedOutId)
            message = await channel.fetch_message(payload.message_id)
            await message.delete()

if __name__ == "__main__":
    client.run(TOKEN)
