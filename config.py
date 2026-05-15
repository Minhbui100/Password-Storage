import os

db_host=os.getenv("db_host", "localhost")
db_port=os.getenv("db_port", "5432")
db_name=os.getenv("db_name", "passwords")
db_user=os.getenv("db_user", "postgres")
db_password=os.getenv("db_password", "postgres")

master_password=os.getenv("master_password", "admin")
secret_key=os.getenv("secret_key", "secret")
salt=os.getenv("SALT", "passwordstorage-salt-2024").encode()
