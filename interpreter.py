from collections import deque
import time

def run(code, gui, guiQueue, responseQueue):
	bracketMap = makeBracketMap(code)
	if bracketMap is None:
		guiQueue.put(gui.displayError)
		return

	stack = deque([0])
	instPtr = 0
	stackPtr = 0

	global killed
	killed = False

	while instPtr < len(code) and killed == False:
		if code[instPtr] == '<':
			if stackPtr > 0:
				stackPtr -= 1
			else:
				stack.appendleft(0)

		elif code[instPtr] == '>':
			stackPtr += 1
			if stackPtr >= len(stack):
				stack.append(0)

		elif code[instPtr] == '+':
			stack[stackPtr] += 1
			if stack[stackPtr] > 255:
				stack[stackPtr] = 0

		elif code[instPtr] == '-':
			stack[stackPtr] -= 1
			if stack[stackPtr] < 0:
				stack[stackPtr] = 255

		elif code[instPtr] == '[':
			if not stack[stackPtr]:
				instPtr = bracketMap[instPtr]

		elif code[instPtr] == ']':
			if stack[stackPtr]:
				instPtr = bracketMap[instPtr]

		elif code[instPtr] == '.':
			guiQueue.put(lambda emoji=stack[stackPtr]: gui.outputEmoji(emoji))

		elif code[instPtr] == ',':
			guiQueue.put(gui.getInput)
			stack[stackPtr] = responseQueue.get()

		instPtr += 1

	guiQueue.put(gui.codeFinished)

def makeBracketMap(code):
	bracketMap = {}
	openBrackets = []

	for i, char in enumerate(code):
		if char == '[':
			openBrackets.append(i)
		elif char == ']':
			if not openBrackets:
				return None
			match = openBrackets.pop()
			bracketMap[i] = match
			bracketMap[match] = i

	if openBrackets:
		return None

	return bracketMap


def stop():
	global killed
	killed = True