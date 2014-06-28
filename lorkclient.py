import curses, re, textwrap
from liblork import *

newlinere = re.compile("<BR.*?>", re.IGNORECASE)
gtre = re.compile("&gt;", re.IGNORECASE)
nbspre = re.compile("&nbsp;", re.IGNORECASE)
redre = re.compile("<font .*?color='#FE2E2E'.*?>", re.IGNORECASE)
whitere = re.compile("<font .*?color='#ccc'.*?>", re.IGNORECASE)
boldre = re.compile("<b>", re.IGNORECASE)

class Screen:
	def __init__(self, stdscr):
		self.titleText = "Lork v0.1"
		self.stdscr = stdscr

		self.stdscr.keypad(0)
		curses.curs_set(1)
		curses.echo()

		self.rows, self.cols = self.stdscr.getmaxyx()
		self.lines = ["Type \"/quit\" or \"/exit\" to return to your shell\n",
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
		self.stdscr.addstr(0, 0, " " * self.cols, curses.color_pair(2))
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
		# there's gotta be a better way to normalize these lines
		# ...anyone?
		lines = newlinere.sub("\n", "\n".join(lines))
		lines = gtre.sub(">", lines)
		lines = nbspre.sub(" ", lines)
		lines = redre.sub(chr(256 + 3), lines)
		lines = whitere.sub(chr(256 + 1), lines)
		lines = boldre.sub(chr(266 + 1), lines)
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
			elif ord(text[i]) > 256:
				self.lineattr = curses.color_pair(ord(text[i]) - 256)
			else:
				self.stdscr.addch(text[i], self.lineattr)
		self.lineattr &= ~curses.A_BOLD

	def renderInput(self):
		self.stdscr.addstr(self.rows - 1, 0, ">" +
				(" " * (self.cols - 2)), curses.color_pair(2))
		self.stdscr.move(self.rows - 1, 2)

	def getInput(self):
		self.stdscr.attron(curses.color_pair(2))
		text =  self.stdscr.getstr(self.rows - 1, 2)
		self.stdscr.attroff(curses.color_pair(2))
		return text

def startCurses(stdscr):
	screen = Screen(stdscr)
	lc = LorkClient(verbose=True)
	lc.addClearCallback(screen.clearLines)
	imp = screen.getInput()
	while imp.lower() not in (b"/quit", b"/exit"):
		resp = lc.input(imp)
		screen.setRoom(lc.room)
		screen.setScore(lc.points)
		screen.addLine(resp)
		imp = screen.getInput()

if __name__ == "__main__":
	curses.wrapper(startCurses)
