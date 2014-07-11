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

def build_matrix(rows, columns, space_filler):
	#rows are items, columns are users
	#ratings[item_id-1][user_id-1]
	matrix = [space_filler]*rows
	for i in xrange(rows):
		matrix[i] = [space_filler]*columns

	matrix = np.array(matrix)
	return matrix

def read_movie_rating(my_file):
	f = open(my_file)
	lines = f.readlines()
	f.close()
	return lines


def fill_matrix(lines, ratings):

	#get movie_id from filetext of lines; corresponds to first index
	#of ratings matrix
	line1 = lines[0].split(":", 1)
	movie_id=int(line1[0])

	lines.pop(0)  #remove first line with movie_id


	for i in xrange(len(lines)):

		individual_rating = lines[i].split(",")
		#individual_rating = [user_id, rating, date]

		user_id = int(individual_rating[0])
		rating = int(individual_rating[1])


		ratings[movie_id-1][user_id-1]=rating

	return ratings

def build_ratings_matrix_from_file(directory_name, num_users, space_filler):

	files = os.listdir(directory_name)
	files.pop(0)  #first entry is .ds_store

	#users have to be hardcoded in

	ratings = build_matrix(len(files), num_users, space_filler)

	for filename in files:
		lines = read_movie_rating(directory_name + "/" + filename)
		fill_matrix(lines, ratings)

	return ratings


def fill_matrix_with_average_ratings(ratings):
	for i in xrange(len(ratings)):
		average_rating = np.mean(ratings[i])
		for j in xrange(len(ratings[i])):
			if ratings[i][j] == 0:
				ratings[i][j] = average_rating

	return ratings

def retrieve_folder_data(directory_name, movie_id, line_num):
	files = os.listdir(directory_name)
	files.pop(0)  #first entry is ds.store

	filepath = directory_name + "/" + files[movie_id-1]

	individual_rating = linecache.getline(filepath, line_num).split(",")

	user_id = int(individual_rating[0])

	rating = int(individual_rating[1])

	return user_id, rating

def file_len(my_file):
	with open(my_file) as f:
		for i, l in enumerate(f):
			pass
	return i+1


def matrix_factorization_from_file(directory_name, K, iterations, alpha, beta, num_users):
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
	A = []

	files = os.listdir(directory_name)
	files.pop(0)  #removes first entry of ds.store

	num_movies = len(files)

	P = np.random.rand(num_movies, K)
	Q = np.random.rand(num_users, K)

	Q = Q.T #transpose Q

	for step in xrange(iterations):
		for i in xrange(num_movies): 

			user_list = [0] * num_users

			A.append(user_list)

			filepath = directory_name + "/" + files[i]


			for j in xrange(2,file_len(filepath)):
				individual_rating = linecache.getline(filepath, j).split(",")

				#user_id = int(individual_rating[0])
			

				rating = int(individual_rating[1])

				j = j-1

				A[i][j] = rating


				if A[i][j] > 0:
					eij = A[i][j] - np.dot(P[i,:], Q[:,j])
					for k in xrange(K):
						P[i][k] = P[i][k] + alpha * (2 * eij *Q[k][j] - beta * P[i][k])
						# P.set(i, k, (P.get(i, k) + alpha * (2 * eij *Q[k][j] - beta * P[i][k])
						
						Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])

		error_prime = 0 

		for i in xrange(len(A)):
			for j in xrange(len(A[i])):
				if A[i][j]>0:
					error_prime = error_prime + pow(A[i][j] - np.dot(P[i,:], Q[:,j]),2)
					for k in xrange(K):
						error_prime = error_prime + (beta/2) * (pow(P[i][k],2)+pow(Q[k][j],2))
			if error_prime < 0.001:
				break


	print "Size of A: %s" % sys.getsizeof(A)

	return P, Q.T




def main(): 

	start_time=datetime.datetime.now()

	ratings = build_ratings_matrix_from_file("netflix_local_data", 30, 0)

	print ratings


	print "Size of Ratings: %s" % sys.getsizeof(ratings)

	P, Q = matrix_factorization_from_file("netflix_local_data", K = 2, iterations=5000, alpha=0.0002, beta=0.02, num_users = 30)

	print "************************************************"
	print "Estimated_ratings:"

	predicted_ratings = np.dot(P, Q.T)


	average_error = np.mean(predicted_ratings-fill_matrix_with_average_ratings(ratings))

	print "Size of prediected ratings: %s"  % sys.getsizeof(predicted_ratings)

	print "Average Error: %s" % average_error

	end_time = datetime.datetime.now()

	time_elapsed = end_time-start_time

	print "Total Time Elapsed: %s" % time_elapsed

	



if __name__ == '__main__':
	main()