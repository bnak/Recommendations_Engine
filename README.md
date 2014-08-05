<b>Recommendations Engine</b>
======================

This is an implementation of a neighbor-based matrix decomposition recommendations engine using [Yelp's mrjob package](https://github.com/Yelp/mrjob) to run the program on [Amazon's Elastic MapReduce](http://aws.amazon.com/elasticmapreduce/). 


#<b>Quickstart</b>
Install Python packages Yelp's mrjob package](https://github.com/Yelp/mrjob) and NumPy. 

build_matrix.py will read in a directory, build the initial ratings matrix, and create predicted ratings that can be output to the terminal. 

mr_job_recommendations.py will load:
dictionary of movie ratings - (Key: (movie_id, user_id), Value: rating)
dictionary of movies and users who have rated each movie, used to build neighborhoods - (Key: movie_id, Value: list of users who have rated that movie) 
The map function places movies into neighborhoods and the reduce function produced predicted ratings through matrix decomposition. Yelp's mrjob package has great [documentation](https://pythonhosted.org/mrjob/) and can be configured to Hadoop and Amazon EMR jobs. 

Within the Python files, you can also set the following inputs to affect the accuracy of the algorithm, and the impact of these parameters are discussed in more detail below: 

	    K     : the number of latent features
	    iterations : the maximum number of iterations toward optimization
	    alpha : the learning rate (rate at which vectors in P and Q are incremented toward existing ratings)
	    beta  : the regularization parameter



#<b>File Manifest:</b>

<em>build_matrix.py - </em> functions that read in data files, produce neighborhoods, performs matrix decomposition, and creates predictive ratings matrix. </br>

<em>mr_job_recommendations.py - </em> program that runs the matrix decomposition as a MapReduce job using Yelp's MRjob package</br>

<em>build_test_data.py - </em> program that builds files in the same format as the Netflix data to produce practice datasets</br> 

<em>Sample dataset files - </em> Reduced datasets in the same format as the data provided by Netflix. The first line of every file is the movie_id, and each line thereafter is in the format "user_id,rating,date" 



#<b>The Inspiration:</b></br> 
In 2006, Netflix announced an open competition for the best <em>collaborative filtering algorithm</em> to predict user ratings for films based solely on previous ratings. Netflix provided a dataset of 480,189 users, 17,770 movies, and 100,480,507 ratings. 

#<b>The Challenge: </b></br> 
How does one calculate predicted ratings for each (movie, user) pair from a very sparse seed dataset? 

#<b>The Solution: </b></br> 
Neighbor-based Matrix Decomposition











