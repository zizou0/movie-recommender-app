import gzip
import shutil
import pickle
import os

# Define the file paths to compress
files_to_compress = [
    'data/movies.dat',
    'data/ratings.dat',
    'data/users.dat'
]

def compress_file(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as f_in:
        with gzip.open(output_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# Example: Compressing your .dat files
compress_file('data/ratings.dat', 'data/ratings.dat.gz')
compress_file('data/movies.dat', 'data/movies.dat.gz')
compress_file('data/users.dat', 'data/users.dat.gz')
