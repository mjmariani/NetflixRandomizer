## NetflixRandomizer

Link to Project Proposal:

[Project Proposal](https://docs.google.com/document/d/1wHd4jy7HrYBw1zu-e6qUlC6R9Tqd2w4a/edit)

**Links to API:**

[The Movie DB API](https://www.themoviedb.org/documentation/api)<br>

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary dependencies for this website.

    pip install -r requirements.txt
	flask run

## Tech Stack

### Server/Backend:

**Language**: Python

**Package management**:<br/> PIP<br/><br/>
Frameworks:<br/>
Flask<br/>
Flask-SQLAlchemy

### Web/Frontend:

HTML<br/>
CSS<br/>
JavaScript<br/>
Bootstrap 4<br/>
jQuery<br />

### Database:

Postgres

### Testing:
Unittest

## Usage

The preliminary goal of my website will be to create a project which shows off all of the skills and technologies I have been learning thus far. Hopefully, I can create a foundation to which I can use to grow a more complex website should I decide to pursue this idea further. However, the main and ultimate goal, in terms of its audience, will be to create a place where one can go and be suggested movies, tv shows or other entertainment in a fun manner while being able to enjoy the suggested movies with others.<br/><br/>
In terms of data, I will be primarily using movie and tv show information through the TMDB API. I’m choosing this API as I have just found out that Netflix ended their support for a public API.<br/><br/>

**Steps on how to use:**<br/>
1. Click Sign Up and create an account.<br/>
2. Then click Randomizer, once logged in and go ahead and start liking or disliking movie suggestions.<br/>
3. Any movie/tv show that you like, will be added to your queue to watch at any time.<br/>
4. Once watched, you can mark it as watched and continue using the Randomizer to get another movie/tv show selection.<br/>

*For later implementation:*<br/>
5. Also, go ahead and add people to your friends list by searching for their username. Wait for them to accept friend request.
6. Once you're friends with someone, you can view their queue of movies.

##Testing

To run the tests, we will use unittest and run from the CLI:

    python -m unittest discover

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.