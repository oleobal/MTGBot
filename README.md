Discord Bot with Magic: the Gathering --related features.
---

.. And other minor features. Here's a list of commands :
```
"help" gets you this list

"mc" searches on http://magiccards.info/ :
    tron mc o:"Counter target spell"

"cardgen" can generate card images on the fly

"py" can execute Python programs.
	
"donger" produces dongers :

"jackpot" spins a slot machine.

"rekt" helps maintain your cred.
    You can pass it a name to explain who got rekt.

"company" makes you feel less alone.

"cowsay" and "toilet" are classic ASCII art generators.
    tron cowsay -f dragon-and-cow.cow I'm a [Clockwork Dragon]
```

All these are toggleable in a configuration file.

### Installation instructions :

Watch out, this bot is made for Unix. You're welcome to try it on Windows (probably by disabling features), I suppose.


1. Install Python 3.5 (latest release at time of writing, won't work on earlier versions). When I write ```pip```, I of course mean the Python 3 version, so ```pip3``` or ```python3 pip``` or something along those lines.

2. The following instructions have to be executed in command line 

  * Download discord.py (https://github.com/Rapptz/discord.py) with :
```pip install -U discord.py```

  * Download mtgsdk for python (https://github.com/MagicTheGathering/mtg-sdk-python) with :
```pip install mtgsdk```

3. Create a Discord account for your bot and add him to your server and the right channels on the server

4. Open properties.conf and edit "username" and "password" with your bot's Discord account's so it can connect

5. Run DiscordClient.py and let it run in the background

Two notes here : 
- I find nohup to be a convenient way to do this
- Discord might send e-mails to validate your bot's IP, which can be frustrating. Don't execute the bot twenty times in a row scratching your head, just wait for the (often not timely) e-mails.



#### Enabling cardgen

This requires Pillow if it's not already there. But before you install it, you'll need libraries to read the TrueType fonts used by the generator. On Debian the corresponding package is ```libfreetype6-dev``` ; then, you are free to ```pip install pillow```. If it was already installed, you might need to recompile it (just ```pip uninstall pillow``` and install it again)

Then, go and enable cardgen in properties.conf (remove the "disabled" entry).
#### Enabling cowsay/cowthink/toilet

Simply install the required program (cowsay or toilet).

Then, go and enable it in properties.conf (remove the "disabled" entry).

#### Is there a simpler way ?

Well, I guess you could just invite the instance I'm hosting to your server. Send me a PM or something, I won't check invites otherwise.

### In Discord
Use [cardname] to get the card whose name is “cardname” (or the first 20 cards in alphabetical order whose names contain “cardname” if it does not exist)

The bot uses "tron" and "mchtron" by default for calls :
```tron help```
Note that this is configurable, check properties.conf.
