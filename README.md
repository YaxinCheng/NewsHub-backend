#NewsHub (backend)
  A restful API for downloading news from Chronicle and Metro by a python crawler<br>
  Unfinished yet, more features will be added in the future<br>

###Feature:
  Multi-threaded crawler for better crawling speeds<br>
  Support both Chronicle and MetroNews, and more will be added<br>
  MongoDB used to stored parsed news and user information<br>
  Python Flask and python crawler work seamlessly<br>
  Restful API for easier accesses<br>
  APScheduler ensures regular updates and cleaning old news<br>
  User data encryption with SHA256<br>

###API:
  All parameters and responses will be in JSON format<br>
  <br>
  **News from both sources:**<br>
  Method: GET<br>
  Address: https://hubnews.herokuapp.com/api/news<br>
  Parameters: <br>
  Headers: {'page': <int: number>}<br>
  	Page number (every 15 news in 1 page)<br>
  Response: {'headlines': [], 'normal': []}<br>
  <br>
  **News from specific source:**<br>
  Method: GET<br>
  Address: https://hubnews.herokuapp.com/api/news/<string: source><br>
  	source can be 'metro' or 'chronicle'<br>
  Parameters: <br>
  Headers: {'page': <int: number>}<br>
  	Page number (every 15 news in 1 page)<br>
  Response: <br>
  <br>
  **:**<br>
  Method: <br>
  Address: <br>
  Parameters: <br>
  Headers: <br>
  Response: <br>
  <br>