import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import re
import urllib.request
import json
from bs4 import BeautifulSoup
import gspread
from DiceRoll import *
from WebParser import *

###########################INITIALIZATION VARIABLES###########################
# Designate Command Prefix
bot = commands.Bot(command_prefix='$')

# Discord Bot Token
Discord_TokenFile = open('Tokens/DiscordToken.txt', 'r')
Discord_Token = Discord_TokenFile.read()
#############################################################################

@bot.event
async def on_ready():
        print("Baaybot Active")

@bot.command(pass_context=True)
async def rip(ctx):
        await ctx.send(":dean:")

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
                await ctx.send(total)
                return
        except OSError: # If that's not a valid page, we will attempt another site via google search
                await ctx.send('Starting search...')
        except:
                await ctx.send('Well I tried but its all fucked bro')

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
                    await ctx.send(PrintPageArk(j))
                    break
                if j.__contains__("d20srd.org"):
                    print(j)
                    indic = True
                    await ctx.send(PrintPageD(j))
                    break
            if indic == True:
                break
            query = URLend + " dnd 3.5"

@bot.command(pass_context=True)
async def gurps(ctx, *args):
        username = ctx.message.author.mention
        if not args[0].isnumeric():
            await ctx.send("Error: Incorrect Input Format")
        await ctx.send(username+GurpsRoll(int(args[0])))

@bot.command(pass_context=True)
async def roll(ctx, *args):
        username = ctx.message.author.mention
        rolls, total = PrintRolls("".join(args))
        user_rolls = "```"+rolls+"```"+username+" rolled: **"+str(total)+"**."
        await ctx.send(user_rolls)

@bot.command(pass_context=True)
async def me(ctx, *args):
        with open('Characters/UserNameToCharacterName.json','r') as jsonFile:
            usernames = jsonFile.read().replace('\n','')
        usernameDict = json.loads(usernames)
        if not ctx.message.author.name in usernameDict.keys():
            await ctx.send(ctx.message.author.mention+" No character found for your username")
            return
        cleanArgs = "".join(args).replace(" ","").lower()
        if not cleanArgs:
            await ctx.send(ctx.message.author.mention+" "+usernameDict[ctx.message.author.name])
            return
        if '+' in cleanArgs:
            valPlusMod = cleanArgs.split('+')
            value = valPlusMod[0]
            modifier = "d20+"+valPlusMod[1]
        elif '-' in cleanArgs:
            valPlusMod = cleanArgs.split('-')
            value = valPlusMod[0]
            modifier = "d20-"+valPlusMod[1]
        else:
            value = cleanArgs
            modifier = "d20"
        characterFile = usernameDict[ctx.message.author.name]+".json"
        with open('Characters/'+characterFile,'r') as characterJsonFile:
            characterValues = characterJsonFile.read().replace('\n','')
        characterDict = json.loads(characterValues)
        if not value in characterDict.keys():
            await ctx.send(ctx.message.author.mention+" Value "+value+" does not appear in "+characterFile)
            return
        valueString = characterDict[value]
        if valueString[0] == '-':
            modifier += valueString
        elif valueString[0] == '+':
            modifier += valueString
        else:
            modifier += ('+'+valueString)
        rolls, total = PrintRolls(modifier)
        user_rolls = "```"+rolls+"```"+ctx.message.author.mention+" rolled: **"+str(total)+"**."
        await ctx.send(user_rolls)

bot.run(Discord_Token)
