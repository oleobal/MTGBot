from mtgsdk import Card

import urllib.request
#this is used to test whether the URL we build for magiccards.info is valid
#if it's not we fall back to Gatherer (lower scan quality)

def ask_card(cardname):
    cards = Card.where(name=cardname).all()
    l = []
    n = []
    i = 0
    for card in cards:
        if i == 9:
            l.append("\n:exclamation: *More results, stopping here.*")
            break
        if card.name not in n:
            msg = "**" + card.name + "**" + " "
            if card.mana_cost is not None:
                # HERE BE MODIFICATIONS
                #msg += card.mana_cost
                emojifiedManaCost = card.mana_cost


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

                # if card.set_name=='Unhinged' or card.set_name=='Unglued' :
                #msg += " - "
                #last_set = card.printings[-1]
                #msg+=last_set # only latest set
                #for set in card.printings:
                #    msg += set
                #    if set == last_set:
                #        msg += "*"
                #    else:
                #        msg += ", "
            msg += "\n"
            if card.type is not None:
                msg += card.type
            if "Creature" in card.types:
                msg += " " + card.power + "/" + card.toughness
            elif "Planeswalker" in card.types:
                msg += ". Starting Loyalty " + str(card.loyalty)
            if card.text is not None:
                msg += "\n" + card.text
            msg += "\n"
           
            if len(cards)<4 :
                try: 
                    mcScan = urllib.request.urlopen("http://magiccards.info/scans/en/"+str(card.printings[0]).lower()+"/"+str(card.number)+".jpg")
                    msg+="http://magiccards.info/scans/en/"+str(card.printings[0]).lower()+"/"+str(card.number)+".jpg"
                except urllib.error.HTTPError:
                    try:
                        msg+=card.image_url
                    except TypeError:
                        pass

            #msg+="type : "+str(type(card.number))
            if cardname.lower() == card.name.lower():
                l = [msg]
                break
            else:
                l.append(msg)
                i += 1
                n.append(card.name)
            
    return l

