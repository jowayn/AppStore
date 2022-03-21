CREATE TABLE IF NOT EXISTS user_base(
	user_id VARCHAR(64) PRIMARY KEY, 
	user_password VARCHAR(64) NOT NULL, 
	first_name VARCHAR(64) NOT NULL, 
	last_name VARCHAR(64) NOT NULL, 
	phone_number VARCHAR(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS listings(
	listing_id VARCHAR(64) PRIMARY KEY, 
	listing_name VARCHAR(64) NOT NULL,
	neighbourhood VARCHAR(64) NOT NULL,
	neighbourhood_group VARCHAR(64) NOT NULL,
	address VARCHAR(128) NOT NULL,
	latitude NUMERIC NOT NULL CHECK(latitude >= -90 AND latitude <= 90),
	longitude NUMERIC NOT NULL CHECK(longitude >= -180 AND longitude <= 180),
	room_type VARCHAR(64) NOT NULL,
	price MONEY NOT NULL,
	publish_date date NOT NULL,
	owner_id VARCHAR(64) REFERENCES user_base(user_id)
		ON UPDATE CASCADE ON DELETE CASCADE,
	total_occupancy INT NOT NULL,
	total_bedrooms INT NOT NULL,
	has_internet BOOLEAN NOT NULL,
	has_aircon BOOLEAN NOT NULL,
	has_kitchen BOOLEAN NOT NULL,
	has_heater BOOLEAN NOT NULL
);

CREATE EXTENSION btree_gist;
CREATE TABLE IF NOT EXISTS reservations(
	reservation_id VARCHAR(20) PRIMARY KEY,
	user_id VARCHAR(64) REFERENCES user_base(user_id)
		ON UPDATE CASCADE ON DELETE CASCADE,
	total_price MONEY NOT NULL,
	listing_id VARCHAR(64) REFERENCES listings(listing_id)
		ON UPDATE CASCADE ON DELETE CASCADE,
	date_range DATERANGE NOT NULL,
	EXCLUDE USING GIST (room_id WITH =, date_range WITH &&)
);

CREATE TABLE IF NOT EXISTS reviews(
	reservation_id VARCHAR(20) UNIQUE REFERENCES reservations(reservation_id)
		ON UPDATE CASCADE ON DELETE CASCADE,
	review DECIMAL(3) NOT NULL CHECK(review >= 1 AND review <= 5)
);


