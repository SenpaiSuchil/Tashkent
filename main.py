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

def embedMaker(title, desc):
    embed=discord.Embed(title=f"{title}", description=f"{desc}")
    embed.set_image(url="https://cdn.discordapp.com/attachments/630553822036623370/683343006757290009/tskt_azurlane200229.gif")
    embed.add_field(name="**Nota:**", value=f"Para desactivarlo escribe en el server -stop_reminder")
    embed.add_field(name="**Duración:**", value=f"Cada Hora durante 8 horas")
    return embed

@tashkent.event
async def on_ready():
    await tashkent.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="SenpaiSuchil"))
    print("Tashkent is ready!!!!!")
    reminder.start()
    print("reminder module activated")
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

#--------------------------------- command zone -------------------------------------------#


@tashkent.command()
async def stop_reminder(ctx):
    author=ctx.message.author
    dataBase.changeStatus(str(author.id), 0)
    embed=embedMaker("Recordatorio Desactivado", "Si deseas volver activar los recordatorios escribe nuevamente en el servidor -set_reminder")
    await ctx.reply(embed=embed)
    pass


@tashkent.command()
async def set_reminder(ctx):
    author=ctx.message.author
    verify=dataBase.verify(author.id)
    if verify==0:
        #if is not in the database
        time=datetime.datetime.now()
        #send the time twice because is the same value the first time
        dataBase.insert(str(author.id), f"{time}", f"{time}", 1 )
        embed=embedMaker("Recordatorio Activado", "Se recordará que deben de hacer estiramientos!!!!" )
        await ctx.send(embed=embed)
        
    if verify==1:
        #if the user is already in the database with an active reminder
        embed=embedMaker("Recordatorio ya activo", "ya tienes un recordatorio activo" )
        await ctx.send(embed=embed)
    if verify==2:
        #if the user is already in the database but not with an active reminder
        embed=embedMaker("Recordatorio Reactivado", "Se a reactivado tu recordatorio!!!" )
        await ctx.send(embed=embed)

#--------------------------------- loops zone -------------------------------------------#
#this loop will check every minute the list of people who activated the reminder checking if and hour has passed or not
@tasks.loop(minutes=1)
async def reminder():
    list=dataBase.get()
    currentDate=datetime.datetime.now()
    for i in list:
        #i[0] -----> last date update
        #i[1] -----> user id
        #i[2] -----> start date

        dateQuery=datetime.datetime.strptime(str(i[0]), "%Y-%m-%d %H:%M:%S")
        startQuery=datetime.datetime.strptime(str(i[2]), "%Y-%m-%d %H:%M:%S")
        delta1=datetime.timedelta(minutes=1)
        delta8=datetime.timedelta(minutes=3)
        user=tashkent.get_user(int(i[1]))
        

        if (currentDate-delta1)>=dateQuery:
            print(f" hora calculada: {dateQuery+delta1} ||||| hora actual: {currentDate}")

            dataBase.changeDate(f"{currentDate}", str(i[1]))
            for j in range(10):
                await user.send("Recordatorio para tomar aire y despejar la vista!!! recuerda hacer tus estiramientos y pararte de la silla!!")
            embed=embedMaker("Hola!!", "Este es un recordatorio para que hagas algunos estiramientos y despejes la vista!!")
            await user.send(embed=embed)
        
        if (currentDate-delta8)>=startQuery:
            
            await user.send("Has trabajado 8 Horas consecutivas, el recordatorio se desactivará automaticamente")
            embed=embedMaker("Han pasado 8 horas!!", "Si deseas volver activar los recordatorios escribe nuevamente en el servidor -set_reminder")
            await user.send(embed=embed)
            dataBase.changeStatus(str(i[1]), 0)

tashkent.run(TOKEN)