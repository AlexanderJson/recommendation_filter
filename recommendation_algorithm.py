import numpy as np

cols = 4
rows = 50
ratings = "ratings"
user_id = 10

def save_preferences(matrix,filename):
    np.savetxt(filename, matrix, fmt='%d', delimiter=',', header='film_id,genre_id,user_id,rating', comments='')
    print("success")

def read_preferences(filename):
    matrix = np.loadtxt(filename, delimiter=',', skiprows=1, dtype=int)
    return matrix

def get_user_matrix():
    all_ratings = read_preferences(ratings)

def filter_user():
    all_ratings = read_preferences(ratings)
    identical_1 = np.tile([0,0,0, user_id], (rows, 1))
    user_found = all_ratings - identical_1
    filtered_user = user_found[user_found[:, 3] == 0]
    print(filtered_user)
    return filtered_user

filter_user()



