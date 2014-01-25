BlackBagTool
============

A tool for rapid discovery on mounted hard drives

Usage
=====
This tool is designed to rapidly gather information from common applications and known locations
on the filesystem. It's primary use would be in the initial information-gathering stage of an 
investigation. 

The controller isn't written yet, and I'm mostly trying to build out the applications. That way,
they can be used on the command line, in a GUI/CLI interface, and/or in a script.

Example
=======
```
from BlackBagTool.Apps.Skype import Skype
from BlackBagTool.Apps.Chrome import Chrome

skype = Skype('/mnt/Users/Admin/AppData/Roaming/Skype/')

for user in skype.getUsers():
    print "Getting contacts for %s" % user
    print skype.getContacts(user)

chrome = Chrome('/home/user/.config/google-chrome/')

for history_item in chrome.getWebHistory():
    print history_item.pretty()
```

Breakdown
=========

Each asset (web history item, cookie, download, etc) should have it's own class. That class
should have a few basic methods to enable consistent usage:

+ Asset.pretty() - Prints the data in a nice format. This method converts times, dates, etc and draws conclusions based on data. For example, highlighting a contact as "recently added", or calculating the relevance of a piece of data.



    
    	       
