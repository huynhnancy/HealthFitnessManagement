-- Sample data for Admins table
INSERT INTO Admins (admin_name) VALUES
('Admin 1'),
('Admin 2'),
('Admin 3');

-- Sample data for Trainers table
INSERT INTO Trainers (trainer_name, contact, available_date) VALUES
('Trainer 1', '123-456-7890', '2024-04-15'),
('Trainer 2', '987-654-3210', '2024-04-16'),
('Trainer 3', '555-555-5555', '2024-04-17');

-- Sample data for Members table
INSERT INTO Members (member_name, contact, weight, height, weight_goal, time_goal) VALUES
('Member 1', '111-111-1111', 70, 170, 65, '3 months'),
('Member 2', '222-222-2222', 65, 165, 60, '6 months'),
('Member 3', '333-333-3333', 80, 180, 75, '1 year');

-- Sample data for Class table
INSERT INTO Classes (class_name, class_date) VALUES
('Yoga Class', '2024-04-15'),
('Zumba Class', '2024-04-16'),
('Pilates Class', '2024-04-17');

-- Sample data for Room table
INSERT INTO Rooms (room_name, booking_contact, status) VALUES
('Room 1', 444-444-4444, true),
('Room 2', 666-666-6666, true),
('Room 3', NULL, false);

-- Sample data for Equipment table
INSERT INTO Equipments (equip_name, status) VALUES
('Treadmill', true),
('Elliptical', true),
('Dumbbells', false);
