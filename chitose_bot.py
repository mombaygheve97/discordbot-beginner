from ast import alias
from asyncio import events
from tkinter.ttk import Style
from turtle import color
from aiohttp import Payload
import discord
from discord.ext import commands
from discord import Color

intents = discord.Intents.default()
intents.members = True 

client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="!help/ version 1.0.3"))
    channel = client.get_channel(#discordchannelid)
    await channel.send("Chitose is ready to work. Let's work together everyone!")
    await channel.send("https://pa1.narvii.com/6605/3d5c889e106499c23f6c2ee78a206220b663c62f_hq.gif")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You can't do that T_T")
        await ctx.message.delete()
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Please Enter all the required args.")
        await ctx.message.delete()
    elif isinstance(error,commands.MissingRole):
        await ctx.send("You can't do that T_T. You are missing a role needed to use this command")
        await ctx.message.delete()
    else:
        raise error

@client.event
async def on_guild_join(member):
    pass

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == #messageidofyourdiscord:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        member = guild.get_member(payload.user_id)

        if payload.emoji.name == "🔴":
            role = discord.utils.get(guild.roles, name='Red')
            if role in member.roles:
                print('Member already has a role')
            else:
                await member.add_roles(role)

        elif payload.emoji.name == "🟣":
            role = discord.utils.get(guild.roles, name='Purple')
            if role in member.roles:
                print('Member already has a role')
            else:
                await member.add_roles(role)
        
        elif payload.emoji.name == "🧰":
            role = discord.utils.get(guild.roles, name='Tester')
            if role in member.roles:
                print('Member already has a role')
            else:
                await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    """
    Remove a role based on a reaction emoji
    """
    message_id = payload.message_id
    if message_id == #messageidofdiscord:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == "🔴":
            role = discord.utils.get(guild.roles, name='Red')

        elif payload.emoji.name == "🟣":
            role = discord.utils.get(guild.roles, name='Purple')
            
        elif payload.emoji.name == "🧰":
            role = discord.utils.get(guild.roles, name='Tester')

        member = guild.get_member(payload.user_id)
        await member.remove_roles(role)

@client.command()
async def help(ctx):
    embed = discord.Embed(
        title = 'Bot Commands',
        description = 'Welcome to the help section. Here are all the commands for ChitoseBot \n'
        + '!greet = To welcome people in the server (!greet) \n'
        + '!clear - to remove message(only admin) (!clear amount) \n'
        + '!kick - to remove member from the server(admin) (!kick @name)  \n'
        + '!ban - to ban members(admin) (!ban @name) \n'
        + '!message - to use chitose bot to give private message (!message @name example) \n'
        + '!addroles - to addroles(admin) (!addroles/!ar @name role_name)  \n'
        + '!removeroles - to addroles(admin) (!removeroles/!rr @name role_name) \n'
        + '!message - to use sasha bot to give private message (!message/!msg @name example)\n'
        + '!roles - to show roles (!roles @member)\n'
        + '!mute - to mute a member(admin only)\n'
        + '!unmute = to unmute a member(admin only)\n',
        color = Color.blue()
        )

    await ctx.send(embed = embed)


@client.command()
async def greet(ctx):
    await ctx.send("Welcome everyone to KawaiiBoT Hangout") 
    await ctx.send("https://pa1.narvii.com/6605/3d5c889e106499c23f6c2ee78a206220b663c62f_hq.gif")

@client.command(aliases = ['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit = amount)

@client.command(aliases = ['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member,*, reason= "No Reason Provided"):
    await member.send("You have been kicked from the Server. I'm Sorry to hear that. The Reason is: " +reason)
    await member.send("https://pa1.narvii.com/6605/92aedd96c75bc3ba917c75eea9072b2ce9c4c260_hq.gif")
    await member.kick(reason = reason)

@client.command(aliases = ['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member,*, reason= "No Reason Provided"):
    await member.send("You have been Banned from the Server. I'm Sorry to hear that. The Reason is: " +reason)
    await member.send("https://pa1.narvii.com/6605/92aedd96c75bc3ba917c75eea9072b2ce9c4c260_hq.gif")
    await member.kick(reason = reason)

@client.command(aliases = ['m'])
async def message(ctx, member: discord.Member,*, reason= "No Reason Provided"):
    await member.send(reason)
    await ctx.message.delete()

@client.command(aliases = ['msg'])
async def message(ctx, member: discord.Member,*, reason= "No Reason Provided"):
    await member.send(reason)
    await ctx.message.delete()

@client.command(aliases = ['ar'])
@commands.has_permissions(manage_roles = True)
async def addroles(ctx, member: discord.Member,*, role: discord.Role):
    role2 = discord.utils.get(ctx.guild.roles, name='Muted')

    if role != role2:
        if role in member.roles:
            await ctx.send(f"{member.mention} already have that role, {role}")
            await ctx.message.delete()
        else:
            await member.add_roles(role)
            await member.send(f"The role {role} has been added to you")
            await ctx.message.delete()

    else:
        await ctx.send("You cannot use this command to give mute role.")
        await ctx.message.delete()

@client.command(aliases = ['rr'])
@commands.has_permissions(manage_roles = True)
async def removeroles(ctx, member: discord.Member,*, role: discord.Role):

    if role in member.roles:
        await member.remove_roles(role)
        await member.send(f"The role {role} has been removed")
        await ctx.message.delete()
    else:
        await ctx.send(f"{member.mention} does not have the role, {role}")
        await ctx.message.delete()

class MemberRoles(commands.MemberConverter):
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        return [role.name for role in member.roles[1:]]

@client.command(aliases = ['r'])
async def roles(ctx, *, member: MemberRoles):
    """Tells you a member's roles."""
    await ctx.send('I see the following roles: ' + ', '.join(member))

@client.command(aliases = ['adm'])
@commands.has_role('Admin')
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')

    if role in member.roles:
        await ctx.send(f'{member} is already muted')
        await ctx.message.delete()
    else:
        await member.add_roles(role)
        await ctx.message.delete()

@client.command(aliases = ['um'])
@commands.has_role('Admin')
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')

    if role in member.roles:
        await member.remove_roles(role)
        await member.send(f"The role {role} has been removed")
        await ctx.message.delete()
    else:
        await ctx.send(f'{member} is not muted')
        await ctx.message.delete()

client.run('TOKEN')