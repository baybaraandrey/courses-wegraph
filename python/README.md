# Linux Installation
Install Courses Into Virtualenv
```sh
python3 -m venv env                                       # Create virtualenv.
source env/bin/activate                                   # Acivate virtual environments.
python3 -m pip install -U pip setuptools wheel            # Upgrade pip.
python3 -m pip install -e ."[dev,testing,linting,deploy]" # Install courses in development mode.
python3 -m pip install docker-compose                     # Install docker-compose
```

# Docker Compose
```sh
./dev/build_local.bash                         # Build an image for local development.
./dev/build_production.bash                    # Build an image with provided type of a tag and push to the registry.
./dev/migrate.bash                             # Updates database schema.
./dev/createsuperuser.bash                     # Create superuser.
./dev/tests.bash                               # Run tests
./dev/linter.bash                              # Run static code analysis.
./dev/serve.bash                               # Start development server.
```
Goto: http://localhost:8000/swagger/

# Windows Installation
Install Courses Into Virtualenv
```sh
copy env.example to .env

python -m venv env                                        # Create virtualenv.
\env\Scripts\activate.bat                                 # Acivate virtual environments.
python -m pip install -U pip setuptools wheel             # Upgrade pip.
python -m pip install -e ."[dev,testing,linting,deploy]"  # Install courses in development mode.
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
