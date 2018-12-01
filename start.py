#! /usr/bin/python3

from emojiCoder import EmojiCoder
import tkinter as tk
from PIL import Image, ImageTk

class EmojiCoding(tk.Tk):
	
	def __init__(self, *args, **kwargs):
		
		tk.Tk.__init__(self, *args, **kwargs)
		self.geometry("%dx%d+0+0" % (self.winfo_screenwidth(), self.winfo_screenheight()))
		
		self.after(100, lambda: EmojiCoder(self))
		
app = EmojiCoding()
app.mainloop()
