# Hangman
Hangman Programming Exercise 

To use this repo, use a linux like terminal environment with python
installed, python3.11 assumed but substitute with your own. Clone the repo and
cd into the folder (where this readme is) and create a new virtual environment.

```console
python3.11 -m venv __project/venv
```

Activate it.

```console
$ source __project/venv/bin/activate
```

Update pip

```console
$  pip install -r __project/packages/python/_pip.txt
```

Install packages

```console
$ pip install -r __project/packages/python/live.txt
```

If you want the test environment, change 'live.txt' to 'test.txt' for the
full development environment use ' work.txt'

Execute program
```console
$ python -m application
```

## Development
Note that these commands are usually put in a Makefile, however for simplicity
this hasn't been done in this case.

### Code formatting and correctness
```console
mypy application
black application
isort application
coverage run --source application,tests -m unittest discover
coverage report -m
```