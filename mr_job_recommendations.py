
from mrjob.job import mrjob
import * from build_matrix.py

class MR_build_matrix(MRJob):

	def mapper(self, _, movies):
		#yields (out_key, out_value) = (neighborhood, movie)




if __name__ == '__main__'
	MR_build_matrix.run() #where MR_build_matrix is the job class