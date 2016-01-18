import libxml2
import sys

'''
purpose
	store the information from an answer element
'''
class Answer:
	def __init__(self, index, path, result, answer, time):
		self.index = index
		self.path = path
		self.result = result
		self.answer = answer
		self.time = time

'''
purpose
	Store the information from a display element.
'''
class Display:
	def __init__(self, index, path, time):
		self.index = index
		self.path = path
		self.time = time

'''
purpose
	Extract the information from log_file and return it as a list
	of answer and display objects.
preconditions
	log_file is the name of a legal, readable quiz log XML file
'''
def load_quiz_log(log_file):
	#Parse XML log file
	parse_tree = libxml2.parseFile(log_file)
	context = parse_tree.xpathNewContext()
	root = parse_tree.getRootElement()

	quiz_info = []
	elementChild = root.children
	
	#Iterate through children of root
	while elementChild is not None:
		child = elementChild.children
		quiz_index, quiz_path, quiz_result, quiz_answer, quiz_time = None, None, None, None, None
		
		#Case 1: Answer tag
		if elementChild.name == 'answer':
			while child is not None:
				if child.name == 'index':
					quiz_index = int(child.content)
				elif child.name == 'path':
					quiz_path = child.content
				elif child.name == 'result':
					if child.content.isdigit():
						quiz_result = int(child.content)
					else:
						quiz_result = None
				elif child.name == 'answer':
					if child.content == '':
						quiz_answer = None
					else:
						quiz_answer = child.content
				elif child.name == 'time':
					if child.content.isdigit():
						quiz_time = int(child.content)
					else:
						quiz_time = None
				child = child.next
			info = Answer(quiz_index, quiz_path, quiz_result, quiz_answer, quiz_time)
			quiz_info.append(info)
		
		#Case 2: Display tag
		if elementChild.name == 'display':
			while child is not None:
				if child.name == 'index':
					quiz_index = int(child.content)
				elif child.name == 'path':
					quiz_path = child.content
				elif child.name == 'time':
					if child.content.isdigit():
						quiz_time = int(child.content)
					else:
						quiz_time = None
				child = child.next
			disp = Display(quiz_index, quiz_path, quiz_time)
			quiz_info.append(disp)
			
		elementChild = elementChild.next
	return quiz_info #Return elements in list quiz_info

'''
purpose
	Return the number of distinct questions in log_list.
preconditions
	log_list was returned by load_quiz_log
'''
def compute_question_count(log_list):
	questions_seen = []
	
	#Iterate through log_list
	for element in log_list:
		if element.index not in questions_seen:
			questions_seen.append(element.index) #If question number is not yet in list, append
	return len(questions_seen) #number of distinct questions in log_list

'''
purpose
	Extract the list of marks.
	For each index value, use the result from the last non-empty answer,
	or 0 if there are no non-empty results.
preconditions
	log_list was returned by load_quiz_log
'''
def compute_mark_list(log_list):
	mark_list = [0] * compute_question_count(log_list)
	
	#Iterate through log_list
	for element in log_list:
		if isinstance(element, Answer): #If element encounters a class Answer
			if element.result is not None:
				mark_list[element.index] = element.result #Take result in class Answer and store in mark_list
	return mark_list #return list of marks