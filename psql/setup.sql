CREATE TABLE IF NOT EXISTS item (
	item_id integer PRIMARY KEY,
	icon text NOT NULL,
	type text NOT NULL,
	name varchar(100) NOT NULL,
	description text NOT NULL,
	is_members bool NOT NULL);

CREATE TABLE IF NOT EXISTS price (
	/*
		Date cannot be a primary key, this would stop other
		entries from having the same date...
		ItemID cannot be a primary key, this would stop
		the item from having more than one price entry.
		The answer here is a compound key of Date and ItemID!
	*/
	item_id integer NOT NULL,
	date date NOT NULL,
	price integer NOT NULL,
	trend varchar(12) NOT NULL,
	change_today integer NOT NULL,
	PRIMARY KEY (item_id, date));
