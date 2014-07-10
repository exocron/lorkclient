import requests

class LorkClient:
	def __init__(self, session=None, verbose=False):
		self.cookies = LorkClient.getCookies(session)
		self.points = 0
		self.room = "<none>"
		self.clearCallbacks = set()
		self.verbose = verbose

	def addClearCallback(self, clearCallback):
		self.clearCallbacks.add(clearCallback)

	def removeClearCallback(self, clearCallback):
		self.clearCallbacks.remove(clearCallback)

	def getCookies(session=None):
		if session is not None:
			return requests.get("https://bsjtf.com/lork", cookies=dict(PHPSESSID=session)).cookies
		else:
			return requests.get("https://bsjtf.com/lork").cookies

	def input(self, inprompt):
		r = requests.post("https://bsjtf.com/lork/command.php",
				cookies=self.cookies,
				data=dict(inprompt=inprompt))
		self.cookies = r.cookies or self.cookies
		data = r.json()
		self.points = data["POINTS"]
		self.room = data["ROOM"]
		# eww...
		try:
			if data["RESPONSE"] == "START":
				for cb in self.clearCallbacks:
					cb()
				return data["DISPLAY"]
		except KeyError:
			pass
		if self.verbose:
			try:
				return data["BASE"] + data["DISPLAY"]
			except KeyError:
				return data["DISPLAY"]
		else:
			return data["DISPLAY"]

if __name__ == "__main__":
	lc = LorkClient()
	# you may want to rate-limit this
	print(lc.input("global thermonuclear war"))
	print(lc.input("turn on flashlight"))
	print(lc.input("west"))
	print(lc.input("south"))
	print(lc.input("look at sticky note"))
	print(lc.input("north"))
	print(lc.input("use keypad"))
	# ??? (what's next...)
