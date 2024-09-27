<<<<<<< HEAD
# MovieWatchlist
=======

# Movie Watchlist 

**Users can:**
- Discover, Search for movies
- See movie details
- Log in/register
- Watch movie trailers
- Add movies to their list
- Mark movies as watched
- Rate movies
- Delete movies

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- [Python 3.x](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/download/package-manager) (for frontend React/Vite)
- [MySQL](https://www.mysql.com/downloads/)

### Backend Requirements:
- Flask
- MySQL
- GraphQL



## Screenshots

![App Screenshot](https://www.etsy.com/market/movie_watchlist)


## Technologies Used

**Frontend:**
- React+vite
- CSS

**Backend:**
- Mysql
- Flask
- GraphQL


## API used

 - For movies: [TMDB](https://developer.themoviedb.org/docs/getting-started)
 - For IMDb scores: [IMBbOt](https://github.com/TelegramPlayGround/Free-Movie-Series-DB-API)


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
  cd backend
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

## Run the Backend Server
```bash
  python app.py

```

The Backend will be running at http://localhost:5000

## You can test your GraphQL queries and mutations by navigating to:
```bash
http://localhost:5000/graphql

```
# Set Up the Frontend(React+Vite)

- a) Install Node.js dependencies
Navigate to the frontend/ directory and install the required packages: 

```bash
cd frontend
npm install
```
- b) Run the Frontend Development Server
Start the Vite development server:
```bash
npm run dev
```
The frontend will be running at http://localhost:3000 (or another port specified by Vite).

# Summary of Local URLs
- Backend (GraphQL endpoint):

    http://localhost:5000/graphql - GraphiQL interface for testing GraphQL queries and mutations.

- Frontend (React + Vite):

    http://localhost:3000 - React front-end served by Vite.
>>>>>>> 81b3d86 (added readme file)
