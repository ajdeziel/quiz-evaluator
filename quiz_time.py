'''
quiz_time.py
Author: Alain-Joseph Po-Deziel
SENG265 - Assignment 3
'''


import libxml2
import sys
import quiz_library

'''
purpose
	Accept 1 or more log file names on the command line.

	For each log file, compute the total time taken for each question. 

	Write to standard output, the average time spent for each question.
preconditions
	Each command-line argument is the name of a readable and
	legal quiz log file.

	All the log_files have the same number of questions.
'''

# handle command line arguments
if len(sys.argv) < 2:
	print 'Syntax:', sys.argv[0], 'quiz_log_file ...'
	sys.exit()

log_file = quiz_library.load_quiz_log(sys.argv[1])
question_count = quiz_library.compute_question_count(log_file)
time_stamps = [0] * question_count #initialse list to store times taken for each question, for length of number of questions

#Iterate through each file on command line
for i in sys.argv[1:]:
	
	quiz_log = quiz_library.load_quiz_log(i)
	questions = quiz_library.compute_question_count(quiz_log)
	time_final, time_prev = None, None
	display_items = [x for x in quiz_log if isinstance(x, quiz_library.Display)] #retrieve all elements that are Display instances
	
	#Iterate through an enumeration of display_items
	for index, log_item in enumerate(display_items):
		time_prev = time_final
		time_final = log_item
		
		#Case 1: Previous time returns None
		if time_prev == None:
			continue
		
		time_stamps[time_prev.index] += time_final.time - time_prev.time #store time taken to complete question in time_stamps
		
		#Case 2: Element at end of file
		if index == len(display_items) - 1:
			time_prev = time_final
			time_final = quiz_log[-1]
			time_stamps[time_prev.index] += time_final.time - time_prev.time #store time taken to complete question in time_stamps

			
#Calculate list of average completion times for each question
final_avg = [float(time_final)/(len(sys.argv) - 1) for time_final in time_stamps]


'''
The following lines prints final_avg in CSV format
with a special condition for its first element
'''
output = '' + str(final_avg[0])

for i in final_avg[1:len(final_avg)]:
	output = output + ',' + str(i)

print output