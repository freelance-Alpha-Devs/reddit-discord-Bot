import discord
import discordhelp
import os

# made for docker, if the environment variable doesn't exist use token.conf to read the bots token
envToken = os.environ.get("BOT_TOKEN", False)
if envToken:
    TOKEN = envToken
else:
    f = open("token.conf")      #if you are not running docker, put your discord token into token.conf
    TOKEN = f.readline()
    f.close()

prefix = "//"
defaultRole = "Visitors"

client = discord.Client()

embed = discord.Embed(title="Developer Bot", description="The best dev bot.", color=0x2196F3)
embed.set_author(name="Authors: Devs", url="https://www.patreon.com/unknownProjects")
embed.set_thumbnail(
    url="https://cdn.discordapp.com/avatars/734127694416969731/494a49a03df1d4c53d7d5c659d8328a3.png?size=128")
embed.add_field(name="Prefix", value="The bots prefix is //", inline=False)
embed.add_field(name="Clean messages", value="//clean, deletes a number of message that you put in, up to 50",
                inline=False)
embed.add_field(name="Clean messages",
                value="//hardclean, deletes a number of message that you put in, no limit, preferably use //clean",
                inline=False)
embed.add_field(name="Help menu", value="//help, shows this menu", inline=False)

client = discord.Client()

ids = {
    "incoming": 0,
    "incoming-unrelated": 0,
    "reached-out": 0,
    "turned-down": 0,
    "bot-news": 0,
    "bot-id": 0,
}


@client.event
async def on_ready():
    channels = client.get_all_channels()
    for channel in channels:
        if channel.name in ids:
            ids[channel.name] = channel.id
    ids["bot-id"] = client.user.id
    await client.get_channel(ids["bot-news"]).send("I am back online and ready to serve you my devs.")


async def permissionError(channel):
    await channel.send(f"```You are a peasant and you don't have permissions to access this command.```")


@client.event
async def on_message(message):
    channel = client.get_channel(message.channel.id)
    text = str(message.content)
    text = text.split()
    if not message.author.bot and text[0] == str(prefix + "help"):
        await channel.send(embed=embed)
    if not message.author.bot and text[0] == str(prefix + "clean"):
        if "a d m i n" in [role.name.lower() for role in message.author.roles]:
            if len(text) > 1:
                number = int(text[1])
                if number <= 50:
                    await channel.purge(limit=number)
                    await channel.send(f"```I've deleted {number} messages my dev.```")
                else:
                    await channel.send(f"```You can't delete that many messages.```")
            else:
                number = 10
                await channel.purge(limit=number)
                await channel.send(f"```I've deleted {number} messages my dev.```")
        else:
            await permissionError(channel)
    if not message.author.bot and text[0] == str(prefix + "hardclean"):
        if "a d m i n" in [role.name.lower() for role in message.author.roles]:
            if len(text) > 1:
                number = int(text[1])
                await channel.purge(limit=number)
                await channel.send(f"```I've deleted {number} messages my dev.```")
            else:
                number = 10
                await channel.purge(limit=number)
                await channel.send(f"```I've deleted {number} messages my dev.```")
        else:
            await permissionError(channel)
    if message.channel.id == ids["incoming"] or message.channel.id == ids["reached-out"] or message.channel.id == ids["incoming-unrelated"]:
        if message.author.bot:
            await message.add_reaction(discordhelp.getEmoteFromName(":green_circle:"))
            await message.add_reaction(discordhelp.getEmoteFromName(":red_circle:"))


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=defaultRole)
    await member.add_roles(role)


@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id != ids["bot-id"] and payload.channel_id == ids["incoming"]:
        if payload.emoji.name == discordhelp.getEmoteFromName(":green_circle:"):
            channel = client.get_channel(ids["incoming"])
            message = await channel.fetch_message(payload.message_id)
            await client.get_channel(ids["reached-out"]).send(embed=message.embeds[0])
            await message.delete()
        elif payload.emoji.name == discordhelp.getEmoteFromName(":red_circle:"):
            channel = client.get_channel(ids["incoming"])
            message = await channel.fetch_message(payload.message_id)
            await client.get_channel(ids["turned-down"]).send(embed=message.embeds[0])
            await message.delete()

    elif payload.user_id != ids["bot-id"] and payload.channel_id == ids["incoming-unrelated"]:
        if payload.emoji.name == discordhelp.getEmoteFromName(":green_circle:"):
            channel = client.get_channel(ids["incoming-unrelated"])
            message = await channel.fetch_message(payload.message_id)
            await client.get_channel(ids["reached-out"]).send(embed=message.embeds[0])
            await message.delete()
        elif payload.emoji.name == discordhelp.getEmoteFromName(":red_circle:"):
            channel = client.get_channel(ids["incoming-unrelated"])
            message = await channel.fetch_message(payload.message_id)
            await client.get_channel(ids["turned-down"]).send(embed=message.embeds[0])
            await message.delete()

    elif payload.user_id != ids["bot-id"] and payload.channel_id == ids["reached-out"]:
        if payload.emoji.name == discordhelp.getEmoteFromName(":green_circle:"):
            channel = client.get_channel(ids["reached-out"])
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
            channel = client.get_channel(ids["reached-out"])
            message = await channel.fetch_message(payload.message_id)
            await message.delete()


if __name__ == "__main__":
    client.run(TOKEN)
