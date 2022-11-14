import discord
from ducky import *
from apiKeys import *
from dataBase import *
import datetime

intents = discord.Intents.all()
intents.members=True
nekoThreads={}
dataBase=myDataBase()
ducky = myBot(command_prefix='-', intents=discord.Intents().all())

TOKEN=DISCORD_TOKEN

@ducky.event
async def on_ready():
    await ducky.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="SenpaiSuchil"))
    print("rubber ducky is ready!!!!!")
    print("-----------------------------")

@ducky.event
async def on_member_join(member):
    guild = member.guild
    if(guild.system_channel is not None):
        msg=f"Bienvenido: {member.mention} a {guild.name}!!!!"
        await guild.system_channel.send(msg)

@ducky.event
async def on_member_remove(member):
    guild = member.guild
    if(guild.system_channel is not None):
        msg=f"Lastimosamente: {member} acaba de dejar {guild.name} :("
        await guild.system_channel.send(msg)

#--------------------------------- zona de comandos -------------------------------------------

@ducky.command()
async def schedule_start(ctx):
    author=ctx.message.author
    embed=discord.Embed(title="Recordatorio Activado", description="Se recordará que deben de hacer estiramientos!!!!")
    embed.set_thumbnail(url="https://i.pinimg.com/originals/bd/70/fb/bd70fbdab605d8cd9d4d4a2fb81530de.jpg")
    embed.add_field(name="**Duración:**", value=f"Cada Hora ")
    await ctx.send(embed=embed)
    reminder.start()

@ducky.command()
async def schedule_stop(ctx):
    reminder.stop()
    await ctx.send(f"recordatorio desactivado!!!!!")

@ducky.command()
async def saludo(ctx):
    author=ctx.message.author
    user=ducky.get_user(author.id)
    await user.send("olaaaaaa")


@ducky.command()
async def set_reminder(ctx):
    time=datetime.datetime.now()
    author=ctx.message.author
    dataBase.insert(str(author.id), f"{time}", 1 )
    await ctx.reply("tu recordatorio se guardó correctamente!")
    dataBase.get()
    pass

@tasks.loop(minutes=1)
async def reminder():
    pass


ducky.run(TOKEN)