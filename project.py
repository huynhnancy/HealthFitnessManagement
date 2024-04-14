import psycopg2
import datetime

def connect_db():
    try:
        conn = psycopg2.connect(database = "project_db", 
                                user = "postgres", 
                                password = "postgres", 
                                host = "localhost", 
                                port = "5432")
        return conn
    except Exception as e:
        print("Error connecting to database: ", e)
        return None

def member_register():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            name = input("Enter your name: ")
            contact = input("Enter your current contact: ")
            weight = int(input("Enter your current weight: "))
            height = int(input("Enter your current height: "))
            weight_goal = int(input("Enter your weight goal: "))
            time_goal = input("Enter your time goal: ")
            cur.execute("INSERT INTO Members (member_name, contact, weight, height, weight_goal, time_goal) VALUES (%s, %s, %s, %s, %s, %s)", (name, contact, weight, height, weight_goal, time_goal))
            conn.commit()
            print("Account created successfully.")
    except Exception as e:
        print("Error creating account: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()
        
def member_update():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            member_id = int(input("Enter your member ID: "))
            contact = input("Enter your current contact: ")
            weight = int(input("Enter your current weight: "))
            height = int(input("Enter your current height: "))
            weight_goal = int(input("Enter your new weight goal: "))
            time_goal = input("Enter your new time goal: ")
            cur.execute("UPDATE Members SET contact = %s, weight = %s, height = %s, weight_goal = %s, time_goal = %s WHERE member_id = %s", (contact, weight, height, weight_goal, time_goal, member_id))
            conn.commit()
            print("Account updated successfully.")
    except Exception as e:
        print("Error updating account: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()       

def profile_display():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            member_id = int(input("Enter your member ID: "))

            cur.execute("SELECT * FROM Members WHERE member_id = %s", [member_id])
            row = cur.fetchone()
            print("Member ID: ", row[0])
            print("Member Name: ", row[1])
            print("Contact: ", row[2])
            print("Weight: ", row[3])
            print("Height: ", row[4])
            print("Weight Goal: ", row[5])
            print("Time Goal: ", row[6])

            cur.execute("SELECT * FROM Billings WHERE member_id = %s", [member_id])
            print("Billings: ")
            billings = cur.fetchall()
            for billing in billings:
                print("Billing ID: ", billing[0])
                print("Amount: ", billing[2])
                print("Due Date: ", billing[3])
            
            cur.execute("SELECT * FROM Personal_sessions WHERE member_id = %s", [member_id])
            print("Personal Sessions: ")
            sessions = cur.fetchall()
            for session in sessions:
                print("Session ID: ", session[0])
                print("Trainer ID: ", session[2])
                print("Session Date: ", session[3])

            cur.execute("SELECT * FROM Activities WHERE member_id = %s", [member_id])
            print("Registered classes: ")
            activities = cur.fetchall()
            for activity in activities:
                print("Class ID: ", activity[2])
                print("Class Name: ", activity[3])

    except Exception as e:
        print("Error displaying profile: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def personal_session():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            member_id = int(input("Enter member ID: "))
            trainer_id = int(input("Enter trainer ID: "))
            date = input("Enter session date: ")
            #Check available date
            cur.execute("SELECT * FROM Trainers WHERE trainer_id = %s", [trainer_id])
            row = cur.fetchone()[3]
            if row.strftime("%Y-%m-%d") != date:
                print("Trainer is not available on this date.")
                return
            cur.execute("INSERT INTO Personal_sessions (member_id, trainer_id, session_date) VALUES (%s, %s, %s)", (member_id, trainer_id, date))
            cur.execute("UPDATE Trainers SET available_date = NULL WHERE trainer_id = %s", [trainer_id])
            conn.commit()
            print("Personal session added successfully.")
    except Exception as e:
        print("Error adding personal session: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def personal_session_cancel():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            session_id = int(input("Enter session ID to cancel: "))
            cur.execute("DELETE FROM Personal_sessions WHERE session_id = %s", [session_id])
            conn.commit()
            print("Personal session cancelled successfully.")
    except Exception as e:
        print("Error cancelling personal session: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def personal_session_update():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            session_id = int(input("Enter session ID to update: "))
            date = input("Enter new session date: ")
            #Check available date
            cur.execute("SELECT * FROM Personal_sessions WHERE session_id = %s", [session_id])
            trainer_id = cur.fetchone()[1]
            cur.execute("SELECT * FROM Trainers WHERE trainer_id = ", [trainer_id])
            row = cur.fetchone()[3]
            if row.strftime("%Y-%m-%d") != date:
                print("Trainer is not available on this date.")
                return
            cur.execute("UPDATE Trainers SET available_date = NULL WHERE trainer_id = (SELECT trainer_id FROM Personal_sessions WHERE session_id = %s)", [session_id])
            cur.execute("UPDATE Personal_sessions SET session_date = %s WHERE session_id = %s", (date, session_id))
            conn.commit()
            print("Personal session updated successfully.")
    except Exception as e:
        print("Error updating personal session: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def class_register():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            member_id = int(input("Enter member ID: "))
            class_id = int(input("Enter class ID: "))
            cur.execute("SELECT * FROM Classes WHERE class_id = %s", [class_id])
            class_name = cur.fetchone()[1]
            cur.execute("INSERT INTO Activities (member_id, class_id, class_name) VALUES (%s, %s, %s)", (member_id, class_id, class_name))
            conn.commit()
            print("Class registered successfully.")
    except Exception as e:
        print("Error registering for class: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def member_delete():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            member_id = int(input("Enter member ID to delete: "))
            cur.execute("DELETE FROM Members WHERE member_id = %s", [member_id])
            conn.commit()
            print("Account deleted successfully.")
    except Exception as e:
        print("Error deleting account: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def trainer_register():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            name = input("Enter your name: ")
            contact = input("Enter your current contact: ")
            available = input("Enter your available date: ")
            cur.execute("INSERT INTO Trainers (trainer_name, contact, available_date) VALUES (%s, %s, %s)", (name, contact, available))
            conn.commit()
            print("Trainer account created successfully.")
    except Exception as e:
        print("Error creating trainer account: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def trainer_update():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            trainer_id = int(input("Enter your trainer ID: "))
            contact = input("Enter your current contact: ")
            available = input("Enter your new available date: ")
            cur.execute("UPDATE Trainers SET contact = %s, available_date = %s WHERE trainer_id = %s", (contact, available, trainer_id))
            conn.commit()
            print("Trainer account updated successfully.")
    except Exception as e:
        print("Error updating trainer account: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def trainer_delete():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            trainer_id = int(input("Enter trainer ID to delete: "))
            cur.execute("DELETE FROM Trainers WHERE trainer_id = %s", [trainer_id])
            conn.commit()
            print("Trainer account deleted successfully.")
    except Exception as e:
        print("Error deleting trainer account: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def view_member():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            member_name = input("Enter member name to view: ")
            cur.execute("SELECT * FROM Members where member_name = %s", [member_name])
            rows = cur.fetchall()
            for row in rows:
                print("Member ID: ", row[0])
                print("Member Name: ", row[1])
                print("Contact: ", row[2])
                print("Weight: ", row[3])
                print("Height: ", row[4])
                print("Weight Goal: ", row[5])
                print("Time Goal: ", row[6])

    except Exception as e:
        print("Error viewing member: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def admin_register():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            admin_name = input("Enter your name: ")
            cur.execute("INSERT INTO Admins (admin_name) VALUES (%s)", [admin_name])
            conn.commit()
            print("Admin account created successfully.")
    except Exception as e:
        print("Error creating admin account: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def room_booking():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            room_id= input("Enter room id: ")
            cur.execute("SELECT * FROM Rooms WHERE room_id = %s", [room_id])
            row = cur.fetchone()
            print("Room ID: ", row[0])
            print("Room Name: ", row[1])
            print("Booked: ", row[3])
            option = input("Do you want to book or cancel the room? (book/cancel): ")
            if option == "cancel":
                contact = None
                status = "FALSE"
            elif option == "book":
                #check availability
                if row[3] == True:
                    print("Room is already booked.")
                    return
                contact = input("Enter your contact: ")
                status = "TRUE"
            cur.execute("UPDATE Rooms SET booking_contact = %s, status = %s WHERE room_id = %s", (contact, status, room_id))
            conn.commit()
            print("Room updated successfully.")
    except Exception as e:
        print("Error updating room: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def equipment_maintenance():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            equipment_id= input("Enter equipment id to maintain: ")
            status = input("Enter maintenance status (TRUE = Working, FALSE = Not working): ")
            cur.execute("UPDATE Equipments SET status = %s WHERE equip_id = %s", (status, equipment_id))
            conn.commit()
            print("Equipment maintenance updated successfully.")
    except Exception as e:
        print("Error updating maintenance: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def class_schedule():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            class_name= input("Enter class name: ")
            class_date= input("Enter class date: ")
            cur.execute("INSERT INTO Classes (class_name, class_date) VALUES (%s, %s)", (class_name, class_date))
            conn.commit()
            print("Class schedule updated successfully.")
    except Exception as e:
        print("Error updating class schedule: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def class_cancel():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            class_id= input("Enter class id to cancel: ")
            cur.execute("DELETE FROM Classes WHERE class_id = %s", [class_id])
            cur.execute("DELETE FROM Activities WHERE class_id = %s", [class_id])
            conn.commit()
            print("Class cancelled successfully.")
    except Exception as e:
        print("Error cancelling class: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def billing():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            member_id = int(input("Enter member ID: "))
            amount = int(input("Enter amount to pay: "))
            due_date = input("Enter due date: ")
            cur.execute("INSERT INTO Billings (member_id, amount, due_date) VALUES (%s, %s, %s)", (member_id, amount, due_date))
            conn.commit()
            print("Billing entered successfully.")
    except Exception as e:
        print("Error billing: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def billing_update():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            billing_id = int(input("Enter billing ID: "))
            amount = int(input("Enter current amount to pay: "))
            due_date = input("Enter due date: ")
            cur.execute("UPDATE Billings SET amount = %s, due_date = %s WHERE billing_id = %s", (amount, due_date, billing_id))
            conn.commit()
            print("Billing updated successfully.")
    except Exception as e:
        print("Error updating billing: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def view_all_billings():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Billings")
            billings = cur.fetchall()
            for billing in billings:
                print(billing)
    except Exception as e:
        print("Error viewing billing: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def view_personal_sessions():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Personal_sessions")
            sessions = cur.fetchall()
            for session in sessions:
                print(session)
    except Exception as e:
        print("Error viewing personal sessions: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def view_class_schedule():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Classes")
            classes = cur.fetchall()
            for session in classes:
                print(session)
    except Exception as e:
        print("Error viewing class schedule: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def view_all_equipments():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Equipments")
            equipments = cur.fetchall()
            for equipment in equipments:
                print(equipment)
    except Exception as e:
        print("Error viewing equipments: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def view_all_rooms():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Rooms")
            rooms = cur.fetchall()
            for room in rooms:
                print(room)
    except Exception as e:
        print("Error viewing room: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def view_all_members():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Members")
            members = cur.fetchall()
            for member in members:
                print(member)
    except Exception as e:
        print("Error viewing members: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def view_all_trainers():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Trainers")
            trainers = cur.fetchall()
            for trainer in trainers:
                print(trainer)
    except Exception as e:
        print("Error viewing trainers: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def view_all_admins():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Admins")
            admins = cur.fetchall()
            for admin in admins:
                print(admin)
    except Exception as e:
        print("Error viewing admins: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def view_all_activities():
    try:
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Activities")
            activities = cur.fetchall()
            for activity in activities:
                print(activity)
    except Exception as e:
        print("Error viewing activities: ", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def main():
    print("Welcome to the gym management system.")
    print("1. Member")
    print("2. Trainer")
    print("3. Admin")
    print("4. Exit")
    while True:
        option = int(input("Select your role: "))
        if option == 1:
            print("1. Register")
            print("2. Update")
            print("3. Display Profile")
            print("4. Personal Session")
            print("5. Cancel Personal Session")
            print("6. Update Personal Session")
            print("7. Register for Class")
            print("8. Delete Account")
            choice = int(input("Select your choice: "))
            if choice == 1:
                member_register()
            elif choice == 2:
                member_update()
            elif choice == 3:
                profile_display()
            elif choice == 4:
                personal_session()
            elif choice == 5:
                personal_session_cancel()
            elif choice == 6:
                personal_session_update()
            elif choice == 7:
                class_register()
            elif choice == 8:
                member_delete()
        elif option == 2:
            print("1. Register")
            print("2. Update")
            print("3. Delete")
            print("4. Display Member Profile")
            choice = int(input("Select your choice: "))
            if choice == 1:
                trainer_register()
            elif choice == 2:
                trainer_update()
            elif choice == 3:
                trainer_delete()
            elif choice == 4:
                view_member()
        elif option == 3:
            print("1. Register")
            print("2. Room Booking")
            print("3. Equipment Maintenance")
            print("4. Class Schedule")
            print("5. Cancel Class")
            print("6. Billing")
            print("7. Update Billing")
            print("8. View Personal Session")
            print("9. View Class Schedule")
            print("10. View All Equipments")
            print("11. View All Rooms")
            print("12. View All Members")
            print("13. View All Trainers")
            print("14. View All Admins")
            print("15. View All Billings")
            print("16. View All Activities")
            choice = int(input("Select your choice: "))
            if choice == 1:
                admin_register()
            elif choice == 2:
                room_booking()
            elif choice == 3:
                equipment_maintenance()
            elif choice == 4:
                class_schedule()
            elif choice == 5:
                class_cancel()
            elif choice == 6:
                billing()
            elif choice == 7:
                billing_update()
            elif choice == 8:
                view_personal_sessions()
            elif choice == 9:
                view_class_schedule()
            elif choice == 10:
                view_all_equipments()
            elif choice == 11:
                view_all_rooms()
            elif choice == 12:
                view_all_members()
            elif choice == 13:
                view_all_trainers()
            elif choice == 14:
                view_all_admins()
            elif choice == 15:
                view_all_billings()
            elif choice == 16:
                view_all_activities()
        elif option == 4:
            break

main()