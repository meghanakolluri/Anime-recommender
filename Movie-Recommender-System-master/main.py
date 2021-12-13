import numpy as np
import pandas as pd
from flask import Flask, render_template, request
# libraries for making count matrix and similarity matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MaxAbsScaler

# define a function that creates similarity matrix
# if it doesn't exist
def create_sim():
    data = pd.read_csv('anime.csv')
    anime_features=pd.read_csv("anime_features.csv")
    max_abs_scaler = MaxAbsScaler()
    anime_features = max_abs_scaler.fit_transform(anime_features)
    return data,anime_features



# defining a function that recommends 10 most similar movies
def rcmd(query=None):
    data,anime_features=create_sim()
    if query not in data['name'].unique():
        return('This anime is not in our database.\nPlease check if you spelled it correct.')
    else:
        nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(anime_features)
        distances, indices = nbrs.kneighbors(anime_features)
        l=[]
        if query:
            found_id = data[data["name"]==query].index.tolist()[0]
            for id in indices[found_id][1:]:
                l.append(str(data["name"].iloc[id]))
        return l

        

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/recommend")
def recommend():
    movie = request.args.get('movie')
    r = rcmd(movie)
    print(r)
    movie = movie.upper()
    if type(r)==type('string'):
        return render_template('recommend.html',movie=movie,r=r,t='s')
    else:
        return render_template('recommend.html',movie=movie,r=r,t='l')



if __name__ == '__main__':
    app.run()
