lorkclient: A curses [bsjtf lork](https://bsjtf.com) client, written in python.
===============================================================================

To run (Ubuntu):

* `sudo apt-get install python3-requests`
* Optional, macros: `sudo apt-get install python3-yaml`
* `TERM=xterm-256color python3 lorkclient.py`
  * Totally will not work without redefining TERM!

No Windows, sorry. (WINDOWS, Y U NO HAVE CURSES MODULE?)

UPDATE: Turns out there *is* an unofficial port of curses to Windows.
[Have fun.](http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses)

Macros: How do they work?
-------------------------

Macros are a list of commands that are automatically submitted sequentially by
the client. The intention is to make it easy to catch back up to a previous
state after becoming a Grue snack. To invoke a macro, type a forward slash,
followed by the name of the macro. For example, to replay the commands in the
if-main of liblork.py:

	catchup:
	 - global thermonuclear war
	 - turn on flashlight
	 - west
	 - south
	 - look at sticky note
	 - north
	 - use keypad

Once defined, typing `/catchup` will issue these commands one after another.
Macros are defined in custom.yaml and require PyYAML. Any number of macros can
be defined one after another. Macros are completely optional, and PyYAML is not
required when not using macros.

Known Issues:
-------------

HTML tags. Most tags are replaced (br becomes newlines, gt and nbsp are
unescaped, b triggers bold color and the font tags trigger red color).
Everything else will show up verbatim in your terminal (avoid HELP like the
plague!)
