
# requirements :
# - pillow for Python 3.5+
# - libfreetype6-dev

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import textwrap
from time import clock,localtime,strftime


def genCard(name="Nameless", type="Typeless", pt="", cost="", text="", returnType="path"):
	frame = Image.open("cardgen/artifact.png").convert('RGBA') # convert to avoid bug https://github.com/python-pillow/Pillow/issues/646#issuecomment-42615401
	draw = ImageDraw.Draw(frame)
	if (len(name)<26) :
		fontTitle = ImageFont.truetype("cardgen/beleren-bold.ttf",18)
		draw.text((22,15), name, font=fontTitle, fill=(0,0,0,224))
	else :
		fontTitle = ImageFont.truetype("cardgen/beleren-bold.ttf",14)
		draw.text((20,18), name, font=fontTitle, fill=(0,0,0,224))
	
	# magic
	type = type.replace(" - "," — ")
	if (len(type)<36) :
		fontTitle = ImageFont.truetype("cardgen/beleren-bold.ttf",18)
		draw.text((18,254), type, font=fontTitle, fill=(0,0,0,224))
	else :
		fontTitle = ImageFont.truetype("cardgen/beleren-bold.ttf",14)
		draw.text((18,257), type, font=fontTitle, fill=(0,0,0,224))
	
	#TODO ruletext parsing :
	# - symbols
	# - italics
	
	startHeight=283
	
	"""
	if (len(text)<31) :
		textWrapped=textwrap.wrap(text, width=30)
		fontText = ImageFont.truetype("cardgen/mplantin.ttf",16)
		for i in textWrapped :
			draw.text((18,startHeight), i, font=fontText, fill=(0,0,0,224))
			startHeight+=17
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
genCard(name="Jean-Marc, Homeworker", type="Legendary Creature - Student", text=bigText)
"""