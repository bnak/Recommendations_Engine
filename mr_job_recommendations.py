
from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np
import os
import datetime
import linecache
import sys
import build_matrix

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