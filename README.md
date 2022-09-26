# Basic ecommerce CRUD Flask app to demonstrate SOLID principles
- practicals examples of solid principles in python flask
# Requirements
- Python 3.x
- Required modules should be installed from equirements.txt file
# Installation and setup
- make a virtual environment in your machine using `python3 -m venv .venv` and activate it using `source .venv/bin/activate` in the same directory
- Clone repository using `git clone https://github.com/kat1zzz/flask-solid-app.git` in your command terminal.
- Enter `pip install -r requirements.txt` to install required packages.
- change Config file to add you db url - `PSQL_URL`
- Open the terminal and run `python main.py` command
- hit the Postman for API repsonses

- to create db open any sql terminal or GUI to create tables
`
CREATE TABLE user2
(
  id SERIAL PRIMARY KEY,
  email text,
  name text,
  username text,
  password text
);

CREATE TABLE items
(
  id SERIAL PRIMARY KEY,
  price integer,
  name text
);

CREATE TABLE orders
(
  id SERIAL PRIMARY KEY,
  user_id integer REFERENCES user2(id),
  payment_id integer REFERENCES payment(id)
);

CREATE TABLE payment
(
  id SERIAL PRIMARY KEY,
  type text,
  status text
);

CREATE TABLE cart
(
  id SERIAL PRIMARY KEY,
  user_id integer REFERENCES user2(id),
  item_id integer REFERENCES items(id)
);
`
