import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

# CONNECT TO DISCORD
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

# DECLARE LISTS FOR VOICE CHANNELS STATUS
vch_stat_id = []
vch_stat_mem = []

vc_main = os.getenv('MAIN_VC')


# THIS FUNCTION FILLS UP THE DECLARED LISTS WITH ALL VOICE CHANNELS INFO
def vc_refresh():
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            id_channel = channel.id
            channel = bot.get_channel(id_channel)
            vch_stat_id.append(id_channel)
            mem_count = 0
            for member in channel.members:
                mem_count = mem_count + 1
            vch_stat_mem.append(mem_count)


# PING COMMAND
@bot.command(name='ping', help='Responds with pong if it is running')
async def ping(ctx):
    await ctx.send('pong')


# WHEN THE BOT IS CONNECTED TO DISCORD AND READY THIS TRIGGERS
@bot.event
async def on_ready():
    vc_refresh()

# WHEN ANYTHING HAPPENS IN VOICE CHANNELS THIS TRIGGERS
# BEFORE AND AFTER CONTAIN NUMBERS OF MEMBER OF THE CURRENT VC IT IS ITERATING
# AFTER IT LOOPS IT WILL REFILL THE VOICE CHANNEL STATUS LISTS IN CASE NUMBER OF MEMBERS OR CHANNELS CHANGED
@bot.event
async def on_voice_state_update(member, before, after):
    iteration = 0
    for i in vch_stat_id:
        before = vch_stat_mem[iteration]
        channel = bot.get_channel(i)
        mem_count = 0
        for member in channel.members:
            mem_count = mem_count + 1
        after = mem_count
        if after != 0 and len(vch_stat_mem) == iteration + 1:
            await channel.clone()
        if before != 0 and after == 0 and i != vc_main:
            await channel.delete()
        iteration = iteration + 1
    vch_stat_id.clear()
    vch_stat_mem.clear()
    vc_refresh()

# RUN THE BOT
bot.run(TOKEN)
