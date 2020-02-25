
from flask import (Flask, render_template, redirect, request, flash,
                   session)
from model import User, Rating, Movie
import correlation

# this gives an error
m = Movie.query.filter_by(title="Toy Story").one()
u = User.query.get(1)
ratings = u.ratings
other_ratings = Rating.query.filter_by(movie_id=m.movie_id).all()
other_users = [r.user for r in other_ratings]
score_pairs = [(5, 5), (3, 3), (2, 3)]
print(correlation.pearson(score_pairs))

dictionary = {}
score_pairs = []
# o == other users
o = other_users[0]
for rating in ratings:
    dictionary[rating.movie_id] = rating.score

for o_rating in o.ratings:
    if o_rating.movie_id in dictionary:
        score_pairs.append((dictionary.get(o_rating.movie_id),
                            o_rating.score))
