'''
quiz_marks.py
Author: Alain-Joseph Po-Deziel
SENG265 - Assignment 3
'''


import libxml2
import sys
import quiz_library

'''
purpose
	Accept 1 or more log file names on the command line.
	For each log file
		write to standard output the course mark for the log file,
		in CSV format
preconditions
	Each command-line argument is the name of a legal, readable quiz log file.
'''

# handle command line arguments
if len(sys.argv) < 2:
	print 'Syntax:', sys.argv[0], 'quiz_log_file ...'
	sys.exit()

#retrieve target files
target_file = sys.argv[1:]

for quiz in target_file:
	load_file = quiz_library.load_quiz_log(quiz)
	quiz_mark_list = quiz_library.compute_mark_list(load_file)
	quiz_total = reduce(lambda x, y: x + y, quiz_mark_list) #Get total mark
	
	print quiz + ',' + str(quiz_total)