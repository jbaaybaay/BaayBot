import json

playerjson = None

def jsonLoad():
	with open("players.json") as f:
		playerjson = json.load(f)
	print(playerjson)

def parseJSON(user,cmd):
	print(playerjson[user][cmd])

#jsonLoad()
with open("players.json") as f:
	playerjson = json.load(f)
parseJSON("Waldo","fireball")
