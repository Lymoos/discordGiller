#БОТ ЛЕЖИТ НА СЕРВЕРЕ
#БУДТЕ АККУРАТНЕЕ С ЭТИМ ФАЙЛОВ
#СОЗДАТЕЛЬ: ШЕСТАКОВ МАКСИМ(LYMOOS)
import discord
import json
from discord.ext import commands, tasks
from discord import app_commands
from info import token, host, version
from js import newjs, takejs, takejsN
from fastapi import FastAPI, HTTPException
import uvicorn
import asyncio
from discord.ext.commands import has_permissions, CheckFailure

app = FastAPI()

intents = discord.Intents.all()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='/',intents=intents)
#tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await print("#########--BOT_WORKING_NORMALY--#########")

@bot.command()
@commands.has_permissions(ban_members=True)
async def gban(ctx, member: discord.Member, *, reason=None):
    try:
        if reason is None:
            await member.ban()  
            await member.send(f"You were banned from {ctx.guild.name}")
            print(f"Successfully banned {member.name} ({member.id})")
        else:
            await member.ban(reason=reason)
            await member.send(f"You were banned from {ctx.guild.name} because {reason}")
            print(f"Successfully banned {member.name} ({member.id})")
    except discord.Forbidden:
        print(f"Could not send message to {member.name} after ban due to privacy settings")
    except Exception as e:
        print(f"An error occurred while banning the member: {e}")
        msg = await ctx.send("An error occurred while banning the member.")
    else:
        await ctx.message.delete()
        await msg.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def gkick(ctx, member, *, reason=None):
    if reason is None:
        await member.send(f"You were kicked from {ctx.guild.name}")
        await member.kick()
    else:
        await member.send(f"You were kicked from {ctx.guild.name} because {reason}")
        await member.kick(reason=reason)
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban_all(ctx):
    for member in ctx.guild.members:
        try:
            await member.ban()
            await ctx.send(f"Successfully banned {member.name} by {ctx.author.name}")
        except:
            pass
    await ctx.message.delete()
#Сделать проверку на вшивость(админов)
@bot.command()
@commands.has_permissions(administrator=True)
async def connect(ctx):#Поменять команду на регестрацию бота
    squad = takejs(ctx.guild.name)
    if(squad["id"] == 0):
        newjs(ctx.guild.name,ctx.guild.id)
        msg = await ctx.send("Your server added")
        await asyncio.sleep(1)
        await msg.delete()
        await ctx.message.delete()
    else:
        msg = await ctx.send("Server already added")
        await asyncio.sleep(1)
        await msg.delete()
        await ctx.message.delete()

@connect.error
async def connect_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        msg = await ctx.send("You don't have permission")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await msg.delete()

@bot.hybrid_command()
@commands.has_permissions(administrator=True)
async def gconnect(ctx):
    squad = takejs(ctx.guild.name)
    if(squad["id"] == 0):
        newjs(ctx.guild.name,ctx.guild.id)
        msg = await ctx.send("Your server added")
        await asyncio.sleep(1)
        await msg.delete()
        await ctx.message.delete()
    else:
        msg = await ctx.send("Server already added")
        await asyncio.sleep(1)
        await msg.delete()
        await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def settings_voice_name(ctx):
    if(takejs(ctx.guild.name)["voice_mod"]["voice_name"] == "None"):
        print("Maybe later")

@bot.event
async def on_voice_state_update(member: discord.Member, before, after):
    if after.channel is not None:
        if after.channel.name == '[+]Создать канал':  
             for guild in bot.guilds:
                 if(guild.id == after.channel.guild.id):
                    maincategory = discord.utils.get(guild.categories, name='Voice') 
                    if maincategory is not None:  # Проверка, что категория найдена
                        channel2 = await guild.create_voice_channel(f'Канал {member.name}', category=maincategory)
                        await member.move_to(channel2)
                    else:
                        ...
                    if before.channel is not None and before.channel.category.name == 'Voice':
                            if len(before.channel.members) == 0 and before.channel != after.channel:
                                await before.channel.delete()
    elif before.channel is not None and before.channel.category.name == 'Voice':  # Проверка, что пользователь отключился от голосового канала
        if len(before.channel.members) == 0:  # Проверка, что в канале нет пользователей
            if before.channel.name != '[+]Создать канал':  # Проверка, что канал не является каналом '+создать канал'
                await before.channel.delete()
    if before.channel is not None and before.channel.category.name == 'Voice':  
        if len(before.channel.members) == 0:  
            if before.channel.name != '[+]Создать канал':  
                await before.channel.delete()

@app.on_event("startup")
async def start_up():
    asyncio.create_task(bot.start(token))

@app.get('/')
async def ready():
     return {"BOT":[{"version": version, "stable": "yes", "bot": bot.user.name}], "API":"ONLINE"}

@app.delete('/ban')#ENDED
async def ban(nickname:str, server_name:str, reason:str = None):#в будущем сделать проверку имеет ли пользователь права на сервере
    if (takejs(server_name) == 0):
        return HTTPException(status_code=404,detail="Server not found")
    else:
        id = takejs(server_name)
        guild = bot.get_guild(id["id"])
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

@app.get('/members/{server_name}')#ENDED
async def members(server_name:str):
    squad = takejs(server_name)
    if squad["id"] == 0:
        raise HTTPException(status_code=404,detail="Server not found")
    else:
        guild = bot.get_guild(squad["id"])
        members = guild.members
        return {"members": [str(member) for member in members]}

@app.get('/squads')#ENDED
async def squads():
    try:
        squads = takejsN()
        return {"Squads": [squads]}
    except:
        return HTTPException(status_code=500,detail="DATA.JSON ERROR")

@app.put('/unban')#ENDED
async def unban(server_name:str, nickname:str):
    squad = takejs(server_name)
    if squad["id"] == 0:
        raise HTTPException(status_code=404,detail="Server not found")
    else:
        guild = bot.get_guild(squad["id"])
        try:
            async for banned_entry in guild.bans():
                    if banned_entry.user.name == nickname:
                        await guild.unban(user=banned_entry.user)
                        return {"member" : [{"nick":banned_entry.user.name, "id":banned_entry.user.id}]}
        except:
            return HTTPException(status_code=404,detail="User not found")
    
@app.get('/ban/{server_name}')
async def bans(server_name:str):
    squad = takejs(server_name)
    if takejs(squad["id"]) == 0:
        raise HTTPException(status_code=404,detail="Server not found")
    else:
        try:
            ban_members = []
            guild = bot.get_guild(squad["id"])
            async for banned_entry in guild.bans():
                ban_members.append({"nickname":banned_entry.user.name,"id":banned_entry.user.id, "reason":banned_entry.reason})
            return {f"bans on {server_name}":ban_members}
        except:
            return HTTPException(status_code=500,detail="DATA.JSON ERROR")
    

def run_fastapi():
    uvicorn.run(app, host=host, port=80)

if __name__=="__main__":
    run_fastapi()