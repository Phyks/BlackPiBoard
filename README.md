BlackPiBoard
============

A blackboard using a Raspberry Pi and a pico-projector !

## Setup
I had a Raspberry Pi, an old videoprojector and a Wacom tablet lying around and
search for something cool to do with them. So, I decided to make an interactive
blackboard.

The base code is minimalist for now, but I will develop it in the future.

So, basically, you just have to connect the Wacom tablet and the videoprojector
to the Raspberry Pi and launch the script. You should install `python-wxtools` with `sudo apt-get install python-wxtools` though.

## Detailed configuration

I have an Arch Linux ARM up to date on my Raspberry Pi (important to have the
modules for wacom tablet, only available from version 3.10.27-1 of
`linux-raspberrypi` package). The wacom tablet should be detected automatically
by the kernel and be usable.

The picoprojector is connected to the Raspberry Pi _via_ composite AV cable.

I didn't want to have a full desktop environment running on my Raspberry Pi, so
I just installed the X server, and set up a xinitrc in my user home dir to
automatically launch this python script at startup. I also set up an automatic
login using (this
page)[https://wiki.archlinux.org/index.php/automatic_login_to_virtual_console].

I still have to find a correct configuration for the Wacom tablet. Especially
to be able to use the eraser and the menu in the app.

## LICENSE

**Note :** The original code was found here: http://compsci.ca/v3/viewtopic.php?t=32343.
I reused his code which was a good base for my code, but don't have any ways to
contact him and no information on the license. So, the following only apply to
my personnal modifications of the code.

TLDR; I don't give a damn to anything you can do using this code (but please,
tell me if you do anything cool :). It would just be nice to quote where the
original code comes from.


* -----------------------------------------------------------------------------
* "THE NO-ALCOHOL BEER-WARE LICENSE" (Revision 42):
* Phyks (webmaster@phyks.me) modified this file. As long as you retain this notice
* you can do whatever you want with this stuff (and you can also do whatever
* you want with this stuff without retaining it, but that's not cool...). If we
* meet some day, and you think this stuff is worth it, you can buy me a
* <del>beer</del> soda in return.
*																		Phyks
* ------------------------------------------------------------------------------
