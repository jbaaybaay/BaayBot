BaayBot is a discord bot designed to facilitate tabletop gaming over discord, it was written for D&D 3.X but I guess you can use it for other systems if you want

$roll
	- rolls dice, input should be given as a comma separated list, case insensitive
	- Example: '$roll d20 + 10,d20 + 5,4d6 + 4,4d6 + 4'

$search <NAME>
	- Search for NAME on therafirmrpg, prints out spell/maneuver descriptions, finnicky  
	- Example: '$search fireball'

$rip
	- rip the boi
	
$mysheet <SHEETLINK>
	- Adds SHEETLINK to centralized google sheet under your discord ID and username
	- If you already have an entry in the centralized google sheet, it replaces the google sheet with SHEETLINK
	
$spot, $listen, $init
	- Pulls from your initialized sheet to return a d20 + modifier roll (requires $mysheet initialization first)
	
$here
	- Adds your name to the active users list for the discord session
	
$here <Mentioned user>
	- Add the user to the active users list for the discord session
	- Example: '$here @JBaay'
	
$nothere
	- Removes your name from the active users list for the discord session
	
$nothere <Mentioned user>
	- Removes the user from the active users list for the discord session
	- Example: '$nothere @JBaay'

$clearhere
	- Removes all users from the actives users list for the discord session
	
$rollcall
	- Shabooya
