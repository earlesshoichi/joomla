# joomla
The script is pretty simple. It takes a username and passwords from a wordlist, looks to enter them into the /Administrator login portal, and see if it returns an error or not.

However, for Joomla 4 and above (not tested on Joomla 3), the cookie is a little bit complicated. Also using Hydra would be complicated since the Joomla resulting response page shows both the login SUCCESS AND login ERROR messages.
Hence, the script looks for the DIV section where the error message should occur.

I'm leaving this in Python for now as it is easier to modify, especially as Joomla versions later on may change the resulting login ERROR message.

Have fun!
