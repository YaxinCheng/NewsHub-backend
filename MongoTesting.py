from pymongo import MongoClient
from PIL import Image
import requests
from io import BytesIO
import base64
import json

client = MongoClient('mongodb://***REMOVED***.mlab.com:15335/heroku_gfp8zr4k')
mongo = client.heroku_gfp8zr4k
imageURL = 'http://www.metronews.ca/content/dam/thestar/uploads/2016/7/9/wintersleep1.jpg.size.xxlarge.closeup.jpg'
response = requests.get(imageURL)
imageFile = Image.open(BytesIO(response.content))
imageFile.thumbnail((120,120))
imageBuffer = BytesIO()
imageFile.save(imageBuffer, format = "JPEG")
imageString = base64.b64encode(imageBuffer.getvalue())
imageString = imageString.decode('utf-8')
mongo.images.insert_one({'_id': imageURL, 'img': imageString, 'Binary': 1})
result = mongo.images.find({'_id': imageURL})
string = result[0]['img']
print(string == imageString)