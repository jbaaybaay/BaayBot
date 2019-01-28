import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import re
import urllib.request
from bs4 import BeautifulSoup

EncounterSwitch = False
NumGrant = 2
Ungranted = ['Leading The Attack', 'Charging Minotaur', 'White Raven Tactics', 'Revitalizing Strike', 'Defensive Rebuke']
Granted = []
Expended = []

bot = commands.Bot(command_prefix='$')

class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"

# Both these sources have different HTML formats so i need to parse them differently
# Ark throws everything into one HTML section while d20 just puts it in all different places
# Both are nightmares, I like therafim better

def PrintPageArk(URL):
        
        opener = AppURLopener()
                    
        page = opener.open(URL)
        soup = BeautifulSoup(page, "html.parser")

        content = soup.find('div', attrs={'id': 'content'})
        print(content)
        content = content.text.strip()
        content = content.replace('\n\n', '\n')
        content = content[:2000] + (content[2000:] and '..')

        return content

def PrintPageD(URL):
        
        opener = AppURLopener()
                    
        page = opener.open(URL)
        soup = BeautifulSoup(page, "html.parser")

        title = soup.find('h1')
        title = title.text.strip()

        stitle = soup.find('h4')
        stitle = stitle.text.strip()

        table = soup.find('table', attrs={'class': 'statBlock'})
        table = table.text.strip()
        table = table.replace('\n\n\n', '\r')
        table = table.replace('\n', ' ')

        desc = soup.findAll('p')

        descp = ''
        
        for para in desc:
                para = para.text.strip()
                if para.__contains__("Hypertext"):
                        break
                descp += '\n' + para + '\n'

        total = title + '\n' + stitle + '\n' + table + '\n' + descp

        return total



@bot.event
async def on_ready():
	print ("Baaybot Active")

@bot.command(pass_context=True)
async def cru(ctx):
        global EncounterSwitch
        if EncounterSwitch == True:
                await bot.say("Already in a current encounter")
                return

        global CrUser

        CrUser = ctx.message.author

        EncounterSwitch = True
        output = "Welcome to Baay Crusader Logic {0.author.mention} \nUse the functions $turn, $use, and $rec to proceed and don't forget to $clear after the encounter.  Only one can use!".format(ctx.message)
        await bot.say(output)
        i = 0
        global NumGrant
        global Ungranted
        global Granted
        global Expended
        while i < NumGrant:
            which = random.randint(0, (len(Ungranted)-1))
            Granted.append(Ungranted[which])
            Ungranted.pop(which)
            i += 1
            await bot.say(str(Granted[len(Granted)-1] + " Granted"))

@bot.command(pass_context=True)
async def rip(ctx):
        await bot.say(":dean:")

##@bot.command(pass_context=True)
##async def roll(ctx, *args):
##        #assume xdy
##        die = args[0].split("d")
##        for i in range(int(die[0])):
##                roll[i] = random.randint(1, int(die[1]))
##                total += roll[i]
##
##        await bot.say(roll)


@bot.command(pass_context=True)
async def man(ctx):

        global EncounterSwitch
        
        if EncounterSwitch == False:
                await bot.say("Not in an encounter currently")
                return
        
        global Ungranted
        global Granted
        global Expended
        output = "Maneuvers Granted: \n"
        i = 0
        while i < len(Granted):
                i += 1
                output += str(i) + ". " + str(Granted[i-1]) + "\n"

        output += ("Maneuvers Expended: \n")
        i = 0
        while i < len(Expended):
                i += 1
                output += str(i) + ". " + str(Expended[i-1]) + "\n"

        await bot.say(output)

@bot.command(pass_context=True)
async def turn(ctx):

        global EncounterSwitch
        
        if EncounterSwitch == False:
                await bot.say("Not in an encounter currently")
                return
        
        global CrUser
        global Ungranted
        global Granted

        if CrUser != ctx.message.author:
                await bot.say("Crusader Denied")
                return
        
        if len(Ungranted) > 0:
                which = random.randint(0, (len(Ungranted)-1))
                Granted.append(Ungranted[which])
                Ungranted.pop(which)
                await bot.say(str(Granted[len(Granted)-1] + " Granted"))

@bot.command(pass_context=True)
async def use(ctx, select:int):

        global EncounterSwitch
        
        if EncounterSwitch == False:
                await bot.say("Not in an encounter currently")
                return
        
        global Granted
        global Expended
        global CrUser

        if CrUser != ctx.message.author:
                await bot.say("Crusader Denied")
                return
        
        if select <= len(Granted) and select > 0:
                x = select - 1
                await bot.say("Used " + Granted[x])
                Expended.append(Granted[x])
                Granted.pop(x)


@bot.command(pass_context=True)
async def rec(ctx):

        global EncounterSwitch
        
        if EncounterSwitch == False:
                await bot.say("Not in an encounter currently")
                return
        
        global CrUser

        if CrUser != ctx.message.author:
                await bot.say("Crusader Denied")
                return
        
        global Granted
        global Expended
        await bot.say("Granted Maneuvers Recovered")
        Granted.extend(Expended)
        Expended.clear()

@bot.command(pass_context=True)
async def clear(ctx):

        global EncounterSwitch
        
        if EncounterSwitch == False:
                await bot.say("Not in an encounter currently")
                return

        global CrUser

        if CrUser != ctx.message.author:
                await bot.say("Crusader Denied")
                return
        
        global Granted
        global Expended
        global Ungranted

        Ungranted = ['Leading The Attack', 'Charging Minotaur', 'White Raven Tactics', 'Revitalizing Strike', 'Defensive Rebuke']
        Granted = []
        Expended = []
        EncounterSwitch = False

# Haven't successfully implemented voice features yet

##@bot.command(pass_context=True)
##async def join(ctx):
##        channel = ctx.message.author.voice.voice_channel
##        await bot.join_voice_channel(channel)
##
##@bot.command(pass_context=True)
##async def leave(ctx):
##        server = ctx.message.server
##        voice_client = bot.voice_client_in(server)
##        await voice_client.disconnect()

# Search for a spell/maneuver/etc within a few different sites

@bot.command(pass_context=True)
async def search(ctx, *args):


        URLend = '-'.join(args)

        URL = "http://therafimrpg.wikidot.com/" + URLend

        # Plug the search term directly into therafim's URL format

        try:

                page = urllib.request.urlopen(URL)
                soup = BeautifulSoup(page, "html.parser")

                title = soup.find('div', attrs={'id': 'page-title'})
                titlep = title.text.strip() 

                content = soup.find('div', attrs={'id': 'page-content'})
                contentp = content.text.strip()

                total = titlep + "\n" + contentp
                total = total[:2000] + (total[2000:] and '..')
                
                await bot.say(total)

                return
    
        except OSError:

                # If that's not a valid page, we will attempt another site via google search
                
                await bot.say('Starting search...')

        except:

                await bot.say('Well I tried but its all fucked bro')
                

        class AppURLopener(urllib.request.FancyURLopener):
                version = "Mozilla/5.0"

        try: 
                from googlesearch import search 

        except ImportError:  
                print("No module named 'google' found")

        indic = False

        query = " ".join(args)

        for k in range(2):
            
            for j in search(query, num=10, stop=1, pause=2): 
                if j.__contains__("dnd.arkalseif.info"):

                    indic = True
                    
                    await bot.say(PrintPageArk(j))

                    break
                    
                if j.__contains__("d20srd.org"):
                    print(j)
                    indic = True

                    await bot.say(PrintPageD(j))
                    
                    break

            if indic == True:
                break
            
            query = URLend + " dnd 3.5"



    
bot.run(*TOKEN*)
