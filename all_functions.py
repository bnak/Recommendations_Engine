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
 

def create_dictionary_of_ratings(directory_name, movie_ratings_dictionary):

	files = os.listdir(directory_name)

	files.pop(0)  #first entry is ds.store

	#individual_rating = linecache.getline(filepath, line_num).split(",")

	movies_and_users_who_rated = {} #(key, value) = (movie_id, [users_rated])

	
	for j in xrange(len(files)):

		movie_id = j + 1
		movie_id_string = "%07d" % movie_id
		#filepath = directory_name + "/" + files[movie_id-1]
		#ratings = read_movie_rating(filepath)
		filepath = directory_name + "/" + "mv_" + movie_id_string +".txt"

		list_of_users_who_rated_movie = []
		print movie_id


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


def calculate_number_of_users_who_rated_all_movies(movie_list, movies_and_users_who_rated):

	common_users = movies_and_users_who_rated[movie_list[0]]

	for j in range(len(movie_list)):

		i = j+1

		movie_i_ratings = movies_and_users_who_rated[i]

		common_users = list(set(common_users).intersection(movie_i_ratings))


	return len(common_users)



def calculate_common_users_of_both_movies(movie1, movie2, movies_and_users_who_rated):

	common_users = movies_and_users_who_rated[movie1]


	common_users = list(set(common_users).intersection(movies_and_users_who_rated[movie2]))


	return len(common_users)




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
	movies_and_neighborhood = dictionary where key = movie that defined neighborhood
		value = neighborhood[index] corresponding to that movies_and_neighborhood

	OUTPUT: 
	neighborhoods


	'''

	neighborhoods =[[] for x in xrange(num_neighborhoods)] #list of neighborhoods

	movies_and_neighborhood = {}


	list_of_movies_that_define_neighborhood = list_of_movies_that_define_neighborhood[0:num_neighborhoods]


	for i in range(num_neighborhoods):
		movies_and_neighborhood[list_of_movies_that_define_neighborhood[i]] = neighborhoods[i]


	list_of_movies_that_define_neighborhood = list_of_movies_that_define_neighborhood[0:num_neighborhoods]

	movies_and_users_who_rated.pop(0, None)

	
	movies = movies_and_users_who_rated.items()



	for movie in movies:
		movie_id = movie[0]
		#print movie_id

		best_match=1

		movies_and_users_who_rated[0] = []


		for item in list_of_movies_that_define_neighborhood:

			best_match_score = calculate_common_users_of_both_movies(movie_id, best_match, movies_and_users_who_rated)

			common_users = calculate_common_users_of_both_movies(movie_id, item, movies_and_users_who_rated)

			if common_users > best_match_score:

				if len(movies_and_neighborhood[item])<max_size_of_neighborhood:
					best_match = item

		movies_and_neighborhood[best_match].append(movie_id)




	return movies_and_neighborhood

def remove_duplicates_from_list(list1): 
   # order preserving
   checked = []
   for x in list1:
       if x not in checked:
           checked.append(x)
   return checked

                                                     
 



def main(): 

	start_time=datetime.datetime.now()

	np.set_printoptions(precision=2)

	# K=2 
	# iterations=5000
	# alpha=.0002
	# beta=.0002
	# num_users = 30

	dictionary = {}
	movie_ratings_dictionary, movies_and_users_who_rated = create_dictionary_of_ratings("training_set", dictionary)


	# P, Q, movies_and_index_in_neighborhood = matrix_factorization_from_file(neighborhood_tuple, K, iterations, alpha, beta,
	#  num_users, num_movies, ratings_dictionary)
	print_output_to_file(movie_ratings_dictionary, "Test_output", "movie_ratings_dictionary_full")
	print_output_to_file(movies_and_users_who_rated, "Test_output", "movies_and_users_who_rated_full")





	end_time = datetime.datetime.now()
	time_elapsed = end_time-start_time

	print "***********************************************************"
	print "Total Time Elapsed: %s" % time_elapsed

	



if __name__ == '__main__':
	main()