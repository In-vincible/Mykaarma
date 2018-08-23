# How to run a local copy: 

* Runtime: Python 3.6
* Database: PostgreSQL
* Database Extention: PostGIS(for saving/searching spatial data efficiently) 
## Setting up PostGIS
```
$ createdb  <db name>
$ psql <db name>
> CREATE EXTENSION postgis;
```
## How to Clone:
```
git clone https://github.com/In-vincible/Mykaarma.git
```
### Create virtualenv using venv(new for python 3.6):
```
python3.6 -m venv karm
source karm/bin/activate
```

## or 

### Create virtualenv using virtualenvwrapper
```
mkvirtualenv karm --python=python3.6
workon karm
```

## Installing Dependecies:
(Enter project directory after activating the venv as described above)
```
pip install -r requirements.txt
pip freeze #to check the installed modules
```
## Setting up environment for database:
(Use the same db_name as used while setting up postgis)
```
export DATABASE_URL=postgis://<username>:<password>@localhost/<db_name>
```
## Migrate, insert data(from csv) inside databse, Run:
```
$ python manage.py migrate
$ python manage.py shell
> from endpoints.views import *
> create_modals("<path_of_file_relative_to_project_directory>")
$ python manage.py runserver
```
