import numpy as np

cols = 4
rows = 70
ratings_file = "ratings"
user_id = 10

def save_preferences(matrix,filename):
    np.savetxt(filename, matrix, fmt='%d', delimiter=',', header='film_id,genre_id,user_id,rating', comments='')
    print("success")

def read_preferences(filename):
    matrix = np.loadtxt(filename, delimiter=',', skiprows=1, dtype=float)
    return matrix

def get_user_matrix():
    all_ratings = read_preferences(ratings_file)
    return all_ratings


## filters out the user by id and finds all user interactions
## make this more abstract for different filter scenarios
def filter_user(all_ratings):
    identical_1 = np.tile([0,0,0, user_id], (rows, 1))
    user_found = all_ratings - identical_1
    filtered_user = user_found[user_found[:, 3] == 0]
    print(" FILTERED USER: ", filtered_user, "----------------------------------")
    return filtered_user

##interface later
def filter_user_ratings(user):
    filter_ratings = user[:, 2]
    print("FILTERED RATINGS: ", filter_ratings, "----------------------------------")
    return filter_ratings

def calculate_recommendations(user,user_ratings):
    mean = np.mean(user_ratings)
    distance = user_ratings - mean
    print(distance, "----------------------------------")
    return distance

def filter_user_genres(user):
    genre_found = user[:, 1]
    print(" FILTERED GENRES: ", genre_found, "----------------------------------")
    return genre_found

def filter(index,matrix):
    filter_ratings = matrix[:, index]
    print("--------------", filter_ratings, "----------------------------------")
    return filter_ratings

def recommend_movie():
    all_actions = get_user_matrix()
    user_actions = filter_user(all_actions)
    user_ratings = filter(2,user_actions)
    print("Rating: ")
    rating_gradient = calculate_recommendations(user_actions,user_ratings)
    print("Grading: ")
    user_genres = filter(1,user_actions)
    rating_genres = np.column_stack((user_genres,rating_gradient))
    recommendation_matrix = np.maximum(0, rating_genres)
    print("Rated: ", recommendation_matrix)

recommend_movie()


## TODO: add more complex recommendations later on with movie ID etc. Need to make another matrix for movies
# or just add more parameters like actor, director, etc, then fetch movies from these based on amount of parameters.
# highest recommendaiton = most parameters there, thats not already fully in matrix?


## make: good % to make a border for user rating and genres. If user only rated 1 movie genre
## in matix with 1000 rows, that genre is irrelevant. Gradiant solves?

