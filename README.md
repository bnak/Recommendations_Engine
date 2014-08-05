<b>Recommendations Engine</b>
======================

This is an implementation of a neighbor-based matrix decomposition recommendations engine using [Yelp's mrjob package](https://github.com/Yelp/mrjob) to run the program on [Amazon's Elastic MapReduce](http://aws.amazon.com/elasticmapreduce/). 


#<b>Quickstart</b>
Install Python packages [Yelp's mrjob package](https://github.com/Yelp/mrjob) and [NumPy](http://www.numpy.org/). 

<b>build_matrix.py</b> will read in a directory, build the initial ratings matrix, and create predicted ratings that can be output to the terminal. 

<b>mr_job_recommendations.py</b> will load:
dictionary of movie ratings - (Key: (movie_id, user_id), Value: rating)

dictionary of movies and users who have rated each movie, used to build neighborhoods - (Key: movie_id, Value: list of users who have rated that movie) 

The map function places movies into neighborhoods and the reduce function produced predicted ratings through matrix decomposition. Yelp's mrjob package has great [documentation](https://pythonhosted.org/mrjob/) and can be configured to Hadoop and Amazon EMR jobs. 

Within the Python files, you can also set the following inputs to affect the accuracy of the algorithm, and the impact of these parameters are discussed in more detail below: 

	    K     : the number of latent features
	    iterations : the maximum number of iterations toward optimization
	    alpha : the learning rate (rate at which vectors in P and Q are incremented toward existing ratings)
	    beta  : the regularization parameter (prevents overfitting) 



#<b>File Manifest</b>

<b>build_matrix.py - </b> functions that read in data files, produce neighborhoods, performs matrix decomposition, and creates predictive ratings matrix. </br>

<b>mr_job_recommendations.py - </b> program that runs the matrix decomposition as a MapReduce job using Yelp's MRjob package</br>

<b>build_test_data.py - </b> program that builds files in the same format as the Netflix data to produce practice datasets</br> 

<b>Sample dataset files - </b> Reduced datasets in the same format as the data provided by Netflix. The first line of every file is the movie_id, and each line thereafter is in the format "user_id,rating,date" 



#<b>The Inspiration</b></br> 
In 2006, Netflix announced an open competition for the best <em>collaborative filtering algorithm</em> to predict user ratings for films based solely on previous ratings. Netflix provided a dataset of 480,189 users, 17,770 movies, and 100,480,507 ratings. 

#<b>The Challenge </b></br> 
How does one calculate predicted ratings for each (movie, user) pair from a very sparse seed dataset? 

#<b>The Solution </b></br> 
Neighbor-based Matrix Decomposition

![alt text](https://raw.githubusercontent.com/bnak/Recommendations_Engine/mrjob/static/matrix1.jpg)




![alt text](https://raw.githubusercontent.com/bnak/Recommendations_Engine/mrjob/static/matrix4.jpg)




![alt text](https://raw.githubusercontent.com/bnak/Recommendations_Engine/mrjob/static/MapReduce.jpg)



#<b>References and Sources </b></br> 

*[Matrix Factorization Techniques for Recommender Systems](https://datajobs.com/data-science-repo/Recommender-Systems-%5BNetflix%5D.pdf)

*[PyCon 2011: mrjob: Distributed Computing for Everyone](http://blip.tv/pycon-us-videos-2009-2010-2011/pycon-2011-mrjob-distributed-computing-for-everyone-4898987/)

*[Matrix Factorization: A Simple Tutorial and Implementation in Python](http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/)

*[Using Linear Algebra for Intelligent Information Retrieval](http://lsirwww.epfl.ch/courses/dis/2003ws/papers/ut-cs-94-270.pdf)

*[Large-scale Parallel Collaborative Filtering for the Netflix Prize] (http://www.hpl.hp.com/personal/Robert_Schreiber/papers/2008%20AAIM%20Netflix/netflix_aaim08(submitted).pdf)

*[Incremental Singular Value Decomposition Algorithms for Highly Scaleable Recommender Systems](http://files.grouplens.org/papers/sarwar_SVD.pdf)













