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
  Headers: {'page': <int: number>, 'location': <string: location>}<br>
  	Page number (every 15 news in 1 page)<br>
  Response: {'headlines': [.], 'normal': [.]}<br>
  <br>
  **News from specific source:**<br>
  Method: GET<br>
  Address: https://hubnews.herokuapp.com/api/news/<string: source><br>
  	source can be 'metro' or 'chronicle'<br>
  Parameters: <br>
  Headers: {'page': <int: number>, 'location': <string: location>}<br>
  	Page number (every 15 news in 1 page)<br>
  Response: {'headlines': [.], 'normal': [.]}<br>
  <br>
  **Content for specific news:**<br>
  Method: POST<br>
  Address: https://hubnews.herokuapp.com/api/details<br>
  Parameters: {'url': '', 'source': ''}<br>
  Headers: <br>
  Response: {'content': '', 'img': '', 'tag': '', 'title': '', 'source': '', '_id': ''}<br>
  	This response is a News JSON, where '_id' is URL and 'img' is an URL for the image<br>
  <br>
  **Thumbnail for specific news:**<br>
  Method: POST<br>
  Address: https://hubnews.herokuapp.com/api/thumbnails<br>
  Parameters: {'url': ''}<br>
  	The URL should be the image url from the news<br>
  Headers: <br>
  Response: {'_id': '', 'img': ''}<br>
  	The 'img' attribute contains a base64 encoded string which is the binary data of the image<br>
  <br>
  **Register:**<br>
  Method: POST<br>
  Address: https://hubnews.herokuapp.com/register<br>
  Parameters: {'email': '', 'password': '', 'registerTime': '', 'name': ''}<br>
  	Password will be encrypted on server side<br>
  Headers: <br>
  Response: {'ERROR': 'INFO'} or {'SUCCESS': 'INFO'}<br>
  <br>
  **Login:**<br>
  Method: POST<br>
  Address: https://hubnews.herokuapp.com/login<br>
  Parameters: {'email': '', 'password': ''}<br>
  Headers: <br>
  Response: {'ERROR': 'INFO'} or {'_id': '', 'name': '', 'status': BOOL, 'activated': BOOL}<br>
  	The success response is a User JSON
  <br>
  <br>
  **Change password:**<br>
  Method: POST (login required)<br>
  Address: https://hubnews.herokuapp.com/uManage/password<br>
  Parameters: {'email': '', 'password': ''}<br>
  Headers: <br>
  Response: {'ERROR': 'INFO'} or {'SUCCESS': 'INFO'}<br>
  Note: User will be log out once the password is changed<br>
  <br>
  <br>
  **Log out***<br>
  Method: GET (login required)<br>
  Address: https://hubnews.herokuapp.com/logout<br>
  Parameters:<br>
  Headers:<br>
  Response: {'SUCCESS': 'INFO'}
  <br>
  **Get available locations:**<br>
  Method: GET<br>
  Address: https://hubnews.herokuapp.com/api/locations<br>
  Parameters: <br>
  Headers: <br>
  Response: {'location': []}<br>
  <br>

###Packages dependency:
  In the file requirements.txt

There are some more coming<br>
		-- Yaxin Cheng @July 19, 2016
