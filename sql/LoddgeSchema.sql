CREATE TABLE IF NOT EXISTS user_base(
	user_id VARCHAR(64) PRIMARY KEY, 
	user_password VARCHAR(64) NOT NULL, 

	first_name VARCHAR(64) NOT NULL, 
	last_name VARCHAR(64) NOT NULL, 
	phone_number NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS listings(
	listing_id INT PRIMARY KEY, 
	listing_name VARCHAR(128) NOT NULL,
	neighbourhood VARCHAR(64) NOT NULL,
	neighbourhood_group VARCHAR(64) NOT NULL,
	address VARCHAR(128) NOT NULL,
/*	latitude NUMERIC NOT NULL CHECK(latitude >= -90 AND latitude <= 90),
	longitude NUMERIC NOT NULL CHECK(longitude >= -180 AND longitude <= 180), */
	room_type VARCHAR(64) NOT NULL,
	price MONEY NOT NULL,
/*	publish_date date NOT NULL, */
	owner_id VARCHAR(64) REFERENCES user_base(user_id)
		ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	total_occupancy INT NOT NULL,
	total_bedrooms INT NOT NULL,
	has_internet VARCHAR(3) NOT NULL,
	has_aircon VARCHAR(3) NOT NULL,
	has_kitchen VARCHAR(3) NOT NULL,
	has_heater VARCHAR(3) NOT NULL
);

CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE TABLE IF NOT EXISTS reservations(
	reservation_id INT PRIMARY KEY,
	user_id VARCHAR(64) REFERENCES user_base(user_id)
		ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	listing_id INT REFERENCES listings(listing_id)
		ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	date_range DATERANGE NOT NULL,
	EXCLUDE USING GIST (listing_id WITH =, date_range WITH &&)
);

CREATE TABLE IF NOT EXISTS reviews(
	reservation_id INT UNIQUE REFERENCES reservations(reservation_id)
		ON UPDATE CASCADE ON DELETE CASCADE,
	review INT NOT NULL CHECK(review >= 1 AND review <= 5)
);
