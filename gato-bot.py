#   /$$$$$$              /$$               /$$$$$$$              /$$     
#  /$$__  $$            | $$              | $$__  $$            | $$     
# | $$  \__/  /$$$$$$  /$$$$$$    /$$$$$$ | $$  \ $$  /$$$$$$  /$$$$$$   
# | $$ /$$$$ |____  $$|_  $$_/   /$$__  $$| $$$$$$$  /$$__  $$|_  $$_/   
# | $$|_  $$  /$$$$$$$  | $$    | $$  \ $$| $$__  $$| $$  \ $$  | $$     
# | $$  \ $$ /$$__  $$  | $$ /$$| $$  | $$| $$  \ $$| $$  | $$  | $$ /$$ 
# |  $$$$$$/|  $$$$$$$  |  $$$$/|  $$$$$$/| $$$$$$$/|  $$$$$$/  |  $$$$/  
#  \______/  \_______/   \___/   \______/ |_______/  \______/    \___/    
#

# Imports
from discord import Client, Activity, ActivityType, Embed, Member, HTTPException
from discord.ext import commands
from datetime import datetime

import asyncio, time, os, requests, random

import tkinter
root = tkinter.Tk()
root.withdraw()

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
VERSION = os.getenv("VERSION")

purple_dark= 0x6a006a # Colours
purple_medium= 0xa958a5
purple_light= 0xc481fb
orange= 0xffa500
gold= 0xdaa520
red_dark= 8e2430
red_light= 0xf94343
blue_dark= 0x3b5998
cyan= 0x5780cd
blue_light= 0xace9e7
aqua= 0x33a1ee
pink= 0xff9dbb
green_dark= 0x2ac075
green_light= 0xa1ee33
white= 0xf9f9f6
cream= 0xffdab9

client = Client() # Grab token from .env, command prefix and activity
b = commands.Bot(
    command_prefix = '!',
    activity = Activity(type=ActivityType.watching, name="commits @ github.com/64x2/gato-bot-public")
)

@b.event # Startup Print
async def on_ready():
    print(
        """  ________        __        __________        __    \n"""
        """ /  _____/_____ _/  |_  ____\______   \ _____/  |_  \n"""
        """/   \  ___\__  \\   __\/  _ \|    |  _//  _ \   __\ \n"""
        """\    \_\  \/ __ \|  | (  <_> )    |   (  <_> )  |   \n"""
        """ \______  (____  /__|  \____/|______  /\____/|__|   \n"""
        """        \/     \/                   \/              \n"""
        """                                                    \n"""
        f"""Welcome to GatoBot {VERSION} by Xofo & Invy55. Avaliable at github.com/64x2/gato-bot-public\n"""
    )

@b.command(pass_context=True) # Ping/Latency command
async def ping(ctx):
    time_1 = time.perf_counter()
    await ctx.trigger_typing()
    time_2 = time.perf_counter()
    ping = round((time_2-time_1)*1000)
    await ctx.send(f"Pong! Gato-bot currently has a ping of {ping}ms")

@b.command() # Grabs current version
async def version(ctx):
    embed=Embed(title=f"Gato-bot.py {VERSION}", url="https://github.com/64x2/gato-bot", description="Gato-bot.py is property of Xofo LLC. Unauthorized use and/or abuse of Xofo LLC property isn't nice :(", color=800080)
    await ctx.send(embed=embed)
    print("Command Version was used")

@b.command() # Coinflip
async def coinflip(ctx):
    lista = ['head', 'tails']
    coin = random.choice(lista)
    try:
        if coin == 'head':
            embed= Embed(color= orange, title="Head",timestamp=datetime.utcfromtimestamp(time.time()))
            embed.set_thumbnail(url="https://webstockreview.net/images/coin-clipart-dime-6.png")
            embed.set_footer(text=f" GatoBot {VERSION}")
            await ctx.send(embed=embed)
        else:
            embed= Embed(color= orange, title="Tails",timestamp=datetime.utcfromtimestamp(time.time()))
            embed.set_thumbnail(url="https://www.nicepng.com/png/full/146-1464848_quarter-tail-png-tails-on-a-coin.png")
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
                embed = Embed(color= orange, title="USD -> BTC", description=f"USD: {num}\n BTC: {final}", timestamp=datetime.utcfromtimestamp(time.time()))
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
            embed= Embed(color= green_dark, title="1337 Haxor", description=f"{leetmsg.upper()}", timestamp=datetime.utcfromtimestamp(time.time()))
            embed.set_thumbnail(url="https://i.imgur.com/TR2cv3C.jpg")
            embed.set_footer(text=f" GatoBot {VERSION}")
            await ctx.send(embed=embed)
        except HTTPException:
            await ctx.send(f"{leetmsg.upper()}")
            
@b.command() # Free Nitro !!!!!!
@commands.has_permissions(mention_everyone=True)
async def nitro(ctx):
    await ctx.send("@everyone Free Discord Nitro AirDrop from Steam! https://steams-discord.ru/airdrop")

b.run(TOKEN) # Run bot init
