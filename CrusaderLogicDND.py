import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random

EncounterSwitch = False
NumGrant = 2
Ungranted = ['Leading The Attack', 'Charging Minotaur', 'White Raven Tactics', 'Revitalizing Strike', 'Defensive Rebuke']
Granted = []
Expended = []

bot = commands.Bot(command_prefix='$')

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
##async def change(ctx, new: int):
##        await bot.say("Changing Spellcraft to {}".format(new))
##        Spellcraft = new
##        await bot.say("The Spellcraft value is " + str(Spellcraft))
##
##@bot.command(pass_context=True)
##async def spellcraft(ctx):
##        await bot.say("The Spellcraft value is " + str(Spellcraft))
##
##@bot.command(pass_context=True)
##async def FoxCunning(ctx):
##        check = FCcheck - Spellcraft - random.randint(1,20)
##        if check < 0:
##                await bot.say("Fox's Cunning Persisted, success by " + str(-check))
##        else:
##                await bot.say("Persist Failed, failure by " + str(check))

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
    
bot.run("*TOKEN*")
