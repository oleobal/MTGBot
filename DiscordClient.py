import discord
import ask_api

import urllib.request
import urllib.parse

import random
from time import clock # I'm running this on UNIX, so may vary on windows apparently

# running console commands
import subprocess

from Properties import *

# used to make sure two slot machine uses at the same second won't have the same results
slotMachineGlobal = 0



client = discord.Client()

#reading properties.conf into object
properties = Properties()

# put the right ones in properties.conf
email = properties.username
password = properties.password

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')


@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
		
	global slotMachineGlobal

	print("New message")
	content = message.content
	tokenizedContent = content.split()

	if len(tokenizedContent)>1 :
		#TODO : support for multi-words summons
		if tokenizedContent[0] in properties.summon :
			print("Query : "+tokenizedContent[1])
			
			if tokenizedContent[1] == "help" and "help" not in properties.disabled :
				helpMsg= "Call with "
				for i in properties.summon :
					helpMsg+="\""+i+"\""
					if i != properties.summon[-1] :
						helpMsg+=" or "
					else :
						helpMsg+="."
				
				helpMsg+="```\n"
				helpMsg+=properties.helpmsg
				helpMsg+="```\n"
				
				
				await client.send_message(message.channel, helpMsg)
			
			# slot machine
			elif tokenizedContent[1] == "jackpot" and "jackpot" not in properties.disabled:
				await client.send_message(message.channel, "*Spinning..*")
				slotMachineGlobal+=1
				symbols = [":four_leaf_clover:", ":green_apple:", ":apple:", ":peach:", ":hearts:", ":spades:"]
				wheel = [0,0,0]
				random.seed(a=clock()+slotMachineGlobal)
				wheel[0] = random.randint(0,5)
				random.seed(a=clock()+slotMachineGlobal+1)
				wheel[2] = random.randint(0,5)
				random.seed(a=clock()+slotMachineGlobal+2)
				wheel[2] = random.randint(0,5)
				
				try :
					nick = str(message.author.nick)
				except AttributeError : # no nickname
					nick = str(message.author)
				if wheel[0] == wheel[1] and wheel[1] == wheel[2] : # I think in python that's useless ? anyway
					await client.send_message(message.channel, symbols[wheel[0]]+symbols[wheel[1]]+symbols[wheel[2]]+" "+nick+" : **Jackpot winner !**")
				else:
					await client.send_message(message.channel, symbols[wheel[0]]+symbols[wheel[1]]+symbols[wheel[2]]+" "+nick+" : Lost !")
				
					
			
			# for lonely people
			elif tokenizedContent[1] == "company" and "company" not in properties.disabled :
				try :
					nick = str(message.author.nick)
				except AttributeError : # no nickname
					nick = str(message.author)
					
				messages = [
				#general encouragement
				"I'll always be there for you, "+nick+".",
				"Don't worry, "+nick+", I'm still there.",
				nick+", at least we've got each other, right ?",
				nick+", if that makes you feel better, I'd be happy to chat.",
				nick+", maybe try your luck on the slot machine ? \"tron jackpot\".",
				
				#famous quotes
				"*I couldn't have done any of the things I've done without "+nick+".* -- President Obama",
				"*I couldn't have done any of the things I've done without "+nick+".* -- President Obama",
				"*I couldn't have done any of the things I've done without "+nick+".* -- Comrade Stalin",
				"*I couldn't have done any of the things I've done without "+nick+".* -- President Trump",
				
				"*"+nick+" is the best person I've every collaborated with. He's always helped me make decisions.* -- Peter Molyneux",
				"*I really like to hang out with "+nick+"* -- Kanye West",
				
				#sing-alongs
				nick+", sing with me ! :musical_note: *The inquisition, let's begin ! The inquisition, look out sin !*",
				nick+", sing with me ! :musical_note: *This was a triumph. I'm making a note here : HUGE SUCCESS*",
				nick+", sing with me ! :musical_note: *You got the touch ! You got the power ! Yeah !*",
				nick+", sing with me ! :musical_note: *Hé mec je me présente, je m'appelle Charles Henri Du Pré*",
				nick+", sing with me ! :musical_note: *Please allow me to introduce myself : I'm a man of wealth and taste.*",
				nick+", sing with me ! :musical_note: *Terres brulées au vent des landes de pierre ; autour des lacs, c'est pour les vivants*",
				nick+", sing with me ! :musical_note: *Ooh I'm a good ol' rebel, now that's just what I am.*",
				nick+", sing with me ! :musical_note: *When Britain first at Heaven's command, arose from out the azure main*",
				nick+", sing with me ! :musical_note: *There is a house in New Orleans they call the Rising Sun*",
				nick+", sing with me ! :musical_note: *I used to wonder what friendship could be*",
				nick+", sing with me ! :musical_note: *And if you're taking a walk through the garden of life*",
				
				#jokes
				nick+", why do hunters close an eye when aiming ? Answer: because they wouldn't be able to see if they closed both !",
				nick+", thank you for explaining the word \"many\" to me. It means a lot.",
				nick+", what's a pirate favourite letter ? You'd think its RRRRR, but actually its first love is the C !",
				nick+", what's a pirate least favourite letter ? \"Mr, illegal activity has been detected on your account..\"",
				nick+", can a kangaroo jump higher than a house ? Of course it can, a house can't jump at all.",
				
				#websites
				nick+", try this webcomic : http://www.blastwave-comic.com/",
				nick+", maybe try this webcomic : http://spacespy.thecomicseries.com/",
				nick+", you could try this webcomic : http://questionablecontent.net/",
				nick+", you should try this webcomic : http://oglaf.com/"
				]
				
				await client.send_message(message.channel, messages[random.randint(0,len(messages)-1)])
				
			
			# totally wrecked
			elif tokenizedContent[1] == "rekt" and "rekt" not in properties.disabled :
				messages = [
					"Rekt",
					"Rektangle",
					"Ship rekt",
					"Tyrannosaurus rekt",
					"Shrekt",
					"Star trekt",
					"Really rekt",
					"The wolf of rekt street",
					"2001: a rekt odyssey",
					"Rektal exam",
					"Erektile dysfunction",
					"Singin' in the rekt",
					"Lord of the rekts"
				]
				endMsg=""
				
				slotMachineGlobal+=1
				random.seed(a=clock()+slotMachineGlobal)
				
				#due to the easter egg thing down there. I know it's not very elegant.
				skipItAll = False
				if len(tokenizedContent)>2 :
					endMsg+="**"
					for i in range(2, len(tokenizedContent)) :
						endMsg+=tokenizedContent[i]+" "
					endMsg+="just got :**\n"
					
					# totally secret easter egg
					# 1/100 chances NOT to get rekt
					if random.randint(0,99) == 0 :
						endMsg += ":ballot_box_with_check: **Not rekt**\n"
						endMsg += ":white_medium_square: Rekt\n"
						await client.send_message(message.channel, endMsg) 
						skipItAll = True
					
				
				if not skipItAll :
					endMsg += ":white_medium_square: Not rekt\n"
					
					# using the same one as in "jackpot" just in case we get two at the same second
					
					random.shuffle(messages)
					# so there are three random "rekt" outcomes. To determine which ones get checked (at least one must be)
					# we spin a rand int
					# 0, 1, 2 -> corresponding one is checked
					# 3 -> #0 and #1 are checked ; 4 -> #1 and #2 are checked ; 5 -> #0 and #2 are checked
					# 6 -> all three are checked
					swag = random.randint(0,5)
					
					if swag in {0, 3, 5, 6} :
						endMsg+=":ballot_box_with_check: "+messages[0]
					else :
						endMsg+=":white_medium_square: "+messages[0]
					endMsg+="\n"
					if swag in {1, 3, 4, 6} :
						endMsg+=":ballot_box_with_check: "+messages[1]
					else :
						endMsg+=":white_medium_square: "+messages[1]
					endMsg+="\n"
					if swag in {2, 4, 5, 6} :
						endMsg+=":ballot_box_with_check: "+messages[2]
					else :
						endMsg+=":white_medium_square: "+messages[2]
					endMsg+="\n"
					
				
					await client.send_message(message.channel, endMsg) 

			
			
			if len(tokenizedContent)>2 :
				# print dongers
				if tokenizedContent[1] == "donger" and "donger" not in properties.disabled :
					msgText = ""
					if len(tokenizedContent)>3 :
						for wallTextK in range(3, len(tokenizedContent)):
							msgText += " "+tokenizedContent[wallTextK]
					
					if tokenizedContent[2] == "lenny":
						await client.send_message(message.channel, "( ͡° ͜ʖ ͡°)"+msgText)
					elif tokenizedContent[2] == "wizard-lenny":
						await client.send_message(message.channel, "╰( ͡° ͜ʖ ͡° )つ──☆*:・ﾟ"+msgText)
					elif tokenizedContent[2] == "spider-lenny":
						await client.send_message(message.channel, "/╲/( ͡° ͡° ͜ʖ ͡° ͡°)/\\\╱\\"+msgText)
					elif tokenizedContent[2] == "wall":
						wallMsg = "┳┻|\n┻┳|\n┳┻|\n┻┳|\n┳┻|\n┻┳|\n┳┻|\n┻┳|\n┳┻|\n┻┳|\n┳┻| _\n┻┳| •.•)"+msgText+"\n┳┻|⊂ﾉ\n┻┳|"
						await client.send_message(message.channel, wallMsg)
				
				
						
				
				# search on magiccards.info
				elif tokenizedContent[1] == "mc" and "mc" not in properties.disabled :
					# percent-encoding the URL
					queryMC = "";
					for i in range(2, len(tokenizedContent)):
						queryMC+=tokenizedContent[i]
						if i != len(tokenizedContent)-1:
							queryMC+=" "
					listurl = queryMC
					listurl = urllib.parse.quote(listurl, safe="")
					listurl = "http://magiccards.info/query?q="+listurl+"&v=olist&s=cname"
					
					try:
						cardListUrl  = urllib.request.urlopen(listurl)
						# getting the number of cards returned by the request
						cardListSource = cardListUrl.read()
						cardListSource = cardListSource.decode("utf-8")
						cardListUrl.close() # idk
						
						nbCardsIndex = cardListSource.find("[ 1-")
						if nbCardsIndex == -1 :
							# maybe there are no results ?
							if cardListSource.find("Your query did not match any cards") != -1 :
								await client.send_message(message.channel, "*"+queryMC+"* : **NO results**") 
						
							# there's only one card corresponding. MC.info redirected us to it
							else:
								cardTitleIndex = cardListSource.find("<title>")
								cardTitleIndex+=7
								cardEndTitleIndex = cardListSource.find("</title>")
								cardTitle = cardListSource[cardTitleIndex:cardEndTitleIndex]
								
								cardTitleEndPointer = len(cardTitle)
								while True:
									cardTitleEndPointer-=1
									cardTitle=cardTitle[:cardTitleEndPointer]
									#print(str(cardTitleEndPointer))
									if cardTitle[cardTitleEndPointer-1] == "(" :
										cardTitle=cardTitle[:cardTitleEndPointer-2] # -2 because space
										break
								
								await client.send_message(message.channel, "*"+queryMC+"* : **one result**")
								msg_list = ask_api.ask_card(cardTitle)
								for msg in msg_list:
									await client.send_message(message.channel, msg)
								
						else:
							nbCardsIndex+=4
							actualNbCards=""
							for i in range(0, 10) : # I'm sure well never have more than 9999999999 cards in one request, right ? At time of writing there are like 14 000 cards total
								if cardListSource[nbCardsIndex+i]==" " :
									break
								else :
									actualNbCards+=cardListSource[nbCardsIndex+i]
							actualNbCards = int(actualNbCards);
							
							await client.send_message(message.channel, "*"+queryMC+"* : **"+str(actualNbCards)+" results**.\nSee on "+listurl)
							
							#TODO
							#if actualNbCards<10 :
						
						
					except urllib.error.HTTPError: # ¯\_(ツ)_/¯
						await client.send_message(message.channel, "Unable to load magiccards.info")
				
				
				# calls to GNU's bc calculator
				# elif tokenizedContent[1] == "bc" :
				# actually that was dumb
				
				#now we're talking !
				elif (
					(tokenizedContent[1] == "cowsay" and "cowsay" not in properties.disabled)
					or (tokenizedContent[1] == "cowthink" and "cowthink" not in properties.disabled)
					or (tokenizedContent[1] == "toilet" and "toilet" not in properties.disabled)
					):
					args = []
					if tokenizedContent[2] == "list-files" :
						if tokenizedContent[1] == "cowsay" or tokenizedContent[1] == "cowthink" :
							args = ["ls", "/usr/share/cowsay/cows"]
						elif tokenizedContent[1] == "toilet" :
							args = ["ls", "/usr/share/figlet/"]
					else :
						
						for cowi in range(1, len(tokenizedContent)) :
							args.append(tokenizedContent[cowi])
					
					proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
					cowout, cowerr = proc.communicate(timeout=3)
					await client.send_message(message.channel, "```\n"+str(cowout)+"\n"+str(cowerr)+"\n```")

	# from here on, it'as about the [card name] searches
	
	# this way of disabling them does mean we won't log them, but who cares
	if "cardsinbrackets" not in properties.disabled :
		fin = len(content)
		debut = content.find("[") + 1
		while debut > 0:
			# ss1 = content[ouvert: fin]
			fin = content.find("]", debut)
			requete = content[debut: fin]
			print("Request : " + requete)
			if len(requete) > 2:
				msg_list = ask_api.ask_card(requete)
				
				for msg in msg_list:
					await client.send_message(message.channel, msg)
			debut = content.find("[", fin) + 1


client.run(email, password)
