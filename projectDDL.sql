DROP TABLE IF EXISTS Admins;
DROP TABLE IF EXISTS Trainers CASCADE;
DROP TABLE IF EXISTS Members CASCADE;
DROP TABLE IF EXISTS Personal_sessions;
DROP TABLE IF EXISTS Classes CASCADE;
DROP TABLE IF EXISTS Rooms;
DROP TABLE IF EXISTS Billings;
DROP TABLE IF EXISTS Equipments;
DROP TABLE IF EXISTS Activities;

-- Table for storing trainers
CREATE TABLE Trainers (
    trainer_id SERIAL PRIMARY KEY,
    trainer_name VARCHAR(255) NOT NULL,
    contact VARCHAR(255),
    available_date DATE
);

-- Table for storing members
CREATE TABLE Members (
    member_id SERIAL PRIMARY KEY,
    member_name VARCHAR(255) NOT NULL,
    contact VARCHAR(255),
    weight INT NOT NULL,
    height INT NOT NULL,
    weight_goal INT NOT NULL,
    time_goal VARCHAR(255)
);

-- Table for storing admins
CREATE TABLE Admins (
    admin_id SERIAL PRIMARY KEY,
    admin_name VARCHAR(255) NOT NULL
);

-- Table for storing personal sessions
CREATE TABLE Personal_sessions (
    session_id SERIAL PRIMARY KEY,
    trainer_id INT REFERENCES Trainers(trainer_id),
    member_id INT REFERENCES Members(member_id),
    session_date DATE NOT NULL
);

-- Table for storing classes
CREATE TABLE Classes (
    class_id SERIAL PRIMARY KEY,
	class_name VARCHAR(255) NOT NULL,
    class_date DATE NOT NULL
);

-- Table for storing rooms and their bookings
CREATE TABLE Rooms (
    room_id SERIAL PRIMARY KEY,
	room_name VARCHAR(255) NOT NULL,
	booking_contact VARCHAR(255),
    status BOOLEAN
);

-- Table for storing billing information
CREATE TABLE Billings (
    billing_id SERIAL PRIMARY KEY,
	member_id INT REFERENCES Members(member_id),
    amount DECIMAL(10,2) NOT NULL,
    due_date DATE NOT NULL
);

-- Table for storing equipment
CREATE TABLE Equipments (
    equip_id SERIAL PRIMARY KEY,
    equip_name VARCHAR(255) NOT NULL,
    status BOOLEAN
);

--Table for storing member activities
CREATE TABLE Activities (
	activitiy_id SERIAL PRIMARY KEY,
	member_id INT REFERENCES Members(member_id),
	class_id INT REFERENCES Classes(class_id),
	class_name VARCHAR(255)
);
