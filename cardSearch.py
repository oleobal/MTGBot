import urllib.request

# expects an array with all cards and a card name
# returns a string (message)
# requires exact names (case-insensitive)
# returns None if no correspondance
def searchCard(cards, name, attachPicture=True, emojifyCost=True):
	# I know what you're thinking : "why not add other criteria ?".
	# jeez.
	# TODO
	
	cardKey = None
	for i in cards.keys():
		if i.lower() == name.lower():
			cardKey = i
			break
	
	if cardKey == None :
		return "No cards for \""+name+"\"."
	# I used the manage this via exception, but KeyError was thrown in cases where the key existed. I don't know why.
		
	card = cards[cardKey]
	#print(card)
	msg="**"+cardKey+"** "
	emojifiedManaCost = card["manaCost"]
	if emojifyCost :
		emojifiedManaCost = emojifiedManaCost.replace("{X}", ":regional_indicator_x:") 
		emojifiedManaCost = emojifiedManaCost.replace("{0}", ":zero:")
		emojifiedManaCost = emojifiedManaCost.replace("{1}", ":one:")
		emojifiedManaCost = emojifiedManaCost.replace("{2}", ":two:")
		emojifiedManaCost = emojifiedManaCost.replace("{3}", ":three:")
		emojifiedManaCost = emojifiedManaCost.replace("{4}", ":four:")
		emojifiedManaCost = emojifiedManaCost.replace("{5}", ":five:")
		emojifiedManaCost = emojifiedManaCost.replace("{6}", ":six:")
		emojifiedManaCost = emojifiedManaCost.replace("{7}", ":seven:")
		emojifiedManaCost = emojifiedManaCost.replace("{8}", ":eight:")
		emojifiedManaCost = emojifiedManaCost.replace("{9}", ":nine:")

		emojifiedManaCost = emojifiedManaCost.replace("{U}", ":droplet:") #couleurs les plus importantes en premier
		emojifiedManaCost = emojifiedManaCost.replace("{W}", ":sunny:")
		emojifiedManaCost = emojifiedManaCost.replace("{G}", ":deciduous_tree:")
		emojifiedManaCost = emojifiedManaCost.replace("{B}", ":skull:")
		emojifiedManaCost = emojifiedManaCost.replace("{R}", ":fire:")
	msg += emojifiedManaCost		
	msg +="\n"
	if card["type"] is not None:
		msg += card["type"]
	if "Creature" in card["types"]:
		msg += " " + card["power"] + "/" + card["toughness"]
	elif "Planeswalker" in card["types"]:
		msg += ". Starting Loyalty " + str(card["loyalty"])
	if card["text"] is not None:
		msg += "\n" + card["text"]
	msg += "\n"
	
	if attachPicture :
		# trying first with magiccards.info and then Gatherer
		# actually this won't work, because on the AllCards merged json, this data has been removed.
		try: 
			#mcScan = urllib.request.urlopen("http://magiccards.info/scans/en/"+str(card.printings[-1]).lower()+"/"+str(card.number)+".jpg")
			#msg+="http://magiccards.info/scans/en/"+str(card.printings[0]).lower()+"/"+str(card.number)+".jpg"
			#look at that, MtgJson provides a special field for magiccards.info
			mcScan = urllib.request.urlopen("http://magiccards.info/scans/en/"+str(card["printings"][-1]).lower()+"/"+str(card["mciNumber"])+".jpg")
			msg+="http://magiccards.info/scans/en/"+str(card["printings"][-1]).lower()+"/"+str(card["mciNumber"])+".jpg"
		except (urllib.error.HTTPError, KeyError):
			try:
				msg+="http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid="+str(card["multiverseid"])+"&type=card"
			except KeyError :
				pass
	
	return msg