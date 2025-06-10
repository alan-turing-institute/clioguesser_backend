# clioguesser_backend
Back end repo for the Clioguesser historical geography game

## Installation
1. Clone the repository:
   ```
   git clone --recurse-submodules <repository-url>
   cd clioguesser_backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Install GDAL and GEOS for your operating system:
   - **Ubuntu**: 
     ```
     sudo apt-get install gdal-bin libgdal-dev
     ```
   - **macOS**: 
     ```
     brew install gdal
     ```
   - **Windows**: Follow the instructions on the [GDAL website](https://gdal.org/download.html).

5. Unzip the GeoJSON from the Cliopatria into the `clioguesser_backend/data` directory
   ```
   unzip cliopatria/cliopatria.geojson.zip -d clioguesser_backend/data
   ```

## Usage
1. Run the development server:
   ```
   python manage.py runserver
   ```

2. To populate the database with geographical data from a GeoJSON file, use the custom management command:
   ```
   cd clioguesser_backend
   python manage.py populate_cliopatria data/cliopatria_polities_only.geojson
   ```
   - Note: check the data file has this name, or adjust the command accordingly.

## API calls

### Get the polity data for a given year:
```
GET /api/polities/?year=2000
```

Test with curl:
```
curl -X GET "http://localhost:8000/api/polities/?year=2000"
```

### Get the current leaderboard:
```
GET /api/leaderboard/
```

Test with curl:
```
curl -X GET "http://localhost:8000/api/leaderboard/"
```
### Update the leaderboard

Update the leaderboard with a new score:
```
POST /api/leaderboard/update/
Content-Type: application/x-www-form-urlencoded

initials=ABC&score=1234
```

Test with curl:
```
curl -X POST -d "initials=EJC&score=1234" http://127.0.0.1:8000/api/leaderboard/update/
```

### Calculate a score

Calculate a score based on year range, true year, and guess:
```
GET /api/score/?min_year=1000&max_year=2000&true_year=1500&guess_year=1400
```

Test with curl:
```
curl -X GET "http://localhost:8000/api/score/?min_year=1000&max_year=2000&true_year=1500&guess_year=1400"
```

## Django notes

If you add a new model, you need to create a migration file:
```
   cd clioguesser_backend 
   python manage.py makemigrations
```

Then apply the migration:
```
   python manage.py migrate
```

## Docker

You can run the docker container containing the backend by running:
```
   docker compose up -d
```
