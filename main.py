import discord
import json
from discord.ext import commands
from info import token
from js import newjs, takejs
from fastapi import FastAPI, HTTPException
import uvicorn
import asyncio

app = FastAPI()

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='/',intents=intents)

@bot.event
async def on_ready():
    await print(bot.user)

#Сделать проверку на вшивость(админов)
@bot.command()
async def server_id(ctx):#Поменять команду на регестрацию бота
    try:
        newjs(ctx.guild.name,ctx.guild.id)
        await ctx.send("Your server added")
    except:
        await ctx.send("Server already added")

@app.on_event("startup")
async def start_up():
    asyncio.create_task(bot.start(token))

@app.get('/')
async def ready():
    return {"Bot is working"}

@app.delete('/ban')
async def ban(nickname:str, server_name:str, reason:str | None = None):#в будущем сделать проверку имеет ли пользователь права на сервере
    if (takejs(server_name) == 0):
        return HTTPException(status_code=404,detail="Server not found")
    else:
        id = takejs(server_name)
        guild = bot.get_guild(id)
        member = discord.utils.get(guild.members, name = nickname)
        if member is None:
            raise HTTPException(status_code=404,detail="Member not found")
        if reason is None:
            await member.send(f"You were banned from {server_name}")
            await member.ban()
            return {"member": str(member), "id": str(id), "reason": "None"}
        else:
            await member.send(f"You were banned from {server_name} because {reason}")
            await member.ban(reason=reason)
            return {"member": str(member), "id": str(id), "reason": reason}
# Дописать по уже созданной идеи для json

@app.get('/members/{server_name}')
async def members(server_name:str):
    if takejs(server_name) == 0:
        raise HTTPException(status_code=404,detail="Server not found")
    else:
        id = takejs(server_name)
        guild = bot.get_guild(1069577333629010001)
        members = guild.members
        return {"members": [str(member) for member in members]}

@app.put('/unban')
async def unban(server_name:str, nickname:str):
    if takejs(server_name) == 0:
        raise HTTPException(status_code=404,detail="Server not found")
    else:
        id = takejs(server_name)
        guild = bot.get_guild(id)
        try:
            async for banned_entry in guild.bans():
                    if banned_entry.user.name == nickname:
                        await guild.unban(user=banned_entry.user)
                        return {"member" : [{"nick":banned_entry.user.name, "id":banned_entry.user.id}]}
        except:
            return HTTPException(status_code=404,detail="User not found")
    
@app.get('/ban/{server_name}')
async def bans(server_name:str):
    if takejs(server_name) == 0:
        raise HTTPException(status_code=404,detail="Server not found")
    else:
        ban_members = []
        id = takejs(server_name)
        guild = bot.get_guild(id)
        async for banned_entry in guild.bans():
            ban_members.append({"nickname":banned_entry.user.name,"id":banned_entry.user.id})
        return {f"bans on {server_name}":ban_members}
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__=="__main__":
    run_fastapi()