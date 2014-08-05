<b>Recommendations Engine</b>
======================

This is an implementation of a neighbor-based matrix decomposition recommendations engine using [Yelp's mrjob package](https://github.com/Yelp/mrjob) to run the program on [Amazon's Elastic MapReduce](http://aws.amazon.com/elasticmapreduce/). 



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











