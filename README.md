#### SI 507 Python Programming Project 1 Assignment
This is a README.md for file SI507_Project3.py. This is a homework assignment for SI 507/ Professor Jackie Cohen at the University of Michigan.

##### What are the files included?
The files included are project1-env, requirements.txt, SI507_Project3.py. There is also a templates folder which includes html files (all_directors.html, all_movies.html and index.html).

##### What is the final result and functionality?
In SI507_Project3.py, the code is essentially accomplishing two tasks. It is building a database with the input from the user and also rendering that input on a web interface.

Each route in the code will produce something different on the web interface. Please see below for each route and how they differ.

Route 1: If user inputs "/" at the end of the URL, the screen will read the amount of movies that have been saved in the database.

Route 2: If user inputs '/movie/new/<title>/<director>/<genre>/' an  original  movie title, director and genre that is not yet in the database, the screen will read "New movie: {insert name of movie} by {insert name of director}". If the movie already exists, the user will be prompted so. If not, this new entry will be placed into the movie database.

Route 3: If the user inputs '/all_movies' at the end of the URL, the screen will read all the movies that have been inputted by the user. It is important to note that in this route, the all_movies.html template (from the templates folder) are being used to render the words on the screen. The template is utilizing information from a list that was created in the SI507_Project3 code.

As users are inputting information into the route, the database named sample_movies.db is being populated with this information.

##### How do you run this project?
Download Project3 on your local computer.
requirements.txt will indicate all the dependencies required for this project. Open the terminal and download all the dependencies by typing pip install -r requirements.txt.
