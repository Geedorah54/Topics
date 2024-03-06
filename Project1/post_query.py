# PURPOSE: Handle POST Query requests

from extract_data import execute_query, execute_queryD

class AppointmentService:
    # Checks when submitting an appointment
    @staticmethod
    def book_appointment(email, datetime):
        try:
            execute_query("UPDATE patients SET appointment_datetime = %s WHERE email = %s", (datetime, email))
            return True
        except Exception as e:
            print("Error booking appointment:", e)
            return False

    @staticmethod
    def cancel_appointment(email):
        # Checks when deleting an appointment
        try:
            execute_query("UPDATE patients SET appointment_datetime = NULL WHERE email = %s", (email,))
            return True
        except Exception as e:
            print("Error canceling appointment:", e)
            return False
        
class LoginVerify:
    # Retrieves login info
    @staticmethod
    def check_user(username, password):
        try:
            execute_queryD("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
            return True
        except Exception as e:
            print("Incorrect username or password:", e)
            return False

class RegisterUser:
    # Retrieves login info
    @staticmethod
    def check_user(username, password, email):
        try:
            execute_query('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            return True
        except Exception as e:
            print("Incorrect username or password:", e)
            return False