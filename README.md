lorkclient: A curses [bsjtf lork](https://bsjtf.com) client, written in python.
===============================================================================

To run (Ubuntu):

* `sudo apt-get install python3-requests`
* `TERM=xterm-256color python3 lorkclient.py`
  * Totally will not work without redefining TERM!

No Windows, sorry. (WINDOWS, Y U NO HAVE CURSES MODULE?)

UPDATE: Turns out there *is* an unofficial port of curses to Windows.
[Have fun.](http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses)

Known Issues:
-------------

HTML tags. A small amount of tags and entities are replaced (specifically br,
gt, and nbsp). Everything else will show up verbatim in your terminal (avoid
HELP like the plague!)
