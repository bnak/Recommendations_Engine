
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
		self.ratings_dictionary = {(197, 766): 3, (197, 585): 3, (58, 437): 4, (209, 614): 5, (175, 87): 5, (30, 462): 5, (191, 304): 3, (45, 307): 3, (30, 183): 4, (52, 94): 2, (30, 477): 3, (191, 305): 5, (175, 6): 5, (30, 933): 4, (191, 437): 3, (197, 546): 2, (30, 440): 4, (175, 561): 4, (222, 684): 3, (213, 527): 3, (30, 79): 3, (241, 695): 4, (28, 383): 3, (44, 268): 5, (191, 688): 5, (30, 744): 4, (30, 42): 4, (191, 930): 4, (30, 478): 4, (191, 195): 5, (1, 915): 5, (77, 437): 3, (180, 59): 2, (191, 769): 3, (30, 785): 5, (44, 684): 3, (30, 815): 3, (30, 437): 2, (191, 169): 4, (108, 333): 5, (30, 660): 4, (191, 462): 2, (175, 981): 5, (138, 442): 5, (148, 477): 2, (108, 242): 4, (197, 756): 4, (30, 906): 3, (175, 298): 4, (175, 97): 3, (58, 268): 5, (30, 614): 3, (197, 462): 2, (155, 442): 2, (58, 134): 5, (175, 439): 1, (187, 536): 3, (175, 131): 2, (30, 201): 5, (30, 296): 4, (175, 266): 5, (191, 785): 5, (111, 188): 2, (28, 527): 5, (148, 134): 5, (197, 384): 4, (30, 116): 4, (18, 424): 4, (84, 79): 3, (108, 188): 3, (241, 305): 5, (8, 307): 3, (95, 87): 1, (189, 561): 5, (79, 333): 5, (108, 481): 4, (167, 330): 4, (111, 578): 3, (158, 462): 2, (241, 169): 4, (143, 769): 4, (77, 134): 4, (169, 158): 3, (56, 911): 4, (167, 363): 5, (227, 250): 5, (78, 201): 4, (17, 911): 4, (191, 188): 3, (191, 684): 5, (191, 6): 2, (180, 684): 4, (197, 10): 4, (76, 609): 4, (30, 265): 5, (167, 97): 4, (28, 265): 3, (111, 735): 3, (225, 79): 2, (143, 596): 2, (175, 199): 4, (28, 906): 3, (171, 664): 3, (197, 33): 4, (30, 199): 5, (191, 7): 4, (175, 7): 5, (167, 788): 4, (241, 769): 5, (197, 682): 4, (213, 192): 4, (210, 834): 4, (241, 298): 5, (175, 664): 4, (225, 592): 2, (143, 265): 4, (197, 178): 3, (126, 769): 3, (143, 906): 4, (96, 684): 5, (197, 825): 3, (30, 266): 4, (191, 596): 4, (83, 695): 3, (111, 481): 5, (191, 735): 4, (157, 6): 3, (30, 481): 5, (156, 756): 3, (30, 527): 4, (148, 536): 5, (83, 7): 5, (191, 750): 5, (181, 962): 3, (191, 527): 4, (175, 906): 4, (111, 192): 3, (175, 742): 4, (197, 719): 5, (241, 684): 5, (118, 134): 5, (175, 164): 5, (197, 481): 4, (30, 998): 4, (191, 383): 3, (191, 266): 4, (44, 296): 3, (108, 437): 2, (197, 735): 4, (197, 42): 4, (178, 25): 3, (28, 592): 4, (111, 416): 5, (175, 478): 1, (189, 735): 3, (30, 439): 4, (191, 561): 5, (8, 734): 1, (241, 664): 4, (197, 911): 3, (156, 769): 2, (143, 199): 4, (197, 352): 5, (30, 307): 4, (191, 291): 3, (191, 766): 5, (167, 87): 4, (30, 781): 2, (175, 305): 1, (191, 134): 5, (175, 440): 4, (30, 981): 2, (58, 602): 4, (175, 195): 5, (30, 834): 3, (148, 609): 4, (30, 471): 3, (223, 383): 4, (191, 59): 5, (30, 944): 3, (199, 330): 3, (30, 624): 4, (187, 735): 5, (148, 79): 1, (71, 478): 4, (197, 477): 5, (138, 596): 5, (33, 930): 5, (189, 188): 4, (30, 602): 5, (241, 383): 3, (111, 87): 2, (191, 602): 5, (197, 6): 3, (108, 788): 4, (97, 592): 5, (17, 491): 3, (191, 592): 3, (223, 742): 5, (187, 906): 1, (187, 305): 4, (148, 614): 2, (8, 7): 5, (111, 265): 3, (197, 301): 4, (197, 769): 2, (28, 7): 4, (223, 785): 5, (199, 695): 4, (30, 6): 3, (83, 296): 4, (223, 748): 3, (175, 695): 2, (156, 906): 3, (175, 596): 5, (191, 979): 3, (187, 981): 1, (28, 201): 4, (175, 735): 5, (175, 10): 3, (28, 134): 5, (173, 6): 4, (197, 998): 3, (189, 684): 2, (191, 834): 3, (191, 87): 4, (215, 609): 5, (118, 188): 3, (30, 663): 4, (58, 684): 4, (30, 301): 4, (175, 785): 5, (199, 756): 4, (171, 330): 4, (199, 981): 4, (241, 6): 3, (199, 769): 4, (143, 195): 4, (18, 933): 4, (104, 735): 4, (30, 168): 4, (30, 188): 3, (197, 527): 4, (197, 602): 3, (30, 592): 4, (8, 742): 4, (199, 508): 4, (152, 829): 5, (175, 302): 5, (83, 97): 4, (191, 42): 3, (191, 481): 5, (30, 283): 4, (30, 492): 4, (175, 602): 4, (152, 384): 4, (30, 536): 5, (8, 695): 1, (199, 684): 5, (118, 684): 5, (175, 766): 4, (36, 561): 1, (175, 998): 2, (143, 298): 3, (143, 481): 3, (197, 788): 3, (201, 857): 4, (197, 840): 4, (187, 815): 3, (143, 424): 4, (197, 183): 4, (191, 352): 5, (148, 283): 1, (111, 199): 4, (83, 744): 4, (4, 967): 1, (191, 199): 4, (5, 685): 3, (175, 769): 5, (30, 788): 4, (187, 481): 3, (191, 261): 2, (55, 134): 5, (191, 79): 4, (44, 979): 5, (30, 840): 3, (197, 750): 3, (97, 527): 3, (28, 815): 4, (191, 477): 4, (143, 134): 5, (248, 87): 5, (199, 188): 4, (175, 933): 3, (223, 981): 5, (175, 684): 5, (58, 481): 5, (191, 201): 5, (241, 330): 4, (30, 756): 3, (197, 199): 3, (199, 664): 4, (30, 424): 4, (30, 59): 2, (185, 7): 4, (30, 7): 5, (156, 527): 4, (241, 131): 3, (148, 201): 1, (197, 437): 3, (199, 906): 5, (191, 247): 4, (223, 766): 4, (175, 304): 5, (17, 462): 2, (110, 424): 3, (191, 10): 4, (223, 609): 4}
		self.movies_and_users_who_rated = {1: [915], 2: [], 3: [], 4: [967], 5: [685], 6: [], 7: [], 8: [695, 7, 307, 734, 742], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [], 15: [], 16: [], 17: [462, 491, 911], 18: [933, 424], 19: [], 20: [], 21: [], 22: [], 23: [], 24: [], 25: [], 26: [], 27: [], 28: [383, 265, 906, 201, 7, 592, 134, 527, 815], 29: [], 30: [478, 834, 744, 840, 199, 602, 59, 788, 440, 42, 116, 471, 781, 944, 296, 79, 265, 477, 906, 201, 462, 301, 624, 756, 7, 592, 307, 660, 437, 266, 168, 481, 283, 527, 981, 998, 183, 439, 614, 933, 6, 785, 536, 492, 424, 815, 663, 188], 31: [], 32: [], 33: [930], 34: [], 35: [], 36: [561], 37: [], 38: [], 39: [], 40: [], 41: [], 42: [], 43: [], 44: [979, 296, 684, 268], 45: [307], 46: [], 47: [], 48: [], 49: [], 50: [], 51: [], 52: [94], 53: [], 54: [], 55: [134], 56: [911], 57: [], 58: [602, 684, 437, 481, 134, 268], 59: [], 60: [], 61: [], 62: [], 63: [], 64: [], 65: [], 66: [], 67: [], 68: [], 69: [], 70: [], 71: [478], 72: [], 73: [], 74: [], 75: [], 76: [609], 77: [437, 134], 78: [201], 79: [333], 80: [], 81: [], 82: [], 83: [744, 695, 97, 296, 7], 84: [79], 85: [], 86: [], 87: [], 88: [], 89: [], 90: [], 91: [], 92: [], 93: [], 94: [], 95: [87], 96: [684], 97: [592, 527], 98: [], 99: [], 100: [], 101: [], 102: [], 103: [], 104: [735], 105: [], 106: [], 107: [], 108: [788, 333, 437, 481, 242, 188], 109: [], 110: [424], 111: [199, 87, 265, 578, 481, 416, 192, 188, 735], 112: [], 113: [], 114: [], 115: [], 116: [], 117: [], 118: [684, 134, 188], 119: [], 120: [], 121: [], 122: [], 123: [], 124: [], 125: [], 126: [769], 127: [], 128: [], 129: [], 130: [], 131: [], 132: [], 133: [], 134: [], 135: [], 136: [], 137: [], 138: [442, 596], 139: [], 140: [], 141: [], 142: [], 143: [769, 195, 199, 298, 265, 906, 596, 481, 134, 424], 144: [], 145: [], 146: [], 147: [], 148: [609, 79, 477, 201, 134, 283, 614, 536], 149: [], 150: [], 151: [], 152: [384, 829], 153: [], 154: [], 155: [442], 156: [769, 906, 756, 527], 157: [6], 158: [462], 159: [], 160: [], 161: [], 162: [], 163: [], 164: [], 165: [], 166: [], 167: [788, 97, 87, 363, 330], 168: [], 169: [158], 170: [], 171: [664, 330], 172: [], 173: [6], 174: [], 175: [769, 478, 195, 199, 602, 664, 302, 440, 298, 695, 164, 87, 97, 766, 131, 906, 684, 7, 266, 596, 981, 998, 439, 305, 10, 561, 742, 933, 6, 785, 304, 735], 176: [], 177: [], 178: [25], 179: [], 180: [59, 684], 181: [962], 182: [], 183: [], 184: [], 185: [7], 186: [], 187: [906, 481, 981, 305, 536, 815, 735], 188: [], 189: [684, 561, 188, 735], 190: [], 191: [261, 769, 979, 834, 195, 199, 602, 59, 383, 42, 169, 87, 352, 247, 750, 766, 79, 477, 201, 462, 684, 7, 592, 437, 266, 596, 481, 134, 527, 305, 10, 561, 6, 785, 291, 930, 304, 188, 688, 735], 192: [], 193: [], 194: [], 195: [], 196: [], 197: [769, 384, 546, 840, 199, 602, 682, 788, 42, 719, 352, 750, 766, 477, 462, 301, 585, 756, 911, 178, 825, 437, 481, 527, 183, 998, 10, 6, 33, 735], 198: [], 199: [769, 664, 695, 906, 756, 684, 981, 508, 188, 330], 200: [], 201: [857], 202: [], 203: [], 204: [], 205: [], 206: [], 207: [], 208: [], 209: [614], 210: [834], 211: [], 212: [], 213: [527, 192], 214: [], 215: [609], 216: [], 217: [], 218: [], 219: [], 220: [], 221: [], 222: [684], 223: [748, 383, 609, 766, 981, 742, 785], 224: [], 225: [79, 592], 226: [], 227: [250], 228: [], 229: [], 230: [], 231: [], 232: [], 233: [], 234: [], 235: [], 236: [], 237: [], 238: [], 239: [], 240: [], 241: [769, 664, 298, 383, 695, 169, 131, 684, 305, 6, 330], 242: [], 243: [], 244: [], 245: [], 246: [], 247: [], 248: [87], 249: [], 250: []}
		#np.load("movies_and_users_who_rated_NLD").item() #needs to be loaded from input file
		self.num_movies = 250 #static int - hardcoded
		self.num_users = 1000 #static int - hardcoded

		self.list_of_movies_that_define_neighborhood = [30, 191, 175, 197, 241, 143, 199, 111, 28, 148, 187, 223, 108, 58, 167, 8, 83, 156, 189, 44] #list of movies with most ratings - hardcoded or read in from file
		self.num_neighborhoods = 20 #static int - hardcoded
		self.max_size_of_neighborhood = 13 #static int- hardcoded#static int- hardcoded. Number of movies in neighborhood


		#parameters hardcoded for matrix factorization
		self.K=2 
		self.iterations=5000
		self.alpha=.0002
		self.beta=.0002



	def mapper_build_neighborhoods(self, _, movies):
		#yields (out_key, out_value) = (neighborhood, movies)

		movies_and_neighborhood = make_neighborhoods_from_movie(
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
		movies_in_neighborhood = remove_duplicates_from_list(movies_in_neighborhood)


		P, Q, movies_and_index_in_neighborhood = matrix_factorization_from_file(movies_in_neighborhood, 
			self.K, self.iterations, self.alpha, self.beta, self.num_users, self.ratings_dictionary)



		predicted_ratings_dictionary = create_dictionary_of_predicted_ratings (P, Q, movies_and_index_in_neighborhood, self.num_users)

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