import csv
import numpy as np
import os
import datetime
import linecache
import sys
from pprint import pprint

#Class for input generators

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

def print_output_to_file(output_matrix, directory_name, file_name):
	filepath = directory_name + "/" + file_name
	output_text = open(filepath, 'w')
	np.save(output_text, output_matrix)
	print "Output %s printed." % file_name


def remove_duplicates_from_list(list1): 
   # order preserving
   checked = []
   for x in list1:
       if x not in checked:
           checked.append(x)
   return checked


def create_dictionary_of_ratings(directory_name):
	"""
	INPUT: 
		directory_name: directory with ratings by movie

	OUTPUT: 
		movie_ratings_dictionary: ((movie_id, user_id), rating)
		movies_and_users_who_rated: (movie_id, [user_ids_who_rated)
	"""
	movie_ratings_dictionary = {} 
	files = os.listdir(directory_name)

	if files[0] == ".DS_Store":
		files.pop(0)

	movies_and_users_who_rated = {} #(key, value) = (movie_id, [users_rated])

	
	for j in xrange(len(files)):

		movie_id = j + 1
		movie_id_string = "%07d" % movie_id
		filepath = directory_name + "/" + "mv_" + movie_id_string +".txt"
		list_of_users_who_rated_movie = []

		if file_len(filepath) <2:
			pass
		else: 
			for i in xrange(2,file_len(filepath)+1):
				individual_rating = linecache.getline(filepath, i).split(",")

		
				user_id = int(individual_rating[0])	
				rating = int(individual_rating[1])

				list_of_users_who_rated_movie.append(user_id)

				key = (movie_id, user_id)
				movie_ratings_dictionary[key] = rating

		movies_and_users_who_rated[movie_id] = list_of_users_who_rated_movie
		linecache.clearcache()

	return movie_ratings_dictionary, movies_and_users_who_rated


def calculate_common_users_of_both_movies(movie1, movie2, movies_and_users_who_rated):
	common_users = movies_and_users_who_rated[movie1]
	common_users = list(set(common_users).intersection(movies_and_users_who_rated[movie2]))
		#set.intersection: Return a new set with elements common to the set and all others.
	return len(common_users)

def index_of_list_max(list1):
	max_item = None
	max_index = None
	for i in range(len(list1)):
		if list1[i] > max_item:
  			max_item = list1[i]
  		max_index = i
	return max_index


def make_neighborhoods_from_movie(movies_and_users_who_rated, 
	list_of_movies_that_define_neighborhood, num_neighborhoods, max_size_of_neighborhood):

	'''
	INPUT:
		movies_and_users_who_rated[movie_id] = list of users who rated
		list_of_movies_that_define_neighborhood = list of movies with most ratings, 
			shorted to the number of neighborhoods
		num_neighorhoods = number of neighborhoods

	CREATED:
		neighborhoods = List of lists. Index indicates which number of neighbohood, 
			inside list is of movies within that neighborhood


	OUTPUT: 
		movies_and_neighborhood = dictionary where key = movie that defined neighborhood
			value = neighborhood[index] corresponding to that movies_and_neighborhood

	'''

	neighborhoods =[[] for x in xrange(num_neighborhoods)] #list of neighborhoods
	movies_and_neighborhood = {}
	list_of_movies_that_define_neighborhood = list_of_movies_that_define_neighborhood[0:num_neighborhoods]

	for i in range(num_neighborhoods):
		movies_and_neighborhood[list_of_movies_that_define_neighborhood[i]] = neighborhoods[i]


	movies_and_users_who_rated.pop(0, None)
	movies = movies_and_users_who_rated.items()

	for movie in movies:
		movie_id = movie[0]
		common_users_score = []

		for i in range(len(list_of_movies_that_define_neighborhood)):

			common_users = calculate_common_users_of_both_movies(movie_id, list_of_movies_that_define_neighborhood[i],
								 movies_and_users_who_rated)
			common_users_score.append(common_users)

		for i in range(len(list_of_movies_that_define_neighborhood)):
			best_match_index = int(index_of_list_max(common_users_score))
			best_match = list_of_movies_that_define_neighborhood[best_match_index]

			if len(movies_and_neighborhood[best_match])<max_size_of_neighborhood:
				movies_and_neighborhood[best_match].append(movie_id)
			else: 
				common_users_score.pop(best_match_index)


	return movies_and_neighborhood


def matrix_factorization_from_file(neighborhood, K, iterations, alpha, beta,
	 num_users, ratings_dictionary):
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

	num_movies = len(neighborhood)

	movie_and_index_in_neighborhood = {}

	P = np.random.rand(num_movies, K)
	Q = np.random.rand(num_users, K)

	Q = Q.T #transpose Q

	for step in xrange(iterations):
		for i in xrange(num_movies): 

			movie_id = neighborhood[i]

			movie_and_index_in_neighborhood[movie_id] = i 
			

			for j in xrange(num_users):

				rating = ratings_dictionary.get((movie_id, j+1), 0)

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

	movie_and_index_in_neighborhood

	return P, Q.T, movie_and_index_in_neighborhood


def create_dictionary_of_predicted_ratings (P, Q, movies_and_index_in_neighborhood, num_users):

	predicted_ratings_dictionary = {}
	predicted_ratings_matrix = np.dot(P, Q.T)
	predicted_raings_matrix = np.around(predicted_ratings_matrix, decimals = 1)
	movies_in_neighborhood = movies_and_index_in_neighborhood.items()

	for movie in movies_in_neighborhood:
		movie_id = movie[0]
		row_in_matrix = movie[1]

		for i in range(num_users):

			user_id = i
			rating = predicted_ratings_matrix[row_in_matrix][i]

			key = (movie_id, user_id)

			predicted_ratings_dictionary[key] = rating

	return predicted_ratings_dictionary


def main(): 

	start_time=datetime.datetime.now()

	np.set_printoptions(precision=2)


	print "***********************************************************"
	print "Total Time Elapsed: %s" % time_elapsed


if __name__ == '__main__':
	main()