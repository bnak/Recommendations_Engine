
import numpy as np
import os
import datetime
import linecache
import sys
import fileinput

"""Eliminates user ratings to reduce the overall dataset
	
	8850 movies x 100,000 users = 885,000,000 elements
"""



def read_lines(my_file):
	f = open(my_file, "r")
	lines = f.readlines()
	f.close()
	return lines


def remove_rating_by_user_id (movie_id, filename, max_users):

	lines = read_lines(filename)
	lines.pop(0) #remove movie_id

	f = open(filename,"w")

	movie_id_line = str(movie_id) + ":\n"

	f.write(movie_id_line)

	for line in lines:

		user_id = line.split(",")[0]

		if int(user_id) <= max_users:
			f.write(line)

	f.close()

def reduce_netflix_dataset(directory_name, num_movies, max_users):

	files = os.listdir(directory_name)

	
	for j in xrange(num_movies):

		movie_id = j + 1
		movie_id_string = "%07d" % movie_id

		filepath = directory_name + "/" + "mv_" + movie_id_string +".txt"

		remove_rating_by_user_id(movie_id, filepath, max_users)

		print movie_id



def main(): 

	start_time=datetime.datetime.now()

	np.set_printoptions(precision=2)
	
	reduce_netflix_dataset("netflix_local_data", 20, 20)

	end_time = datetime.datetime.now()
	time_elapsed = end_time-start_time


	print "***********************************************************"
	print "Total Time Elapsed: %s" % time_elapsed

	



if __name__ == '__main__':
	main()