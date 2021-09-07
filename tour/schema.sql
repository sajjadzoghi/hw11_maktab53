-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS tours;


CREATE TABLE tours (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  image BLOB NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  start_date TIMESTAMP NOT NULL,
  end_date TIMESTAMP NOT NULL,
  price TEXT NOT NULL,
  distance TEXT NOT NULL,
  travel_by TEXT NOT NULL
);
