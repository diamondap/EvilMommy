# Evil Mommy #

Evil Mommy is a simple Python Flask app that lets Mommy use her smart phone
or iPod touch to kick the kids off the internet.

This app works with the Linksys EA3500. You can run it on any machine 
inside your network that has a web server and a static IP address.

The app has two main features: denying and allowing internet access to a
set of devices. When you deny access, Evil Mommy breaks the device's DHCP
lease so that it loses its internet connection. Just to be extra cruel, Evil
Mommy also adds the device's MAC address to the router's black list, so it
cannot re-connect.

When you allow access, Nice Mommy removes the device's MAC address from the
router's black list, so it can once again access the internet.

## Why would you make something so evil? ##

Because Mommy is tired of you kids not listening when she says it's time for
dinner! She spent all that time cooking, and you won't even bother to look up
from the computer / the Roku / Netflix on the Wii.

Mommy didn't want to be Evil, but how many times did she  warn you about not 
listening?

## Configuring ##

Set your router URL, login name and password in EvilMommy/Config.py. You 
should also set up entries for the machines you want Mommy to control
You can get the configuration information from your Linksys router's web 
management console.

## Running ##

To run the app, run this command in the top-level directory:

> python evil_mommy.py

By default, it runs on port 3000. You can change that by editing the port
number in the last line of evil_mommy.py

## Using ##

Once you log in, choose either "disconnect" or "reconnect", select a device 
from the list, and click the button. That's it! Works even after three
glasses of wine!

## Testing ##

To run the unit tests:

> python test.py

If you set up the Config file to talk to your Linksys router, uncomment
the last line of test.py to run some basic integration tests. You'll have
to watch the output of the tests to see if all is working.

