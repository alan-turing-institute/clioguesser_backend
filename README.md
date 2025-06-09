# clioguesser_backend
Back end repo for the Clioguesser historical geography game

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
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

## Usage
1. Run the development server:
   ```
   python manage.py runserver
   ```

2. To populate the database with geographical data from a GeoJSON file, use the custom management command:
   ```
   python populate_cliopatria.py <path_to_geojson_file>
   ```
