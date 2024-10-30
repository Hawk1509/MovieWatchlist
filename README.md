
# Movie Watchlist 

**Users can:**
- Discover, Search for movies
- See movie details
- Log in/register
- Watch movie trailers

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- [Python 3.x](https://www.python.org/downloads/)
- [SQLite](https://www.sqlite.org/download.html)

### Backend Requirements:
- Flask
- SQLite
- GraphQL



## Screenshots

![App Screenshot](https://www.etsy.com/market/movie_watchlist)


## Technologies Used

**Frontend:**
-Flask

**Backend:**
- SQLite
- Flask
- GraphQL


## Run Locally

## Clone the project

```bash
  git clone https://github.com/Hawk1509/MovieWatchlist.git
```

## Go to the project directory

```bash
  cd MovieWatchlist
```
## Set Up the Backend

Navigate to backend/ directory and create a virtual environment

```bash
  cd movie
  python -m venv venv
```
## Activate the virtual environment

- **On Windows:**
```bash
venv\Scripts\activate
```
- **On macOs/Linux:**
```bash
source venv/bin/activate
```

## Install Backend dependencies

```bash
 pip install -r requirements.txt

```

##Populate the database
```bash
    python populate_db.py
```

## Run the Backend Server
```bash
  python app.py

```

The Backend will be running at http://localhost:5000

## You can test your GraphQL queries and mutations by navigating to:
```bash
http://localhost:5000/graphql

```