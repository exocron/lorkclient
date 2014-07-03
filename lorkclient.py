import curses, re, textwrap
from liblork import *
from html.parser import HTMLParser
try:
	import yaml
	have_yaml = True
except:
	have_yaml = False

class LorkHTMLParser(HTMLParser):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.data_acc = ""
		self.is_bold = False # work-around for lack of </b> tags

	def handle_data(self, data):
		self.data_acc += data

	def handle_starttag(self, tag, attrs):
		if tag == "br":
			if self.is_bold:
				self.data_acc += chr(266 + 2)
				self.is_bold = False
			self.data_acc += "\n"
		elif tag == "font":
			for key, value in attrs:
				if key == "color" and value.lower() == "#fe2e2e":
					# abusing unicode characters >256 as control codes
					self.data_acc += chr(256 + 3)
				elif key == "color" and value.lower() in ("#ccc", "#cccccc"):
					self.data_acc += chr(256 + 1)
		elif tag == "b":
			self.data_acc += chr(266 + 1)
			self.is_bold = True

	def get_data(self):
		return self.data_acc

class Screen:
	def __init__(self, stdscr, custom=False):
		self.titleText = "Lork v0.1"
		self.stdscr = stdscr

		self.stdscr.keypad(0)
		curses.curs_set(1)
		curses.echo()

		self.rows, self.cols = self.stdscr.getmaxyx()
		self.lines = ["Type \"/quit\" or \"/exit\" to return to your shell",
				"Custom commands loaded from custom.yml\n" if custom else "",
				# hardcoded FTW
				"Lork v0.1", "SHALL WE PLAY A GAME?\n"]

		curses.start_color()
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_WHITE, 8)
		curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
		self.lineattr = curses.color_pair(1)

		self.room = ""
		self.score = 0
		self.render()

	def addLine(self, line):
		self.lines.append(line)
		self.render()

	def clearLines(self):
		self.lines = list()
		self.render()

	def setRoom(self, room):
		self.room = room

	def setScore(self, score):
		self.score = score

	def render(self):
		self.stdscr.clear()
		self.renderTitle(self.titleText)
		self.renderRoom(self.room)
		self.renderScore(self.score)
		self.renderInput()
		self.renderLines(self.lines)
		self.stdscr.refresh()

	def renderTitle(self, text):
		self.stdscr.chgat(0, 0, -1, curses.color_pair(2))
		if len(text) > self.cols:
			text = text[:self.cols]
		self.stdscr.addstr(0, (self.cols - len(text)) // 2, text,
				curses.color_pair(2) | curses.A_BOLD)

	def renderRoom(self, room):
		self.stdscr.addstr(0, 0, "Room: %s" % room,
				curses.color_pair(2))

	def renderScore(self, score):
		score = "Score: %d" % score
		self.stdscr.addstr(0, self.cols - len(score), score,
				curses.color_pair(2))

	def renderLines(self, lines):
		self.lineattr &= ~curses.A_BOLD
		parser = LorkHTMLParser(convert_charrefs=True)
		parser.feed("\n".join(lines))
		parser.close()
		lines = parser.get_data()
		# there's gotta be a better way to normalize these lines
		# ...anyone?
		lines = lines.split("\n")
		lines = [textwrap.fill(line, self.cols) for line in lines]
		lines = "\n".join(lines)
		lines = lines.split("\n")
		if len(lines) > self.rows - 2:
			lines = lines[-(self.rows-2):]
		i = 1
		for line in lines:
			self.addstr(i, 0, line)
			i += 1

	def addstr(self, y, x, text):
		self.stdscr.move(y, x)
		for i in range(len(text)):
			if ord(text[i]) == 267:
				self.lineattr |= curses.A_BOLD
			elif ord(text[i]) == 268:
				self.lineattr &= ~curses.A_BOLD
			elif ord(text[i]) > 256:
				self.lineattr = curses.color_pair(ord(text[i]) - 256)
			else:
				self.stdscr.addch(text[i], self.lineattr)

	def renderInput(self):
		self.stdscr.chgat(self.rows - 1, 0, -1, curses.color_pair(2))
		self.stdscr.addstr(self.rows - 1, 0, ">", curses.color_pair(2))
		self.stdscr.move(self.rows - 1, 2)

	def getInput(self):
		self.stdscr.attron(curses.color_pair(2))
		text =  self.stdscr.getstr(self.rows - 1, 2)
		self.stdscr.attroff(curses.color_pair(2))
		return text

def startCurses(stdscr):
	if have_yaml:
		try:
			with open("custom.yaml", "r") as f:
				custom = yaml.load(f)
				screen = Screen(stdscr, True)
		except:
			custom = None
			screen = Screen(stdscr)
	else:
		custom = None
		screen = Screen(stdscr)
	lc = LorkClient(verbose=True)
	lc.addClearCallback(screen.clearLines)
	imp = screen.getInput()
	while imp.lower() not in (b"/quit", b"/exit"):
		if imp.lower().startswith(b"/") and custom is not None:
			try:
				for cmd in custom[imp.lower()[1:].decode("utf-8")]:
					resp = lc.input(cmd)
					screen.setRoom(lc.room)
					screen.setScore(lc.points)
					screen.addLine(resp)
			except KeyError:
				screen.addLine("\nNo command named " + imp.decode("utf-8"))
		else:
			resp = lc.input(imp)
			screen.setRoom(lc.room)
			screen.setScore(lc.points)
			screen.addLine(resp)
		imp = screen.getInput()

if __name__ == "__main__":
	curses.wrapper(startCurses)
