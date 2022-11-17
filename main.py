import discord
from tashkent import *
from apiKeys import *
from dataBase import *
import datetime

intents = discord.Intents.all()
intents.members=True
nekoThreads={}
dataBase=myDataBase()
tashkent = myBot(command_prefix='-', intents=discord.Intents().all())

TOKEN=DISCORD_TOKEN

@tashkent.event
async def on_ready():
    await tashkent.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="SenpaiSuchil"))
    print("Tashkent is ready!!!!!")
    print("-----------------------------")

@tashkent.event
async def on_member_join(member):
    guild = member.guild
    if(guild.system_channel is not None):
        msg=f"Bienvenido: {member.mention} a {guild.name}!!!!"
        await guild.system_channel.send(msg)

@tashkent.event
async def on_member_remove(member):
    guild = member.guild
    if(guild.system_channel is not None):
        msg=f"Lastimosamente: {member} acaba de dejar {guild.name} :("
        await guild.system_channel.send(msg)

#--------------------------------- zona de comandos -------------------------------------------

@tashkent.command()
async def schedule_start(ctx):
    author=ctx.message.author
    embed=discord.Embed(title="Recordatorio Activado", description="Se recordará que deben de hacer estiramientos!!!!")
    embed.set_thumbnail(url="https://i.pinimg.com/originals/bd/70/fb/bd70fbdab605d8cd9d4d4a2fb81530de.jpg")
    embed.add_field(name="**Duración:**", value=f"Cada Hora ")
    await ctx.send(embed=embed)
    reminder.start()

@tashkent.command()
async def schedule_stop(ctx):
    reminder.stop()
    await ctx.send(f"recordatorio desactivado!!!!!")

@tashkent.command()
async def saludo(ctx):
    author=ctx.message.author
    user=tashkent.get_user(author.id)
    await user.send("olaaaaaa")


@tashkent.command()
async def set_reminder(ctx):
    time=datetime.datetime.now()
    author=ctx.message.author
    dataBase.insert(str(author.id), f"{time}", 1 )
    await ctx.reply("tu recordatorio se guardó correctamente!")
    dataBase.get()
    pass


@tashkent.command()
async def get(ctx):
    dataBase.get()

    
@tasks.loop(minutes=1)
async def reminder():
    pass


tashkent.run(TOKEN)