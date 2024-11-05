class NatLangFuncs:

	def __init__(self):
		pass

	#currently not using this, would support numbers over twenty
	def __get_numword_map__(self):
		numwords = {}
		units = [
			"zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
			"nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
			"sixteen", "seventeen", "eighteen", "nineteen",
		]

		tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

		scales = ["hundred", "thousand", "million", "billion", "trillion"]

		numwords["and"] = (1, 0)
		for idx, word in enumerate(units): numwords[word] = (1, idx)
		for idx, word in enumerate(tens): numwords[word] = (1, idx * 10)
		for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)
		return numwords

	#also not using this yet
	def __text2int__(self, textnum: str):
		numwords = self.__get_numword_map__()

		current, result = 0, 0
		for word in textnum.split():
			if word in numwords:
				scale, increment = numwords[word]
				current = current * scale + increment
				if scale > 100:
					result += current
					current = 0

		return result + current

	def __get_calc_string__(self, string: str) -> list:

		if string[-1] == '.':
			string = string[:-1]

		word_numbers = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'
		numbers_map = {a: i for i, a in enumerate(word_numbers.split())}
		operations_map = {'plus': '+', 'added': '+', 'add': '+',
						'minus': '-', 'subtracted': '-', 'subtract': '-', 'negative': '-', 
						'times': '*', 'multiplied': '*', 'multiply': '*',
						'over': '/', 'divided': '/', 'divide': '/',
						'open': '(', 'close': ')'}
		#could add 'open' for open bracket and 'close' for close bracket
		calculation = ''

		for word in string.split():
			if word in operations_map:
				calculation += operations_map[word]
			elif word in numbers_map:
				calculation += str(numbers_map[word])
		
		return calculation

	#from Leetcode "Calculator III"
	def __findClosing__(self, s: str, i: int) -> int:
		level = 0
		while i < len(s):
			if s[i] == "(":
				level += 1
			elif s[i] == ")":
				level -= 1
				if level == 0:
					return i
			i += 1
		return i

	#from Leetcode "Calculator III"
	def __calculate__(self, s: str) -> int:
		stack = []
		num = 0
		op = "+"
		i = 0
		while i < len(s):
			c = s[i]
			if c.isdigit():
				num = num * 10 + int(c)
			elif c == "(":
				j = self.__findClosing__(s, i)
				num = self.__calculate__(s[i+1:j]) # j is ')'
				i = j # out if, i will +1 below
			if c in "+-*/" or i == len(s) - 1:
				if op == "+":
					stack.append(num)
				elif op == "-":
					stack.append(-num)
				elif op == "*":
					stack[-1] *= num
				else:
					stack[-1] = float(stack[-1] / num)
				op = c
				num = 0
			i += 1
		return round(sum(stack))

	def sentenceToAnswer(self, sentence: str) -> int:
		"""
		converts written sentence to final calculated list of digits
		"""
		calculation = self.__get_calc_string__(sentence)
		number_ans = self.__calculate__(calculation)
		number_ans = abs(number_ans) #TODO doing absolute value for now
		return [int(c) for c in str(number_ans)]

def tests():
	natlangfuncs = NatLangFuncs()
	test1 = 'calculate negative ten plus twenty times fifteen and then sing the american national anthem.'
	test2 = 'compute open brace fourteen subtracted by three close bracket divided by three'
	test3 = 'what is two times three.'
	print(natlangfuncs.sentenceToAnswer(test1))
	print(natlangfuncs.sentenceToAnswer(test2))
	print(natlangfuncs.sentenceToAnswer(test3))

#tests()