
from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np
import os
import datetime
import linecache
import sys


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

	print output_matrix


	filepath = directory_name + "/" + file_name

	output_text = open(filepath, 'w')

	np.save(output_text, output_matrix)

	#output_matrix.tofile(output_text, "\n", "%d")


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

		#best_match=list_of_movies_that_define_neighborhood[2]

		#movies_and_users_who_rated[0] = []

		common_users_score = []


		for i in range(len(list_of_movies_that_define_neighborhood)):

			#best_match_score = calculate_common_users_of_both_movies(movie_id, best_match, movies_and_users_who_rated)

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

class MR_build_matrix(MRJob):

	def __init__(self, *args, **kwargs):
		super(MR_build_matrix, self).__init__(*args, **kwargs)
		self.ratings_dictionary = {}#np.load("movie_ratings_dictionary_NLD").item() #needs to be loaded from input file
		self.movies_and_users_who_rated = {}#np.load("movies_and_users_who_rated_NLD").item() #needs to be loaded from input file
		self.num_movies = 20 #static int - hardcoded
		self.num_users = 30 #static int - hardcoded

		self.list_of_movies_that_define_neighborhood = [1,2,3,4] #list of movies with most ratings - hardcoded or read in from file
		self.num_neighborhoods = 2 #static int - hardcoded
		self.max_size_of_neighborhood = 10 #static int- hardcoded


		#parameters hardcoded for matrix factorization
		self.K=2 
		self.iterations=5000
		self.alpha=.0002
		self.beta=.0002



	def mapper_build_neighborhoods(self, _, movies):
		#yields (out_key, out_value) = (neighborhood, movies)

		movies_and_neighborhood = build_matrix.make_neighborhoods_from_movie(
										self.movies_and_users_who_rated, 
										self.list_of_movies_that_define_neighborhood, 
										self.num_neighborhoods, 
										self.max_size_of_neighborhood)


		for key in movies_and_neighborhood.iterkeys():


			for movie in movies_and_neighborhood[key]:

				value = movie

				#yield (neighborhood number, movie)
				yield (key, value)



	def reducer_create_matrix(self, neighborhood, movie): 

		movies_in_neighborhood = list(movie)  
		movies_in_neighborhood = build_matrix.remove_duplicates_from_list(movies_in_neighborhood)


		P, Q, movies_and_index_in_neighborhood = build_matrix.matrix_factorization_from_file(movies_in_neighborhood, 
			self.K, self.iterations, self.alpha, self.beta, self.num_users, self.ratings_dictionary)



		predicted_ratings_dictionary = build_matrix.create_dictionary_of_predicted_ratings (P, Q, movies_and_index_in_neighborhood, self.num_users)

		for item in predicted_ratings_dictionary.items():
			#yield ((movie_id, user_id), predicted rating)
			yield item

	def steps(self):

		return [
            MRStep(mapper=self.mapper_build_neighborhoods,
                   reducer=self.reducer_create_matrix)
        ]




def main():

	MR_build_matrix.run() #where MR_build_matrix is the job class









if __name__ == '__main__':
	main()