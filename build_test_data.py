
import random
import os

'''This file is to quickly build sample test data by outputing text files
with randomized data and check computational speed'''
#Time points for different sizes:
	# 50x50
	# 100x100
	# 300x300
	# 500x500
	# 800x800
	# 1000x1000


def check_lines(my_file, max_user_number, new_file):

	f = open(my_file)

	lines = f.readlines()
	lines.pop(0)

	f.close()
	test_data = open(new_file, 'w')

	for line in lines:
		individual_rating = line.split(",")
		user_id = int(individual_rating[0])	

		if user_id <= max_user_number: 
			test_data.write(line)

	test_data.close()


def make_lines(max_user_number, new_file, movie_id):

	test_data = open(new_file, 'w')


	movie_id_line = "%s:\n" % movie_id
	test_data.write(movie_id_line)

	for i in range(max_user_number):


		if i%5 == 0: #To determine what percentage ratings exist
			line = "%s,%s,date\n" % ((i+1), (random.randint(0, 5)))

			test_data.write(line)

		else: 
			pass

			

	test_data.close()


def create_file(max_movie_number, directory_name, max_user_number, test_size):
	
	if not os.path.exists(test_size):
	    os.makedirs(directory_name + "/" + test_size)


	for i in range(max_movie_number):

		filepath = directory_name + "/" + test_size +"/"+ str(i+1)
		movie_id = str(i+1)

		make_lines(max_user_number, filepath, movie_id)



def main():

	create_file(max_movie_number=50, directory_name = "time_test_data",
		 max_user_number=50, test_size = "50x50")




if __name__ == '__main__':
	main()