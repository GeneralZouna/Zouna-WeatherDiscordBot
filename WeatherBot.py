import discord
import asyncio
import requests
import json


#import ForbiddenSymbols as FS
intents = discord.Intents.all()
client = discord.Client(intents=intents)
conf = {}


#config file initilation
try:
    conf = json.load(open("Config.json"))
except Exception as e:
    print(e)
    print("No Config file was found...")
    print("Creating new Config file...")
    conf["Prefix"] = "!"
    conf["Weather-erase-delay"] = 0
    conf["Weather-download-link"] = "http://meteo.arso.gov.si/uploads/probase/www/observ/radar/si0-rm-anim.gif"
    
    conf["Sat-erase-delay"] = 0
    conf["SatLinks"] = ["https://eumetview.eumetsat.int/static-images/latestImages/EUMETSAT_MSG_RGBNatColourEnhncd_CentralEurope.jpg", "https://eumetview.eumetsat.int/static-images/latestImages/EUMETSAT_MSG_H03B_CentralEurope.png"]
    
    conf["Bot-Token"] = 'Input bot token here'
finally:  
    json.dump(conf,open("Config.json","w"),ensure_ascii=False,indent=1)
    print("Config file had been updated")


@client.event
async def on_ready():

    print('We have logged in as {0.user}'.format(client))
    print(client.user.display_name)
    print("This is the Weather & Satellite branch.")


@client.event
async def on_message(message):
            

#radar command
    if message.content.lower().startswith(f"{conf['Prefix']}radar"):
        x = requests.get(conf["Weather-download-link"])
        open("rad.gif", "wb").write(x.content)

        file_send =  discord.File(open("rad.gif", "rb"))
        if conf["Weather-erase-delay"] > 0:
            message.delete(delay=conf["Weather-erase-delay"])
            await message.channel.send(file = file_send, delete_after=conf["Weather-erase-delay"])
        else:
            await message.channel.send(file = file_send)


#satellite command 
    if message.content.lower().startswith(f"{conf['Prefix']}sat"):
        args = message.content.lower().split(" ")

        x = requests.get(conf["SatLinks"][int(args[1])])
        open("Sat.jpg", "wb").write(x.content)
        
        file_send =  discord.File(open("Sat.jpg", "rb"))
        try:
            if conf["Sat-erase-delay"] > 0:
                message.delete(delay=conf["Sat-erase-delay"])
                
                await message.channel.send(file = file_send, delete_after=conf["Sat-erase-delay"])
            else:
                await message.channel.send(file = file_send)
        except:
            await message.channel.send("There is no satellite image with that index")

client.run(conf["Bot-Token"], bot=True)





