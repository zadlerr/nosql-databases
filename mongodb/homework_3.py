# require the driver package
import pymongo
from pprint import pprint
# Create a client
# client = ...
client = pymongo.MongoClient()
db = client['mydb']

collection = db.movies
# A. Update all movies with "NOT RATED" at the "rated" key to be "Pending rating". The operation must be in-place and atomic.
res = collection.update_many({'rated':'NOT RATED'}, {'$set' : {'rated': 'Pending rating'}})

# B. Find a movie with your genre in imdb and insert it into your database with the fields listed in the hw description.
#print(collection.find({"genres" : "Documentary"}).count())
collection.insert_one({'title': 'Les bosquets', 'year': 2015, 'countries' : ['France'], 'genres':['Documentary','Short'], 'directors':['JR'], 'imdb': {"_id": 7223, 'rating': 7.6, 'votes' : 5}}) 
# C. Use the aggregation framework to find the total number of movies in your genre.
cursor = collection.aggregate([{'$match' : {'genres': 'Documentary'}}])
ret = list(cursor)
print(len(ret))

# D. Use the aggregation framework to find the number of movies made in the country you were born in with a rating of "Pending rating".
cursor = collection.aggregate([{'$match':{"countries": "USA"}},{'$match':{"rated":"Pending rating"}}])
ret = list(cursor)
print(len(ret))
# Example result when country is Hungary:
#  => [{"_id"=>{"country"=>"Hungary", "rating"=>"Pending rating"}, "count"=>9}]

 
# E. Create an example using the $lookup pipeline operator. See hw description for more info.
cursor = collection.aggregate([{'$lookup':{'from':'mynewCol','localField':'year','foreignField':'year released','as': 'time'}}])
ret = list(cursor)
print("lookup operator return=", len(ret))
