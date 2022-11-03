import discord
from pochita import *
from apiKeys import * #import all the shit that apikeys.py has

intents = discord.Intents.all()
intents.members=True
nekoThreads={}
pochita = myBot(command_prefix='-', intents=discord.Intents().all())

TOKEN=DISCORD_TOKEN

@pochita.event
async def on_ready(): # This function will notify when the bot is ready on the console
    await pochita.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="SenpaiSuchil"))
    print("pochita is ready!!!!!")
    print("-----------------------------")

@pochita.event
async def on_member_join(member):
    guild = member.guild
    if(guild.system_channel is not None):
        msg=f"Bienvenido: {member.mention} a {guild.name}!!!!"
        await guild.system_channel.send(msg)

@pochita.event
async def on_member_remove(member):
    guild = member.guild
    if(guild.system_channel is not None):
        msg=f"Lastimosamente: {member} acaba de dejar {guild.name} :("
        await guild.system_channel.send(msg)

#--------------------------------- zona de comandos -------------------------------------------

@pochita.command()
async def schedule_start(ctx):
    embed=discord.Embed(title="Recordatorio Activado", description="Se recordará que deben de hacer estiramientos!!!!")
    embed.set_thumbnail(url="https://i.pinimg.com/originals/bd/70/fb/bd70fbdab605d8cd9d4d4a2fb81530de.jpg")
    embed.add_field(name="**Duración:**", value=f"Cada Hora ")
    await ctx.send(embed=embed)
    reminder.start()

@pochita.command()
async def schedule_stop(ctx):
    reminder.stop()
    await ctx.send(f"recordatorio desactivado!!!!!")


@tasks.loop(minutes=1)
async def reminder():
    channel_to_upload_to = pochita.get_channel(997715893079506974)
    for i in range (10):
        await channel_to_upload_to.send("recordatorio activado **@everyone**!!!!!")

pochita.run(TOKEN)