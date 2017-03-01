import discord

import urllib.request
import urllib.parse

import random
from time import clock,localtime,strftime # I'm running this on UNIX, so may vary on windows apparently

from io import StringIO

# running console commands
import subprocess

from Properties import *
properties = Properties()

if not "cardgen" in properties.disabled :
	from cardGenerator import *

cards = None
if not "cardsinbrackets" in properties.disabled :
	global cards
	import cardSearch
	import json  
	import zipfile  
	# downloading things if possible
	try :
		z = zipfile.ZipFile("AllCards-x.json.zip", "r")
		for filename in z.namelist():
			with z.open(filename) as f:  
				cards = json.loads((f.read()).decode("utf-8"))
				 
	except OSError as readError :
		archiveURL = "https://mtgjson.com/json/AllCards-x.json.zip"
		print("Could not open Cards JSON. Attempting to download "+archiveURL)
		try: 
			archive = urllib.request.urlretrieve(archiveURL, "AllCards-x.json.zip")
			print("Archive downloaded.")
			z = zipfile.ZipFile("AllCards-x.json.zip", "r")
			for filename in z.namelist():
				with z.open(filename) as f:  
					cards = json.loads((f.read()).decode("utf-8"))
		except urllib.error.HTTPError:
			print("Could not download file from mtgjson.com. Disabling cards in brackets for this session.")
			properties.disabled.append("cardsinbrackets")
		

# used to make sure two slot machine uses at the same second won't have the same results
slotMachineGlobal = 0



client = discord.Client()

#reading properties.conf into object


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
	
	# building ourselves a timestamp
	time = strftime("%Z %Y-%m-%d %H:%M:%S", localtime())
	
	
	print(time+" | New message")
	content = message.content
	tokenizedContent = content.split()

	if len(tokenizedContent)>1 :
		#TODO : support for multi-words summons
		if tokenizedContent[0] in properties.summon :
			
			print(time+" | Query : "+tokenizedContent[1])
			
			if tokenizedContent[1] == "help" and "help" not in properties.disabled :
				if len(tokenizedContent) == 2 :
					helpMsg= "Call with "
					for i in properties.summon :
						helpMsg+="\""+i+"\""
						if i != properties.summon[-1] :
							helpMsg+=" or "
						else :
							helpMsg+=".\n"
					helpMsg+="Use \"tron help <command>\" for details on a command.\n"
					
					helpMsg+="```\n"
					helpMsg+=properties.helpmsg
					helpMsg+="```\n"
				
				else :
					helpMsg= "Help for **"+tokenizedContent[2]+"** :\n"
					if tokenizedContent[2] in properties.helpmsgcommand :
						helpMsg+="```\n"
						helpMsg+=properties.helpmsgcommand[tokenizedContent[2]]
						helpMsg+="```\n"
					else:
						helpMsg+="*No help available.*"
				
				
				await client.send_message(message.channel, helpMsg)
			
			
			
			elif tokenizedContent[1] == "cardgen" and "cardgen" not in properties.disabled :
				
				lineContent = content.split("\n") 
				if len(lineContent)<3:
					await client.send_message(message.channel, "Malformed cardgen request.")
				
				genImgUrl=""
				if len(tokenizedContent)>2 :
					genImgUrl=tokenizedContent[2]
				
				nameAndCost = lineContent[1].split(sep=" - ", maxsplit=1)
				genName=nameAndCost[0]
				genCost=nameAndCost[1]
				genType = lineContent[2]
				genText = ""
				if len(lineContent)>3 :
					for i in lineContent[3:] :
						genText+=i+"\n"

				genPath = genCard(name=genName, cost=genCost, type=genType, text=genText, imgurl=genImgUrl)
				await client.send_file(message.channel, genPath)
				
			
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

					
					
					
					
					
					
			#execute python code		
			elif (tokenizedContent[1] == "py" and "py" not in properties.disabled):
				lineContent = content.split("\n")
				if len(lineContent)>3 and (lineContent[1] == "```" or lineContent[1] == "```Python") and lineContent[-1] == "```" :
					inputMessedWith = False
					pythonContent="import time\nimport random\n"
					for i in range(2,len(lineContent)-1) :
						if lineContent[i] != "":
							
							if "pybandages" in properties.disabled :
								
								if lineContent[i].rstrip()[-1] == ":" :
									pythonContent+=lineContent[i]
								else :
									pythonContent+=lineContent[i]+"\n"
							else :
								if (not "import" in lineContent[i]) and (not "exec" in lineContent[i]) and (not "eval" in lineContent[i]) and (not "getattr" in lineContent[i]) and (not "while True" in lineContent[i]): # this does cause collateral damage..
								
									if lineContent[i].rstrip()[-1] == ":" :
										pythonContent+=lineContent[i]
									else :
										pythonContent+=lineContent[i]+"\n"
								else :
									inputMessedWith = True
								
					
					pythonContent = pythonContent.replace('\"', '\\\"')
					
					pythonCommand="python3.5"
					#TODO make it selectable (in properties, users cannot be trusted)
					
					#TODO define command in properties
					#TODO add "pyexec" command that uses exec() (ie can modify the running program, it should be disabled by default)
					proc = subprocess.Popen(pythonCommand+' -c "'+pythonContent+'"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
					pyout, pyerr = proc.communicate(timeout=3)
					finalMessage=""
					try :
						nick = str(message.author.nick)
					except AttributeError : # no nickname
						nick = str(message.author)
					finalMessage+="Python program from "+nick+".\n"
					
					if inputMessedWith :
						finalMessage+="*Warning: some statements modified/removed (such as imports/execs/evals).*\n\n"
					if str(pyout)=="":
						finalMessage+="[Nothing on stdout]\n"
					else:
						finalMessage+="stdout:\n```\n"+str(pyout)+"\n```\n"
					if str(pyerr)!="":
						finalMessage+="stderr:\n```\n"+str(pyerr)+"\n```\n"
					await client.send_message(message.channel, finalMessage)
					
				else :
					await client.send_message(message.channel, "Malformed python call.")

			# executed with exec() without checks
			elif (tokenizedContent[1] == "pyexec" and "pyexec" not in properties.disabled):
				lineContent = content.split("\n")
				pythonContent=""
				if len(lineContent)>3 and (lineContent[1] == "```" or lineContent[1] == "```Python") and lineContent[-1] == "```" :
					for i in range(2,len(lineContent)-1) :
						if lineContent[i] != "":
							#if lineContent[i].rstrip()[-1] == ":" :
							#	pythonContent+=lineContent[i]
							#else :
							pythonContent+=lineContent[i]+"\n"
					
					#pythonContent = pythonContent.replace('\"', '\\\"')

					# redirecting stdout and stderr to print to chat
					pyexecout = StringIO("")
					pyexecerr = StringIO("")
					#totally optimized
					import sys
					orgOut = sys.stdout
					orgErr = sys.stderr
					sys.stdout = pyexecout
					sys.stderr = pyexecerr
					#print("What you typed :\n\n"+pythonContent+"\n----------\n\n")
					exec(pythonContent, globals(), locals())
					sys.stdout = orgOut
					sys.stderr = orgErr
					#del sys
					
					finalMessage=""
					try :
						nick = str(message.author.nick)
					except AttributeError : # no nickname
						nick = str(message.author)
					finalMessage+="Python program from "+nick+".\n"
					
					if str(pyexecout.getvalue())=="":
						finalMessage+="[Nothing on stdout]\n"
					else:
						finalMessage+="stdout:\n```\n"+str(pyexecout.getvalue())+"\n```\n"
					if str(pyexecerr.getvalue())!="":
						finalMessage+="stderr:\n```\n"+str(pyexecerr.getvalue())+"\n```\n"
					await client.send_message(message.channel, finalMessage)
					
				else :
					await client.send_message(message.channel, "Malformed python call.")
			
			
			
			
			
			
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
				
				# calls to cowsay/cowthink/toilet (ascii art generators)
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
					
					
				# python 3 interpreter
				

	# from here on, it'as about the [card name] searches
	
	# this way of disabling them does mean we won't log them, but who cares
	if "cardsinbrackets" not in properties.disabled :
		fin = len(content)
		isItThere = content.find(properties.cardDelimiters[0])
		debut=0
		while isItThere > -1:
			debut = content.find(properties.cardDelimiters[0],debut) + len(properties.cardDelimiters[0])
			fin = content.find(properties.cardDelimiters[1], debut)
			requete = content[debut: fin]
			print(time+" | Request : " + requete)
			if len(requete) > 0:
				global cards
				await client.send_message(message.channel, cardSearch.searchCard(cards, requete))
				
			isItThere = content.find(properties.cardDelimiters[0],debut)

client.run(email, password)

