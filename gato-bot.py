import discord
from discord import Client, Activity, ActivityType, Embed, Member, HTTPException
from discord.ext import commands
from datetime import datetime
from os import system

import asyncio, time, os, requests, random

import tkinter
root = tkinter.Tk()
root.withdraw()

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
VERSION = os.getenv("VERSION")
PREFIX = os.getenv("PREFIX")
STATUS = os.getenv("STATUS")

intents = discord.Intents.all()
intents.members = True

client = Client(intents=intents) # Grab token from .env, command prefix and activity
b = commands.Bot(
    command_prefix = f'{PREFIX}',
    intents=intents,
    activity = Activity(type=ActivityType.playing, name=f'{STATUS}')
)

b.remove_command("help")

@b.event # Startup Print
async def on_ready():
    print(
        """   /$$$$$$              /$$               /$$$$$$$              /$$     \n"""
        """  /$$__  $$            | $$              | $$__  $$            | $$     \n"""
        """ | $$  \__/  /$$$$$$  /$$$$$$    /$$$$$$ | $$  \ $$  /$$$$$$  /$$$$$$   \n"""
        """ | $$ /$$$$ |____  $$|_  $$_/   /$$__  $$| $$$$$$$  /$$__  $$|_  $$_/   \n"""
        """ | $$|_  $$  /$$$$$$$  | $$    | $$  \ $$| $$__  $$| $$  \ $$  | $$     \n"""
        """ | $$  \ $$ /$$__  $$  | $$ /$$| $$  | $$| $$  \ $$| $$  | $$  | $$ /$$ \n"""
        """ |  $$$$$$/|  $$$$$$$  |  $$$$/|  $$$$$$/| $$$$$$$/|  $$$$$$/  |  $$$$/ \n"""
        """  \______/  \_______/   \___/   \______/ |_______/  \______/    \___/   \n"""
        """                                                                        \n"""
        f"""Welcome to Gato Bot {VERSION} by Gato Services\n"""
        f"""MOTD 20/07/22: Beta 1 public release finally!\n"""
        f"""Logged in as {b.user}\n"""
        f"""Status is [{STATUS}]\n"""
        f"""Prefix is [{PREFIX}]\n"""
    )

@b.command(pass_context=True) # Ping/Latency command
async def ping(ctx):
    time_1 = time.perf_counter()
    await ctx.trigger_typing()
    time_2 = time.perf_counter()
    ping = round((time_2-time_1)*1000)
    await ctx.send(f"Pong! Gato Bot currently has a ping of {ping}ms")

@b.command(aliases=["ver"]) # Grabs current version
async def version(ctx):
    embed=Embed(title=f"Gato Bot {VERSION}", url="https://github.com/gato-services", description="GatoBot is a multi-use discord bot, developed by the Gato Services team!", color=0xc481fb)
    await ctx.send(embed=embed)

@b.command(aliases=["cf"]) # Coinflip
async def coinflip(ctx):
    lista = ['head', 'tails']
    coin = random.choice(lista)
    try:
        if coin == 'head':
            embed= Embed(color=0xc481fb, title="Head",timestamp=datetime.utcfromtimestamp(time.time()))
            embed.set_thumbnail(url="https://www.the-random-generator.com/img/heads.png")
            embed.set_footer(text=f" GatoBot {VERSION}")
            await ctx.send(embed=embed)
        else:
            embed= Embed(color=0xc481fb, title="Tails",timestamp=datetime.utcfromtimestamp(time.time()))
            embed.set_thumbnail(url="https://www.the-random-generator.com/img/tails.png")
            embed.set_footer(text=f" GatoBot {VERSION}")
            await ctx.send(embed=embed)
    except HTTPException:
        if coin == 'head':
            await ctx.send("Coinflip: **Head**")
        else:
            await ctx.send("Coinflip: **Tails**")

@b.command() # Converts USB to BTC
async def usdtobtc(ctx, num: int=None):
    if num is None:
        await ctx.send("Invalid format, Please send the amount you would like to convert!")
    else:
        with requests.session() as ses:
            resp = ses.get('https://blockchain.info/ticker')
            pret = int(resp.json()['USD']['last'])
            final = num/pret
            try:
                embed = Embed(color=0xc481fb, title="USD -> BTC", description=f"USD: {num}\n BTC: {final}", timestamp=datetime.utcfromtimestamp(time.time()))
                embed.set_thumbnail(url="https://i.imgur.com/GCPDIYU.png")
                embed.set_footer(text=f" GatoBot {VERSION}")
                await ctx.send(embed=embed)
            except HTTPException:
                await ctx.send(f"USD -> BTC:\n\nUSD: {num}\n BTC: {final}")

@b.command() # Unban a user via User ID
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: Member=None):
    if user is None:
        return await ctx.send("Who do you want to unban? Please use the arg `discord_id`")
    try:
        user1 = await b.fetch_user(user)
        await ctx.guild.unban(user1)
        await ctx.send(f"User {user.mention}({user.id}) has been unbanned!")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"Error: {error}")

@b.command() # Ban a user via tagging them
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: Member=None, *, reason: str=None):
    if user is None:
        return await ctx.send("Who would you like to ban? Please `@` the specified user!")
    elif user == ctx.author:
        return await ctx.send("You can't ban yourself, I'm not that powerful D:")
    try:
        await user.ban(reason=reason)
        await ctx.send(f"User {user.mention}({user.id}) has been banned for reason {reason}. lol ;)")
    except Exception as e:
        await ctx.send(f"{e}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"Error: {error}")

@b.command() # Kick a user via tagging them
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: Member=None, *, reason: str=None):
    if user is None:
        return await ctx.send("Who would you like to kick? Please `@` the specified user!")
    elif user == ctx.author:
        return await ctx.send("You can't ban yourself, That wouldn't be cool :>")
    try:
        await user.ban(reason=reason)
        await ctx.send(f"User {user.mention}({user.id}) has been kicked for reason {reason}. #trolled")
    except Exception as e:
        await ctx.send(f"{e}")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"Error: {error}")

@b.command() # L33t Speak
async def leet(ctx, *, message: str=None):

    if message is None:
        await ctx.send("Insert the message to haxor >:)")
    else:
        rmap = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 't': '7', 's': '$'} # Simple dict mapping letters to replace
        leetmsg = message.lower().replace("you", "j00")
        for l, r in rmap.items():
            leetmsg = leetmsg.replace(l, r)
        try:
            embed= Embed(color=0xc481fb, title="1337 Haxor", description=f"{leetmsg.upper()}", timestamp=datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f" GatoBot {VERSION}")
            await ctx.send(embed=embed)
        except HTTPException:
            await ctx.send(f"{leetmsg.upper()}")

@b.command() # help men
async def help(ctx):
    embed=Embed(title=f"GatoBot Commands • {VERSION}", url="https://github.com/gato-services", description="**avatar:** grabs the avatar of a selected user\n **ban:** ban a selected user\n **coinflip/cf:** flip a coin\n **help:** shows this page\n **kick:** kick a selected user\n **leet:** H4[K$ 73$7\n **ping:** gets the delay in ms\n **unban:** unbans a selected user\n **usdtobtc:** watch btc drop\n **version/ver:** gatobot version\n", color=0xc481fb)
    embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/107760692?s=400&u=881e852ca28eacd526e86e51def5fbfcc47f3752&v=4")
    await ctx.send(embed=embed)

@b.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(f"**Avatar of** `{avamember}`")
    await ctx.send(userAvatarUrl)

b.run(TOKEN) # Run bot init
