import csv
import numpy as np
import os
import datetime
import linecache
import sys
from pprint import pprint

#Time points for different sizes:
	# 50x50
	# 100x100
	# 300x300
	# 500x500
	# 800x800
	# 1000x1000

"""
xrange only available in Python 2.7; generator for iteration rather than creating a list
Matrix: rows x columns
Ratings: Movies x Users

"""


def read_movie_rating(my_file):
	f = open(my_file)
	lines = f.readlines()
	f.close()
	return lines


def file_len(my_file):

	with open(my_file) as f:
		for i, l in enumerate(f):
			pass
		return (i+1)


def create_dictionary_of_ratings(directory_name, movie_ratings_dictionary):

	files = os.listdir(directory_name)

	files.pop(0)  #first entry is ds.store

	#individual_rating = linecache.getline(filepath, line_num).split(",")

	
	for j in xrange(len(files)):

		movie_id = j + 1
		filepath = directory_name + "/" + files[movie_id-1]
		ratings = read_movie_rating(filepath)


		for i in xrange(2,file_len(filepath)):
			individual_rating = linecache.getline(filepath, i).split(",")

	
			user_id = int(individual_rating[0])	
			rating = int(individual_rating[1])

			key = (movie_id, user_id)
			movie_ratings_dictionary[key] = rating


	return movie_ratings_dictionary

def matrix_factorization_from_file(directory_name, K, iterations, alpha, beta, num_users, ratings_dictionary):
	"""

	INPUT:
	    A     : a matrix to be factorized, dimension M x N
	    K     : the number of latent features
	    iterations : the maximum number of iterations toward optimization
	    alpha : the learning rate
	    beta  : the regularization parameter

	CREATES: 
	    P     : an initial matrix of dimension M x K (movies x features)
	    Q     : an initial matrix of dimension N x K (users x features)

	"""

	files = os.listdir(directory_name)
	files.pop(0)  #removes first entry of ds.store

	num_movies = len(files)

	P = np.random.rand(num_movies, K)
	Q = np.random.rand(num_users, K)

	Q = Q.T #transpose Q

	for step in xrange(iterations):
		for i in xrange(num_movies): 
			i = i

			for j in xrange(num_users):


				rating = ratings_dictionary.get((i+1, j+1), 0)



				if rating > 0:
					eij = rating - np.dot(P[i,:], Q[:,j])
					for k in xrange(K):
						P[i][k] = P[i][k] + alpha * (2 * eij *Q[k][j] - beta * P[i][k])
						
						Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])

		error_prime = 0 

		for i in xrange(num_movies):
			for j in xrange(num_users):
				if rating>0:
					error_prime = error_prime + pow(rating - np.dot(P[i,:], Q[:,j]),2)
					for k in xrange(K):
						error_prime = error_prime + (beta/2) * (pow(P[i][k],2)+pow(Q[k][j],2))
			if error_prime < 0.001:
				break

	return P, Q.T






def retrieve_rating(ratings_dictionary, movie_id, user_id, ratings_matrix):
	
	#pprint(ratings_dictionary)

	key = (movie_id, user_id)

	individual_rating = (ratings_dictionary.get(key, 0))
	print individual_rating

	if individual_rating>0: 

		print "Previously rated: %s" % individual_rating

		predicted = (ratings_matrix[movie_id-1][user_id-1])

		print "Predicted: %s" % predicted

		#print "Error: %s" % int(individual_rating-predicted)
		return individual_rating

	else: 
		individual_rating = ratings_matrix[movie_id-1][user_id-1]

		print "Predicted rating: %s" % individual_rating
		return individual_rating


def see_rating(ratings_dictionary, movie_id, user_id, ratings_matrix): 

	print "**************************************************"

	print "Movie_id: %s" % movie_id
	print "User_id: %s" % user_id


	retrieve_rating(ratings_dictionary, movie_id, user_id, ratings_matrix)

	print "\n"

def print_output_to_file(output_matrix, directory_name, file_name):

	print output_matrix


	filepath = directory_name + "/" + file_name

	output_text = open(filepath, 'w')

	np.save(output_text, output_matrix)

	#output_matrix.tofile(output_text, "\n", "%d")


	print "Output printed."






def test_data_set(test_name, directory_name, K, iterations, alpha, beta, num_users):

	start_time=datetime.datetime.now()


	movie_ratings_dictionary = {}  


	movie_ratings_dictionary = create_dictionary_of_ratings(directory_name, movie_ratings_dictionary)




	pprint(movie_ratings_dictionary)

	P, Q = matrix_factorization_from_file(directory_name, 
		K, iterations, alpha, beta,
		num_users, movie_ratings_dictionary)

	ratings_matrix = np.dot(P, Q.T)

	print_output_to_file(ratings_matrix, directory_name, test_name)

	


	end_time = datetime.datetime.now()

	time_elapsed = end_time-start_time



	see_rating(movie_ratings_dictionary, 1, 3, ratings_matrix)



	print test_name
	print "Test Time Elapsed: %s" % time_elapsed
	print "\n"
	print "\n"









def main(): 

	start_time=datetime.datetime.now()

	np.set_printoptions(precision=2)

	K=2 
	iterations=5000
	alpha=.0002
	beta=.0002



	#test_data_set("100x100", "time_test_data/100x100", K, iterations, alpha, beta, 100)

	#test_data_set("800x800", "time_test_data/800x800", K, iterations, alpha, beta, 800)

	#test_data_set("1000x1000", "time_test_data/1000x1000", K, iterations, alpha, beta, 1000)

	test_data_set("Test", "netflix_local_data", K, iterations, alpha, beta, 30)

	# x = np.load("time_test_data/50x50/50x50")

	# print x








	end_time = datetime.datetime.now()
	time_elapsed = end_time-start_time

	print "***********************************************************"
	print "Total Time Elapsed: %s" % time_elapsed

	



if __name__ == '__main__':
	main()