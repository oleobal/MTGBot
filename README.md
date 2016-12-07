Discord Bot to fetch and display Magic : the Gathering cards.
---

.. And other minor features. Here's a list of commands :
```
"help" gets you this list

"mc" searches on http://magiccards.info/ :
    tron mc o:"Counter target spell"
	
"py" can execute Python programs.
	
"donger" produces dongers :
    tron donger <lenny, wizard-lenny, spider-lenny, wall>
    These dongers can use an argument, for instance :
       tron donger wall [text]
	
"jackpot" spins a slot machine.

"rekt" helps maintain your cred.
    You can pass it a name to explain who got rekt.

"company" makes you feel less alone.

"cowsay" and "toilet" are classic ASCII art generators.
    Example :
        tron cowsay -f dragon-and-cow.cow I'm a [Clockwork Dragon]
```

### Installation instructions :

Watch out, this bot expects a Unix environment. Now it might work on Windows, it might not (more probable, but you're welcome to try). But function calls were made without Windows in mind.

1. Install Python 3.5 (latest release at time of writing, won't work on earlier versions)

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

##### Is there a simpler way ?

Well, I guess you could just invite the instance I'm hosting to your server. Send me a PM or something, I won't check invites otherwise.

### In Discord
Use [cardname] to get the card whose name is “cardname” (or the first 20 cards in alphabetical order whose names contain “cardname” if it does not exist)

The bot uses "tron" and "mchtron" by default for calls :
```tron help```
Note that this is configurable, check properties.conf.