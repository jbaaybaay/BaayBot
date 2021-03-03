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
# Initialize Google Sheets Service Account
#gc = gspread.service_account(filename='Tokens/GoogleService.json')

# Designate Command Prefix
bot = commands.Bot(command_prefix='$')

# Discord Bot Token
Discord_TokenFile = open('Tokens/DiscordToken.txt', 'r')
Discord_Token = Discord_TokenFile.read()

# Userdata Sheet ID
#UserDataSheetLinkFile = open('Tokens/UserdataSheet.txt', 'r')
#UserDataSheetLink = UserDataSheetLinkFile.read()
#############################################################################

ID_list, Username_list, Sheet_list = [], [], []
ActiveUsers = []
# Keeps track of who's here for party rolls

# Take in int userID, string cell value (e.g. 'B1'), output CellValue string
#def FindCellValue(userID, cell):
#        global ID_list, Sheet_list
#        CallerID = str(userID)#

#        item = 0
#        for i in ID_list:
#                if i == CallerID:
#                        SheetLink = Sheet_list[item]
#                        break
#                else:
#                    item += 1
#        try:
#                CharacterSheet = gc.open_by_url(SheetLink)
#                CharacterWorksheet = CharacterSheet.get_worksheet(0)
#        except:
#                return ("Error: User Sheet Not Initialized Correctly")#

#        CellValue = CharacterWorksheet.get(cell).first()
#        return CellValue#

#def RefreshUserData():
#        global ID_list, Username_list, Sheet_list
#        
#        UserDataSheet = gc.open_by_key(UserDataSheetLink)
#        UserDataWorksheet = UserDataSheet.worksheet("UserData")#

#        ID_list = UserDataWorksheet.col_values(1)
#        Username_list = UserDataWorksheet.col_values(2)
#        Sheet_list = UserDataWorksheet.col_values(3)
#        return
    

@bot.event
async def on_ready():
        #RefreshUserData()
        print("Baaybot Active")

@bot.command(pass_context=True)
async def here(ctx, *args):
        global ActiveUsers
        if args:
                if ctx.message.mentions:
                        user = ctx.message.mentions[0]
                else:
                        await ctx.send("Invalid User Specified")
        else:
            user = ctx.message.author
        if user.id not in ActiveUsers:
                ActiveUsers.append(user.id)
        return

@bot.command(pass_context=True)
async def nothere(ctx, *args):
        global ActiveUsers
        if args:
                if ctx.message.mentions:
                        user = ctx.message.mentions[0]
                else:
                        await ctx.send("Invalid User Specified")
        else:
            user = ctx.message.author
        if user.id in ActiveUsers:
                ActiveUsers.remove(user.id)
        return

@bot.command(pass_context=True)
async def clearhere(ctx):
        global ActiveUsers
        ActiveUsers = []
        return

@bot.command(pass_context=True)
async def rollcall(ctx):
        rollcall = "ROLLCALL\n"
        global ActiveUsers
        if ActiveUsers:
            for i in ActiveUsers:
                user = bot.get_user(i)
                rollcall += user.mention+" is here!\n"
        else:
            rollcall += "no one is here :("
        await ctx.send(rollcall)


#@bot.command(pass_context=True)
#async def mysheet(ctx, *args):
#    try:
#            CharacterSheet = gc.open_by_url(args[0])
#            CharacterWorksheet = CharacterSheet.get_worksheet(0)
#            ValCheck = CharacterWorksheet.cell(1, 1).value
#            if ValCheck != "Name":
#                await ctx.send("Incorrect Sheet: Please make sure your character sheet is the first worksheet")
#                return
#            
#            UserDataSheet = gc.open_by_key(UserDataSheetLink)
#            UserDataWorksheet = UserDataSheet.worksheet("UserData")#

#            ID_list = UserDataWorksheet.col_values(1)
#            CallerID = str(ctx.message.author.id)
#            row = 1
#            for i in ID_list:
#                if i == CallerID:
#                    # Update Row with new sheet
#                    UsernameCell = 'B'+str(row)
#                    UserDataWorksheet.update(UsernameCell, ctx.message.author.name)
#                    SheetlinkCell = 'C'+str(row)
#                    UserDataWorksheet.update(SheetlinkCell, args[0])
#                    RefreshUserData()
#                    await ctx.send("Sheet Row Updated")
#                    return
#                else:
#                    row += 1#

#            # Create New Row
#            IDCell = 'A'+str(row)
#            UserDataWorksheet.update(IDCell, str(ctx.message.author.id))
#            UsernameCell = 'B'+str(row)
#            UserDataWorksheet.update(UsernameCell, ctx.message.author.name)
#            SheetlinkCell = 'C'+str(row)
#            UserDataWorksheet.update(SheetlinkCell, args[0])
#            RefreshUserData()
#            await ctx.send("New Row Created")
#            return#

#            await ctx.send(row)#

#    except:
#            await ctx.send("Error: Permission or URL Error")
#            return

@bot.command(pass_context=True)
async def rip(ctx):
        await ctx.send(":dean:")

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
async def spot(ctx):
        SpotMod = FindCellValue(ctx.message.author.id, "C78")
        if SpotMod == "Error: User Sheet Not Initialized Correctly":
            await ctx.send(SpotMod)
            return
        rolls, total = PrintRolls("1d20+"+SpotMod)
        user_rolls = "```"+rolls+"```"+ctx.message.author.mention+" rolled: **"+str(total)+"** on **Spot**."
        await ctx.send(user_rolls)

@bot.command(pass_context=True)
async def listen(ctx):
        ListenMod = FindCellValue(ctx.message.author.id, "C68")
        if ListenMod == "Error: User Sheet Not Initialized Correctly":
            await ctx.send(ListenMod)
            return
        rolls, total = PrintRolls("1d20+"+ListenMod)
        user_rolls = "```"+rolls+"```"+ctx.message.author.mention+" rolled: **"+str(total)+"** on **Listen**."
        await ctx.send(user_rolls)

@bot.command(pass_context=True)
async def init(ctx):
        InitMod = FindCellValue(ctx.message.author.id, "C25")
        if InitMod == "Error: User Sheet Not Initialized Correctly":
            await ctx.send(InitMod)
            return
        rolls, total = PrintRolls("1d20+"+InitMod)
        user_rolls = "```"+rolls+"```"+ctx.message.author.mention+" rolled: **"+str(total)+"** on **Initiative**."
        await ctx.send(user_rolls)

bot.run(Discord_Token)
