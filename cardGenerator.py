
# requirements :
# - pillow for Python 3.5+
# - libfreetype6-dev
#TODO: make the font requirements a switch to enable rather than a mandatory thing so that it works out of the box.

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import textwrap
from time import clock,localtime,strftime

from io import BytesIO
import urllib.request
import urllib.parse

def genCard(name="Nameless", type="Typeless", pt="", cost="", text="", imgurl="", returnType="path"):
	frame = Image.open("cardgen/artifact.png").convert('RGBA') # convert to avoid bug https://github.com/python-pillow/Pillow/issues/646#issuecomment-42615401
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
genCard(name="Jean-Marc, Homeworker", type="Legendary Creature - Student", text=bigText, imgurl="http://67.media.tumblr.com/tumblr_lxlmcx8M1n1qc29lyo2_500.jpg")
# """