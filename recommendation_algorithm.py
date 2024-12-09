from flask import Flask, jsonify, request
import numpy as np


app = Flask(__name__)

cols = 4
rows = 70
ratings_file = "ratings"

def read_preferences(filename):
    matrix = np.loadtxt(filename, delimiter=',', skiprows=1, dtype=float)
    return matrix

def get_user_matrix():
    all_ratings = read_preferences(ratings_file)
    return all_ratings


## filters out the user by id and finds all user interactions
## make this more abstract for different filter scenarios
def filter_user(all_ratings, user_id):
    rows = all_ratings.shape[0]
    identical_1 = np.tile([0,0,0, user_id], (rows, 1))
    user_found = all_ratings - identical_1
    filtered_user = user_found[user_found[:, 3] == 0]
    return filtered_user

##interface later
def filter_user_ratings(user):
    filter_ratings = user[:, 2]
    return filter_ratings

def calculate_recommendations(user,user_ratings):
    mean = np.mean(user_ratings)
    distance = user_ratings - mean
    return distance

def filter_user_genres(user):
    genre_found = user[:, 1]
    return genre_found

def filter(index,matrix):
    filter_ratings = matrix[:, index]
    return filter_ratings

def recommend_movie(user_id):
    all_actions = get_user_matrix()
    user_actions = filter_user(all_actions, user_id)
    user_ratings = filter(2,user_actions)
    print("Rating: ")
    rating_gradient = calculate_recommendations(user_actions,user_ratings)
    print("Grading: ")
    user_genres = filter(1,user_actions)
    rating_genres = np.column_stack((user_genres,rating_gradient))
    recommendation_matrix = np.maximum(0, rating_genres)
    print("Rated: ", recommendation_matrix)


    ## aggregated socring (to get the percentages for fun): 

    ## remove duplicates in col 1 (genres)
    unique_genres = np.unique(recommendation_matrix[:,0])
    genre_sums = {genre: np.sum(recommendation_matrix[recommendation_matrix[:, 0] == genre, 1]) for genre in unique_genres}

    ##TODO : fix more here:
    total_score = np.sum(list(genre_sums.values()))
    genre_percentages = {genre: f"{(score / total_score) * 100:.2f}%" if total_score > 0 else 0 for genre, score in genre_sums.items()}
    return genre_percentages


## TODO: add more complex recommendations later on with movie ID etc. Need to make another matrix for movies
# or just add more parameters like actor, director, etc, then fetch movies from these based on amount of parameters.
# highest recommendaiton = most parameters there, thats not already fully in matrix?


## make: good % to make a border for user rating and genres. If user only rated 1 movie genre
## in matix with 1000 rows, that genre is irrelevant. Gradiant solves?



## REST API SECTION

@app.route('/recommend', methods=['GET'])
def get_recommended():
    return jsonify({"message: ": "General recommendations WIP"})


@app.route('/recommend/genre', methods=['POST'])
def get_recommended_movies():
    data = request.json
    print(f"Received data: {data}")

    user_id = data.get("userid")

    if user_id is None:
        return jsonify({"error": "Missing userID"}), 400

    try:
        recommendations = recommend_movie(user_id)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_rating', methods=['POST'])
def add_rating():
    data = request.json
    print(f"Received data: {data}")

    film_id = data.get("filmID")
    genre_id = data.get("genreID")
    user_id = data.get("userID")
    rating = data.get("rating", 5.0) ## TODO fix rating

    if genre_id is None or user_id is None:
        return jsonify({"error": "Missing genreID or userID"}), 400
    
    try: 
        with open(ratings_file, "a") as file:
            file.write(f"{film_id},{genre_id},{rating},{user_id}\n")
        return jsonify({"message": "Movie rated"}), 201
    except Exception as e: 
        return jsonify({"error": str(e)}),500

if __name__ == '__main__':
    app.run(debug=True)
