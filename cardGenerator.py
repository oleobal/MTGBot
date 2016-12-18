
# requirements :
# - pillow for Python 3.5+
# - libfreetype6-dev
#TODO: make the font requirements a switch to enable rather than a mandatory thing so that it works out of the box.

# Note that Pillow has basic to no anti-aliasing, depending on functions
# there is when you resize, but not on fonts for instance
# Hence image artifacts

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import textwrap
from time import clock,localtime,strftime

from io import BytesIO
import urllib.request
import urllib.parse

def genCard(name="Nameless", type="Typeless", pt="", cost="", text="", imgurl="", returnType="path"):

	# parsing costs to determine colour
	# finalCost contains the filenames without path or extension ("U" -> "cardgen/symbols/U.png")
	finalCost=[]
	idx = 0
	while idx < len(cost) :
		i=cost[idx]
		i=i.upper()
		# single symbols
		if i in ['W', 'U', 'B', 'R', 'G', 'S', 'X','C' ] : # classic magic eructation
			finalCost.append(i)
			
		
		
		# numbers 0-20
		elif i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] :
			if (idx+1 < len(cost)) and (cost[idx+1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) :
				if i=="2" :
					finalCost.append("20")
					idx+=1
				elif i=="1" :
					finalCost.append(str(i+cost[idx+1]))
					idx+=1
				# else we just put one then the oether I guess
				else :
					finalCost.append(i)
			else :
				finalCost.append(i)
		
		# curly brackets
		elif i=="{" :
			k=1
			item=""
			while cost[idx+k] != "}" :
				item+=cost[idx+k]
				k+=1
				
			finalCost.append(curlyBracketsToFileName(item))
			
			idx+=k
		
		idx+=1
	#print(str(finalCost))
	
	#determining colour
	colours=[]
	for i in ['W', 'B', 'U', 'R', 'G'] :
		for j in finalCost :
			if i in j :
				colours.append(i)
	
	# selecting appropriate frame
	if len(colours) == 0 :
		# now obviously all colourless aren't artifacts and a lot of artifacts have coloured costs but colourless nonartifacts are pretty rare so..
		frame = Image.open("cardgen/artifact.png").convert('RGBA') # convert to avoid bug https://github.com/python-pillow/Pillow/issues/646#issuecomment-42615401
	
	elif len(colours) == 1 :
		if 'W' in colours :
			frame = Image.open("cardgen/white.png").convert('RGBA')
		elif 'B' in colours :
			frame = Image.open("cardgen/white.png").convert('RGBA')
		elif 'U' in colours :
			frame = Image.open("cardgen/blue.png").convert('RGBA')
		elif 'R' in colours :
			frame = Image.open("cardgen/red.png").convert('RGBA')
		elif 'G' in colours :
			frame = Image.open("cardgen/green.png").convert('RGBA')
	else :
		frame = Image.open("cardgen/gold.png").convert("RGBA")
		
		
	draw = ImageDraw.Draw(frame)
	
	if imgurl != "" and (imgurl.endswith("jpg") or imgurl.endswith("jpeg") or imgurl.endswith("png") or imgurl.endswith("gif")):
		picture = urllib.request.urlopen(imgurl)
		if 200 <= picture.getcode() <= 299 : #loaded correctly
			#picture = urllib.request.Request(imgurl)
			picFile=BytesIO(picture.read())
			cardPicture = Image.open(picFile).convert('RGBA')
			
			# now we have out picture we must crop it
			# in our frames the img frame is 279*205=
			
			
			for i in range(500) : # not too many iterations, right ?
				imgx, imgy = cardPicture.size
				if (imgx/imgy) > (1.38): #too high
					cardPicture = cardPicture.crop((1,0,imgx-1,imgy))
				elif (imgx/imgy) < (1.34): # too wide
					cardPicture = cardPicture.crop((0,1,imgx,imgy-1))
				else:
					break
					
			cardPicture=cardPicture.resize((279,205))
			frame.paste(cardPicture, (16,43))
	
	# title
	if (len(name)<26) :
		fontTitle = ImageFont.truetype("cardgen/beleren-bold.ttf",19)
		draw.text((22,15), name, font=fontTitle, fill=(0,0,0,224))
	else :
		fontTitle = ImageFont.truetype("cardgen/beleren-bold.ttf",14)
		draw.text((20,18), name, font=fontTitle, fill=(0,0,0,224))
	
	# cost is formally {<letter(s)>} but for single colours and numbers it's most often given without
	# basically, 3SU{U/P}{G/R} should be recognized
	
	# font-based cost
	# using https://andrewgioia.github.io/Mana/
	"""
	finalCost=""
	idx = 0
	while idx < len(cost) :
		i=cost[idx]
		i=i.upper()
		if i == "W" :
			#finalCost+="&#xe600;"
			finalCost+=""
		elif i == "U" :
			#finalCost+="&#xe601;"
			finalCost+=""
		elif i == "B" :
			#finalCost+="&#xe602;"
			finalCost+=""
		elif i == "R" :
			#finalCost+="&#xe603;"
			finalCost+=""
		elif i == "G" :
			#finalCost+="&#xe604;"
			finalCost+=""
		elif i == "C" :
			finalCost+=""
		elif i == "S" :
			finalCost+=""
		elif i == "X" :
			finalCost+=""
		elif i == "Y" :
			finalCost+=""
		elif i == "Z" :
			finalCost+=""
		
		#todo handle {something} syntax
			
		elif i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] :
			if (cost[idx+1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) and (i in ['1', '2']) :
				# now this is only 10-20, that's the font, not me
				if i == '2' :
					finalCost+="" #20
				else :
					if cost[idx+1] == '0' : # 10
						finalCost+=""
					if cost[idx+1] == '1' : # 11
						finalCost+=""
					if cost[idx+1] == '2' :
						finalCost+=""
					if cost[idx+1] == '3' :
						finalCost+=""
					if cost[idx+1] == '4' :
						finalCost+=""
					if cost[idx+1] == '5' :
						finalCost+=""
					if cost[idx+1] == '6' :
						finalCost+=""
					if cost[idx+1] == '7' :
						finalCost+=""
					if cost[idx+1] == '8' :
						finalCost+=""
					if cost[idx+1] == '9' :
						finalCost+=""
						
				idx+=1 # skipping second digit
				
			else :
				if i == '0' :
					finalCost+=""
				if i == '1' :
					finalCost+=""
				if i == '2' :
					finalCost+=""
				if i == '3' :
					finalCost+=""
				if i == '4' :
					finalCost+=""
				if i == '5' :
					finalCost+=""
				if i == '6' :
					finalCost+=""
				if i == '7' :
					finalCost+=""
				if i == '8' :
					finalCost+=""
				if i == '9' :
					finalCost+=""
			
		idx+=1
	
	fontCost=ImageFont.truetype("cardgen/mana.ttf",17) 
	costOffset = 295
	#print("LOLOLOL "+str(draw.textsize(finalCost, font=fontCost)))
	costOffset -= draw.textsize(finalCost, font=fontCost)[0]
	draw.text((costOffset,17), finalCost, font=fontCost, fill=(0,0,0,255))
	"""
	
	#image-based cost
	
	costOffset = 297-(18*len(finalCost))
	for c in finalCost :
		symbol = Image.open("cardgen/symbols/"+c+".png").convert('RGBA')
		symbol=symbol.resize((17,17),resample=Image.LANCZOS )
		draw.ellipse([(costOffset-1, 17+1), (costOffset-1+17, 17+1+17)], fill=(0,0,0,128), outline=(0,0,0,128))
		frame.paste(symbol, (costOffset,17), mask=symbol) # What's with using the pasted image itself as mask ? Can't we directly use transparency values ?
		costOffset+=18 
	
	
	# type
	type = type.replace(" - "," — ")
	if (len(type)<36) :
		fontTitle = ImageFont.truetype("cardgen/beleren-bold.ttf",17)
		draw.text((18,254), type, font=fontTitle, fill=(0,0,0,224))
	else :
		fontTitle = ImageFont.truetype("cardgen/beleren-bold.ttf",14)
		draw.text((18,257), type, font=fontTitle, fill=(0,0,0,224))
	
	#TODO add italics support
	
	# my plan is to go word per word, with a 2d cursor. That way we manage the symbols as well
	# so we'll support the same symbols in text as in costs, plus tap ({T}) and energy ({E})
	# Difference being it's only the curly-bracketed versions
	
	#startHeight=283
	
	if (len(text)<150) :
		fontHeight = 17
	else :
		fontHeight = 14
		
	fontText = ImageFont.truetype("cardgen/mplantin.ttf",fontHeight)
	
	
	# separating into "words", maybe the wrong choice of words
	# basically, along spaces, but also separating {things} and \n from the rest
	# So for instance ['{T}', ',', '{X}', ' ', ':', ' ', 'Do', ' ', 'nothing', '\n', '\n', 'If', ' ', 'things,', ' ', 'then', ' ', 'thongs', '\n']
	tokens = text.split(" ")
	
	tidx=0
	words = []
	while tidx<len(tokens) :
		t=tokens[tidx]
		sym=""
		idx = 0
		while idx < len(t) :
			i = t[idx]
			
			
			if i=="\n":
				if sym != "" :
					words.append(sym)
				words.append("\n")
				#idx+=1
				sym=""
			
			
			elif i=="{" :
				if sym != "" :
					words.append(sym)
				sym = ""
				k=1
				while t[idx+k] != "}" :
					sym+=t[idx+k]
					k+=1
				idx+=k
				words.append("{"+sym+"}")
				sym=""
			
			else:
				sym+=i
			
			idx+=1
		
		if sym != "" :
			words.append(sym)
		
		tidx+=1
		if tidx != len(tokens) :
			words.append(" ")
		
			
	#print(str(words))
	# words now contains a nice list 
	
	# Alright now to draw this.
	
	cursor=[18, 283] #table because tuples are immutable
	idx = 0
	while idx < len(words) :
		i = words[idx]
		if i[0] == "{" and i[-1] == "}" :
			symbol = Image.open("cardgen/symbols/"+curlyBracketsToFileName(i[1:-1])+".png").convert('RGBA')
			symbol=symbol.resize((fontHeight,fontHeight),resample=Image.LANCZOS )
			frame.paste(symbol, (cursor[0], cursor[1]), mask=symbol)
			cursor[0]+=fontHeight
		elif i == " ":
			cursor[0]+=draw.textsize(" ", font=fontText)[0]
		elif i == "\n" :
			cursor[0] = 18
			cursor[1] += fontHeight+1
		else :
			lenEval = cursor[0] + draw.textsize(i, font=fontText)[0]
			if lenEval>294 : # outside the text frame
				cursor[0] = 18
				cursor[1] += fontHeight+1
				draw.text((cursor[0], cursor[1]), i, font=fontText, fill=(0,0,0,224))
				cursor[0] += draw.textsize(i, font=fontText)[0]
			else :
				draw.text((cursor[0], cursor[1]), i, font=fontText, fill=(0,0,0,224))
				cursor[0] += draw.textsize(i, font=fontText)[0]
			
			
		
		idx+=1
	
	"""
	if (len(text)<150) :
		textWrapped=textwrap.wrap(text, width=35)
		fontText = ImageFont.truetype("cardgen/mplantin.ttf",17)
		startHeight+=2
		for i in textWrapped :
			draw.text((18,startHeight), i, font=fontText, fill=(0,0,0,224))
			startHeight+=13
	else :
		textWrapped=textwrap.wrap(text, width=45)
		fontText = ImageFont.truetype("cardgen/mplantin.ttf",14)
		for i in textWrapped :
			draw.text((18,startHeight), i, font=fontText, fill=(0,0,0,224))
			startHeight+=15
	"""
	
	saveTitle=""
	acceptableChars=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	for i in name.lower() :
		if i in acceptableChars:
			saveTitle+=i
			
	time = strftime("%Z-%Y-%m-%d_%H-%M-%S", localtime())
	saveTitle=time+"_"+saveTitle
	
	frame.convert("P") # convert to avoid bug https://github.com/python-pillow/Pillow/issues/646#issuecomment-42615401
	frame.save("cardgen/temp/"+saveTitle+".png", "PNG")
	
	#TODO toy around that maybe at one point ?
	if returnType=="path":
		return "cardgen/temp/"+saveTitle+".png"


"""
smallText="Flying"

mediumText="{T}: Flip a coin. If you win the flip, tap target Student."
	
bigText="When Jean-Marc, Homework enters the battlefield, flip a coin. If you win the flip, Jean-Marc, Homeworker gains \"At the beginning of your upkeep, add {R} to your mana pool.\"."
genCard(name="Jean-Marc, Homeworker", type="Legendary Creature - Student", text=bigText, imgurl="http://67.media.tumblr.com/tumblr_lxlmcx8M1n1qc29lyo2_500.jpg")
# """



"""
This translates what's inside curly brackets (for symbols) to the right filenames

Say you have {U/P}
pass it "U/P"
it will return you "UP"
you know it mean UP.png
"""
def curlyBracketsToFileName(item) :
	
	if item in ['W', 'U', 'B', 'R', 'G', 'S', 'X','C', 'T', 'E' ] :
		return item
	elif item in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'] :
		return item
	
	elif item == "2B" or item == "2/B" or item == "B/2" or item == "B2" :
		return "2B"
	elif item == "2W" or item == "2/W" or item == "W/2" or item == "W2" :
		return "2W"
	elif item == "2G" or item == "2/G" or item == "G/2" or item == "G2" :
		return "2G"
	elif item == "2U" or item == "2/U" or item == "U/2" or item == "U2" :
		return "2U"
	elif item == "2R" or item == "2/R" or item == "R/2" or item == "R2" :
		return "2R"
	
	#ten colour pairs.. yay..
	elif item=="UB" or item=="BU" or item=="U/B" or item=="B/U" :
		return "UB"
	elif item=="UR" or item=="RU" or item=="U/R" or item=="R/U" :
		return "UR"
	elif item=="UG" or item=="GU" or item=="U/G" or item=="G/U" :
		return "GU"
	elif item=="UW" or item=="WU" or item=="U/W" or item=="W/U" :
		return "WU"
	
	elif item=="GB" or item=="BG" or item=="G/B" or item=="B/G" :
		return "BG"
	elif item=="RB" or item=="BR" or item=="R/B" or item=="B/R" :
		return "BR"
	elif item=="WB" or item=="BW" or item=="W/B" or item=="B/W" :
		return "WB"
	
	elif item=="WG" or item=="GW" or item=="W/G" or item=="G/W" :
		return "GW"
	elif item=="WR" or item=="RW" or item=="W/R" or item=="R/W" :
		return "RW"
		
	elif item=="GR" or item=="RG" or item=="G/R" or item=="R/G" :
		return "RG"
	
	#phyrexian mana
	elif item=="UP" or item=="PU" or item=="U/P" or item=="P/U" :
		return "UP"
	elif item=="WP" or item=="PW" or item=="W/P" or item=="P/W" :
		return "WP"
	elif item=="GP" or item=="PG" or item=="G/P" or item=="P/G" :
		return "GP"
	elif item=="BP" or item=="PB" or item=="B/P" or item=="P/B" :
		return "BP"
	elif item=="RP" or item=="PR" or item=="R/P" or item=="P/R" :
		return "RP"
		
	else :
		return ""