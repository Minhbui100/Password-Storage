# Password Storage

A personal password manager with interface, a Flask web app backed by PostgresSQL

## Features

- Master password authentication
- Fernet symmetric encryption 
- Add, view, edit, and delete acounts per website
- Duplicate username dection per website

## Setup
### Prerequisites

- Python 3.x
- PostgreSQL (web app only)

### Install dependencies

```bash
pip install flask psycopg2-binary cryptography
```

### Database setup (web app)

Create a PostgreSQL database and table:

```sql
CREATE DATABASE passwords;

\c passwords

CREATE TABLE account (
    id       SERIAL PRIMARY KEY,
    website  TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    url      TEXT,
    UNIQUE (website, username)
);
```

## Usage
### Web app

```bash
python app.py
```

Navigate to `http://127.0.0.1:5000/`. Log in with the master password to manage accounts.

