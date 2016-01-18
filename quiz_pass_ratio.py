import libxml2
import sys
import quiz_library

'''
purpose
	Accept 1 or more log file names on the command line.

	Accumulate across all the log files the pass ratio for each question.

	A question result is considered a pass if it is not 0 or None
	and fail otherwise.

	The pass ratio for a question is the number of passes
	divided by the number of passes + fails.
preconditions
	Each command-line argument is the name of a
	readable and legal quiz log file.

	All the log_files have the same number of questions.
'''

# check number of command line arguments
if len(sys.argv) < 2:
	print 'Syntax:', sys.argv[0], 'quiz_log_file ...'
	sys.exit()

target = len(sys.argv) - 1
question_total = 0
list_marks = []

#iterate for length of total questions in XML files
while question_total != quiz_library.compute_question_count(quiz_library.load_quiz_log(sys.argv[target])):
	correct_answers = 0.0
	for i in sys.argv[1:]:
		count = 0
		log = quiz_library.load_quiz_log(i)
		
		#Check for every question in log
		for quiz in log:
			if isinstance(quiz, quiz_library.Answer):		
				if (int(quiz.index) == question_total):					
					if (str(quiz.result) == '1'): #Make count true when question is answered correctly
						count = 1
						
		if (count == 1):
			correct_answers += 1 #Increment when correct answer is found
	
	pass_ratio = correct_answers / target
	list_marks.append(pass_ratio)
	question_total += 1 #Increment total questions visited

	
'''
The following lines prints list_marks in CSV format
with a special condition for its first element
'''
output = '' + str(list_marks[0])

for i in list_marks[1:len(list_marks)]:
	output = output + ',' + str(i)

print output
