# clioguesser_backend

## Overview
This project is a Django application designed to manage and analyze geographical data using GeoJSON files. It provides functionalities to populate a database with geographical shapes and their associated metadata.

## Project Structure
```
clioguesser_backend/
├── clioguesser_backend/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── populate_draft.py
└── README.md
```

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
   python populate_draft.py <path_to_geojson_file>
   ```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.