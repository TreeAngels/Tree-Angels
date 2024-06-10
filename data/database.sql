-- sqlite
CREATE TABLE IF NOT EXISTS Login (
    username VARCHAR(45) PRIMARY KEY,
    hash VARCHAR(255) NOT NULL,
privilege VARCHAR(50) NOT NULL CHECK (privilege IN ('admin', 'organization', 'donor'))
);

CREATE TABLE IF NOT EXISTS Donor (
    username VARCHAR(45) PRIMARY KEY,
    donorID INTEGER AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    FOREIGN KEY (username) REFERENCES Login(username)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS DonorDonations (
    donorID INTEGER,
    doneeID INTEGER,
    itemID INTEGER,
    FOREIGN KEY (donorID) REFERENCES Donor(donorID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (doneeID) REFERENCES Donee(doneeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (itemID) REFERENCES Item(itemID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Household (
    householdID INTEGER AUTO_INCREMENT PRIMARY KEY,
    primaryParentFirstName VARCHAR (50) NOT NULL,
    primaryParentMiddleName VARCHAR (50),
    primaryParentLastName VARCHAR (50) NOT NULL,
    primaryParentDOB VARCHAR (50) NOT NULL,
    householdAddress VARCHAR (300),
    primaryParentPhone INTEGER NOT NULL,
    primaryParentEmail VARCHAR (100),
    FOREIGN KEY (orgID) REFERENCES Organization(orgID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Organization (
    username VARCHAR(45) PRIMARY KEY,
    orgID INTEGER AUTO_INCREMENT PRIMARY KEY,
    orgName VARCHAR (200) NOT NULL,
    address VARCHAR (300) NOT NULL,
    FOREIGN KEY (username) REFERENCES Login(username)
        ON UPDATE CASCADE
        ON DELETE CASCADE
 );

CREATE TABLE IF NOT EXISTS DoneeItem (
    doneeID INTEGER,
    itemID INTEGER,
    FOREIGN KEY (doneeID) REFERENCES Donee(doneeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (itemID) REFERENCES Item(itemID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Item (
    itemID INTEGER AUTO_INCREMENT PRIMARY KEY,
    itemName VARCHAR(100) NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS ItemPicture (
    doneeID INTEGER,
    itemID VARCHAR(100) NOT NULL,
    FOREIGN KEY (doneeID) REFERENCES Donee(doneeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Donee (
    doneeID INTEGER AUTO_INCREMENT PRIMARY KEY,
    gender VARCHAR(50),
    realFirstName VARCHAR(50) NOT NULL,
    realLastName VARCHAR(50) NOT NULL,
    displayName VARCHAR(50) NOT NULL,
    latitude REAL,
    longitude REAL,
    bio VARCHAR(250),
    shirtSize VARCHAR(10),
    pantsSize VARCHAR(10),
    coatSize VARCHAR(10),
    shoeSize VARCHAR(10),
    householdID INTEGER NOT NULL,
    orgID INTEGER NOT NULL,
    FOREIGN KEY (householdID) REFERENCES Household(householdID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (orgID) REFERENCES Organization(orgID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- INSERT INTO Login (username, hash, privilidge) VALUES ('Logan', 'scrypt:32768:8:1$khfz1gL0pVReBaIE$2f526838be140c82900602b9a61781a0bcaa8be90c87e8e7d5e7356b83ca2d427ff143749dc1f06826b308ac40056f1aaf4400e544f540cb873ece8eab737b64', 'admin');
-- INSERT INTO Login (username, hash, privilidge) VALUES ('Jacob', 'scrypt:32768:8:1$khfz1gL0pVReBaIE$2f526838be140c82900602b9a61781a0bcaa8be90c87e8e7d5e7356b83ca2d427ff143749dc1f06826b308ac40056f1aaf4400e544f540cb873ece8eab737b64', 'admin');
-- INSERT INTO Login (username, hash, privilidge) VALUES ('Vikyat', 'scrypt:32768:8:1$khfz1gL0pVReBaIE$2f526838be140c82900602b9a61781a0bcaa8be90c87e8e7d5e7356b83ca2d427ff143749dc1f06826b308ac40056f1aaf4400e544f540cb873ece8eab737b64', 'admin');