import discord
from discord.ext import commands
from info import token
from js import newjs
from fastapi import FastAPI
import uvicorn
import asyncio

app = FastAPI()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    await print(bot.user)

#Сделать проверку на вшивость(админов)
@bot.command()
async def server_id(ctx):
    await ctx.send(newjs(ctx.guild.name,ctx.guild.id))

@app.on_event("startup")
async def start_up():
    asyncio.create_task(bot.start(token))

@app.get('/')
async def ready():
    return {"client": str(bot.user)}

#@app.delete('/bann/{nickname}')
#async def ban(nickname:str):
#    guild = bot.get_guild()
# Дописать по уже созданной идеи для json
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__=="__main__":
    run_fastapi()