import csv
import numpy as np
import os
import datetime
import linecache
import sys

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
	return i+1


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


			for j in xrange(num_users):

				rating = ratings_dictionary.get((i, j), 0)


				if rating > 0:
					eij = rating - np.dot(P[i,:], Q[:,j])
					for k in xrange(K):
						P[i][k] = P[i][k] + alpha * (2 * eij *Q[k][j] - beta * P[i][k])
						
						Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])

		error_prime = 0 

		for i in xrange(num_movies):
			for j in xrange(num_users):
				if rating>0:
					error_prime = error_prime + pow(A[i][j] - np.dot(P[i,:], Q[:,j]),2)
					for k in xrange(K):
						error_prime = error_prime + (beta/2) * (pow(P[i][k],2)+pow(Q[k][j],2))
			if error_prime < 0.001:
				break

	return P, Q.T

def create_dictionary_of_ratings(directory_name, movie_id, movie_ratings_dictionary):

	 

	files = os.listdir(directory_name)

	files.pop(0)  #first entry is ds.store

	filepath = directory_name + "/" + files[movie_id-1]

	#individual_rating = linecache.getline(filepath, line_num).split(",")

	ratings = read_movie_rating(filepath)

	for i in xrange(2,file_len(filepath)):
		individual_rating = linecache.getline(filepath, i).split(",")
		user_id = int(individual_rating[0])	

		rating = int(individual_rating[1])

		key = (movie_id, user_id)
		movie_ratings_dictionary[key] = rating



	return movie_ratings_dictionary



def calculate_prediction(directory_name, movie_id, user_id, num_movies, num_users): 

	ratings = {}

	ratings = create_dictionary_of_ratings(directory_name, movie_id, ratings)



	P, Q = matrix_factorization_from_file(directory_name=directory_name, 
		K=2, iterations=5000, alpha=.0002, beta=.0002, 
		num_users=30, ratings_dictionary=ratings)

	
	vector_2 = [Q[user_id]]


	predicted_rating = np.dot(P[movie_id], vector_2[0].T)



	return predicted_rating


def retrieve_rating(directory_name, movie_id, user_id, num_movies, num_users):

	ratings = {}

	ratings_dictionary = create_dictionary_of_ratings(directory_name, movie_id, ratings)

	individual_rating = ratings_dictionary.get((movie_id, user_id), 0)

	if individual_rating>0: 

		print "Previously rated: %s" % individual_rating
		return individual_rating

	else: 
		individual_rating = calculate_prediction(directory_name, movie_id, user_id, num_movies, num_users)

		print "Predicted rating: %s" % individual_rating






def main(): 

	start_time=datetime.datetime.now()

	movie_ratings_dictionary = {}  

	#(movie i, user j) = rating
	movie_id = 3
	user_id = 29



	retrieve_rating("netflix_local_data", movie_id, user_id, 20, 30)





	end_time = datetime.datetime.now()

	time_elapsed = end_time-start_time

	print "Total Time Elapsed: %s" % time_elapsed

	



if __name__ == '__main__':
	main()