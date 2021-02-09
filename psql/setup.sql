CREATE TABLE IF NOT EXISTS item (
	ItemID integer PRIMARY KEY,
	Icon text NOT NULL,
	Type text NOT NULL,
	Name varchar(100) NOT NULL,
	Description text NOT NULL,
	IsMembers bool NOT NULL);

CREATE TABLE IF NOT EXISTS price (
	/*
		Date cannot be a primary key, this would stop other
		entries from having the same date...
		ItemID cannot be a primary key, this would stop
		the item from having more than one price entry.
		The answer here is a compound key of Date and ItemID!
	*/
	ItemID integer NOT NULL,
	Date date NOT NULL,
	Price integer NOT NULL,
	Trend varchar(12) NOT NULL,
	ChangeToday integer NOT NULL,
	PRIMARY KEY (ItemID, Date));
