# joomla4-brute-force.py

**Note: This Python script is intended solely for educational purposes and ethical hacking practice. Please ensure you have explicit permission from the target system's owner before using it in any real-world scenario. Unauthorized or malicious use of this script is strictly discouraged and illegal.**

The script is pretty simple. It takes a username and passwords from a wordlist, looks to enter them into the /Administrator login portal, and see if it returns an error or not.

However, for Joomla 4 and above (not tested on Joomla 3), the cookie is a little bit complicated. Also you can probably do this in Hydra but hopefully this script makes it easier for you as this script for the DIV section where the error message should occur as well as grabs the right cookie.

I'm leaving this in Python for now as it is easier to modify, especially as Joomla versions later on may change the resulting login ERROR message.

Have fun!
