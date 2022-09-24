# inflation case

in first copy .env.example to .env

```shell
    cp .env.example.env
```

in next you need to install virtualenviroment in current directory

```shell
    python3 -m venv env 
    pip install poetry
    poetry install
```

if you need to create a database:

```shell
        python create_db.py
```