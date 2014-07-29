
from mrjob.job import MRJob
import build_matrix
import csv
import numpy as np
import os
import datetime
import linecache
import sys
from pprint import pprint

class MR_build_matrix(MRJob):

	def __init__(self):
		self.ratings_dictionary = {}
		self.movies_and_users_who_rated = {}
		self.num_movies = 20
		self.num_users = 30

		self.list_of_movies_that_define_neighborhood = []
		self.num_neighborhoods = 5
		self.neighborhoods = [[] for x in xrange(self.num_neighborhoods)] #list of neighborhoods
		self.movies_and_neighborhood = {}
		self.max_size_of_neighborhood = 10

		self.K=2 
		self.iterations=5000
		self.alpha=.0002
		self.beta=.0002


	def mapper_build_neighborhoods(self, _, movies):
		#yields (out_key, out_value) = (neighborhood, movies)

		movies_and_neighborhood = make_neighborhoods_from_movie(self.movies_and_users_who_rated, 
				self.list_of_movies_that_define_neighborhood, self.num_neighborhoods, self.max_size_of_neighborhood)

		for item in movies_and_neighborhood.items():
			yield item

	def reducer_create_matrix(self, _, neighborhood): 

		P, Q, movies_and_index_in_neighborhood = matrix_factorization_from_file(neighborhood, self.K, self.iterations, 
			self.alpha, self.beta, self.num_users, self.ratings_dictionary)

		predicted_ratings_dictionary = create_dictionary_of_predicted_ratings (P, Q, movies_and_index_in_neighborhood, self.num_users)

		for item in predicted_ratings_dictionary.items():
			yield item

	def steps(self):

		return [
            MRStep(mapper=self.mapper_build_neighborhoods,
                   reducer=self.reducer_create_matrix)
        ]




def main():

	a = MR_build_matrix()

	print a.iterations

	print "ran"

	#MR_build_matrix.run() #where MR_build_matrix is the job class






if __name__ == '__main__':
	main()