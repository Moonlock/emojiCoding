import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from queue import Queue
from threading import Thread

import interpreter

COMMANDS = ['<', '>', '+', '-', '[', ']', '.', ',']
WHITESPACE = ['\n', '\t', ' ']
ERROR_SIZE = 72
BG_COLOUR = "#000000"
TEXT_COLOUR = "#000020"

class EmojiCoder:

	def __init__(self, root):
		self.HEIGHT = root.winfo_height()
		self.WIDTH = root.winfo_width()

		root.protocol("WM_DELETE_WINDOW", self.onClosing)

		self.guiQueue = Queue()
		self.interpreterQueue = Queue()
		self.root = root
		self.root.config(bg=BG_COLOUR)

		self.createTitle()
		self.createButtons()
		self.root.emoji = self.defineEmoji()
		self.createTextboxes()

		self.checkQueue()


	def createTitle(self):
		titleFrame = tk.Frame(self.root, pady=20, bg=BG_COLOUR)
		titleFrame.pack(side="top")

		fire = ImageTk.PhotoImage(Image.open("emoji/fire.png"))
		self.errorLeft = tk.Canvas(titleFrame, width=ERROR_SIZE, height=ERROR_SIZE,
			bg=BG_COLOUR, highlightbackground=BG_COLOUR)
		self.errorLeft.pack(side="left", padx=50)
		self.errorLeft.image = fire

		brain = ImageTk.PhotoImage(Image.open("emoji/brain.png"))
		brainLabel = tk.Label(titleFrame, image=brain, bg=BG_COLOUR)
		brainLabel.pack(side="left")
		brainLabel.image = brain

		fuck = ImageTk.PhotoImage(Image.open("emoji/fuck.png"))
		fuckLabel = tk.Label(titleFrame, image=fuck, bg=BG_COLOUR)
		fuckLabel.pack(side="left")
		fuckLabel.image = fuck

		self.errorRight = tk.Canvas(titleFrame, width=ERROR_SIZE, height=ERROR_SIZE,
			bg=BG_COLOUR, highlightbackground=BG_COLOUR)
		self.errorRight.pack(side="left", padx=50)
		self.errorRight.image = fire


	def createButtons(self):
		buttonFrame = tk.Frame(self.root, bg=BG_COLOUR)
		buttonFrame.pack(side="top", fill="both")
		buttonFrame.grid_columnconfigure(0, weight=5)
		buttonFrame.grid_columnconfigure(1, weight=3)

		leftFrame = tk.Frame(buttonFrame, bg=BG_COLOUR)
		leftFrame.grid(row=0, column=0)
		rightFrame = tk.Frame(buttonFrame, bg=BG_COLOUR)
		rightFrame.grid(row=0, column=1)

		buttonFrame.images = []
		def createImage(filename):
			image = Image.open("emoji/" + filename + ".png")
			image = ImageTk.PhotoImage(image.resize((40, 40), Image.ANTIALIAS))
			buttonFrame.images.append(image)
			return image

		floppy = createImage("floppy")
		up = createImage("up")
		down = createImage("down")
		run = createImage("run")
		stop = createImage("stop")

		self.createButton([floppy, down], leftFrame, self.save)
		self.createButton([floppy, up], leftFrame, self.load)

		self.startStopButton = self.createButton([run], rightFrame, self.startStop)
		self.startStopButton.startImage = run
		self.startStopButton.stopImage = stop
		self.startStopButton.isStart = True

	def createButton(self, images, frame, command):
		button = tk.Frame(frame, bg=BG_COLOUR, padx=5, pady=5,
			bd=2, relief="groove")
		
		for image in images:
			icon = tk.Label(button, image=image, bg=BG_COLOUR)
			icon.pack(side="left")
			icon.bind('<ButtonPress-1>', lambda e: self.buttonPress(button))
			icon.bind('<ButtonRelease-1>', lambda e: self.buttonRelease(button, command))
		button.pack(side="left", padx=30)
		button.bind('<ButtonPress-1>', lambda e: self.buttonPress(button))
		button.bind('<ButtonRelease-1>', lambda e: self.buttonRelease(button, command))
		
		return icon

	def buttonPress(self, button):
		button.config(relief="sunken")

	def buttonRelease(self, button, command):
		button.config(relief="groove")
		command()

	def save(self):
		f = filedialog.asksaveasfile(
			mode='w', initialdir="programs", defaultextension=".bf",
			filetypes=(("Brainfuck files", "*.bf"), ("All files", "*.*")))
		if f is None:
			return

		text = self.getCode(True)
		f.write(text)
		f.close()
	
	def load(self):
		f = filedialog.askopenfile(
			mode='r', initialdir="programs", defaultextension=".bf",
			filetypes=(("Brainfuck files", "*.bf"), ("All files", "*.*")))
		if f is None:
			return

		self.inputText.delete(1.0, tk.END)
		for line in f:
			for char in line:
				if char in COMMANDS:
					self.inputEmoji(COMMANDS.index(char))
				elif char in WHITESPACE:
					self.inputText.insert(tk.END, char)
		f.close()

	def startStop(self):
		if(self.startStopButton.isStart):
			self.run()
		else:
			self.stop()

	def run(self):
		self.outputText.config(state="normal")
		self.outputText.delete(1.0, tk.END)
		self.outputText.config(state="disabled")

		thread = Thread(target=interpreter.run, 
			args=(self.getCode(False), self, self.guiQueue, self.interpreterQueue))
		thread.start()

		self.startStopButton.config(image=self.startStopButton.stopImage)
		self.startStopButton.isStart = False

	def stop(self):
		interpreter.stop()
		self.returnEmoji(0)
		self.emojiFrame.pack_forget()

		self.startStopButton.config(image=self.startStopButton.startImage)
		self.startStopButton.isStart = True


	def defineEmoji(self):
		emoji = []
		for i in range(256):
			img = Image.open("emoji/" + str(i) + ".png")
			img = img.resize((25, 25), Image.ANTIALIAS)
			emoji.append(ImageTk.PhotoImage(img))
		return emoji


	def createTextboxes(self):
		textFrame = tk.Frame(self.root, bg=BG_COLOUR)
		textFrame.pack(side="top", expand=True, padx=10, pady=10, fill="both")
		textFrame.grid_columnconfigure(0, weight=5)
		textFrame.grid_columnconfigure(2, weight=3)
		textFrame.grid_rowconfigure(0, weight=1)
		textFrame.grid_propagate(False)

		self.inputText = self.createTextbox(textFrame, 0, True)
		self.bindKeys(self.inputText)

		self.outputText = self.createTextbox(textFrame, 2, False)
		self.outputText.config(state="disabled", wrap="char")

		self.outputText.update()
		self.emojiFrame = tk.Frame(self.inputText, bg=BG_COLOUR, bd=2, relief='ridge',
			width=self.inputText.winfo_width() * 1/3)
		self.emojiFrame.grid_propagate(False)
		for x in range(8):
			for y in range(32):
				emojiNum = y*8 + x
				self.emojiFrame.grid_columnconfigure(x, weight=1)
				self.emojiFrame.grid_rowconfigure(y, weight=1)
				emoji = tk.Label(self.emojiFrame, bg=BG_COLOUR, cursor='arrow',
					image=self.root.emoji[emojiNum])
				emoji.grid(row=y, column=x)
				emoji.bind('<ButtonPress-1>',
					lambda e, value=emojiNum: self.returnEmoji(value))

	def returnEmoji(self, value):
		self.emojiFrame.pack_forget()
		self.interpreterQueue.put(value)

	def createTextbox(self, frame, column, xScroll):
		text = tk.Text(frame, wrap="none", bd=3, relief="ridge", width=1,
			highlightbackground=BG_COLOUR, highlightcolor=BG_COLOUR,
			bg=TEXT_COLOUR, insertbackground='white')
		text.grid(row=0, column=column, sticky="nesw", padx=(10,0))

		if xScroll:
			xScrollbar = tk.Scrollbar(frame, command=text.xview, orient="horizontal",
				bg=TEXT_COLOUR, activebackground=BG_COLOUR, troughcolor=BG_COLOUR,
				bd=0, elementborderwidth=2)
			xScrollbar.grid(row=1, column=column, sticky='ew', padx=(15,5))
			text.config(xscrollcommand=xScrollbar.set)

		yScrollbar = tk.Scrollbar(frame, command=text.yview,
			bg=TEXT_COLOUR, activebackground=BG_COLOUR, troughcolor=BG_COLOUR, 
			bd=0, elementborderwidth=2)
		yScrollbar.grid(row=0, column=column+1, sticky='ns', padx=(0,10))
		text.config(yscrollcommand=yScrollbar.set)

		return text

	def bindKeys(self, text):
		text.bind('a', lambda e: self.inputEmoji(0))
		text.bind('s', lambda e: self.inputEmoji(1))
		text.bind('d', lambda e: self.inputEmoji(2))
		text.bind('f', lambda e: self.inputEmoji(3))
		text.bind('j', lambda e: self.inputEmoji(4))
		text.bind('k', lambda e: self.inputEmoji(5))
		text.bind('l', lambda e: self.inputEmoji(6))
		text.bind(';', lambda e: self.inputEmoji(7))
		text.bind('<Left>', self.doDefault)
		text.bind('<Right>', self.doDefault)
		text.bind('<Up>', self.doDefault)
		text.bind('<Down>', self.doDefault)
		text.bind('<BackSpace>', self.doDefault)
		text.bind('<Delete>', self.doDefault)
		text.bind('<Return>', self.doDefault)
		text.bind('<Tab>', self.doDefault)
		text.bind('<space>', self.doDefault)
		text.bind('<Key>', self.doNothing)

	def inputEmoji(self, index):
		self.inputText.image_create(tk.INSERT, 
			image=self.root.emoji[index], name=COMMANDS[index])
		return 'break'

	def doNothing(self, event):
		return 'break'

	def doDefault(self, event):
		pass

	def outputEmoji(self, index):
		self.outputText.image_create(tk.END, 
			image = self.root.emoji[index])


	def getCode(self, keepWhitespace=False):
		pos = "1.0"
		code = ""
		while True:
			try:
				char = self.inputText.get(pos)
				if char in WHITESPACE:
					if(keepWhitespace):
						code += char
				else:
					code += self.inputText.image_cget(pos, 'name')
				pos += "+1c"
			except:
				break

		if keepWhitespace:
			code = code[:-1]	# remove extra newline
		return code

	def getInput(self):
		self.emojiFrame.pack(side='right', fill='y', pady=5, padx=5)

	def displayError(self):
		self.errorLeft.create_image(ERROR_SIZE/2, ERROR_SIZE/2,
			image=self.errorLeft.image)
		self.errorRight.create_image(ERROR_SIZE/2, ERROR_SIZE/2,
			image=self.errorRight.image)
		self.errorLeft.after(2000, self.clearError)
		self.codeFinished()

	def clearError(self):
		self.errorLeft.delete("all")
		self.errorRight.delete("all")

	def codeFinished(self):
		self.startStopButton.config(image=self.startStopButton.startImage)
		self.startStopButton.isStart = True


	def checkQueue(self):
		while self.guiQueue.qsize():
			action = self.guiQueue.get(0)
			action()
		self.root.after(200, self.checkQueue)

	def onClosing(self):
		self.stop()
		self.root.destroy()
