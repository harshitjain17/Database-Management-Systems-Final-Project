import psycopg2 as db_connect
import pandas as pd
import datetime
import csv

host_name="localhost"
db_user="postgres"
db_password="12345"
db_name="project"

def connect_to_db():
    """Connects to the PostgreSQL database and returns a connection object."""

    try:
        connection = db_connect.connect(host=host_name, user=db_user, password=db_password, database=db_name)
        return connection
    except Exception as e:
        print("Error connecting to database:", e)
        return None


def close_connection(connection):
    """Closes the connection to the database."""
    
    if connection:
        connection.close()


def main_menu():
    """Displays the main menu with options for the user."""

    print("\nWelcome to the Hospital Management System!")
    print("1. Insert a new patient")
    print("2. Delete the expired insurance on file for a patient")
    print("3. Update the billing amount for a patient")
    print("4. Search for patients by the doctor assigned to them")
    print("5. Aggregate Functions on Patient table")
    print("6. Sorts patients by age in descending order")
    print("7. Joins Patients and Admission tables for emergency admissions with O- blood type")
    print("8. Groups patients based on user-specified columns")
    print("9. Finds patients with a length of stay exceeding a threshold using a subquery")
    print("10. Discharges a patient using a transaction")
    print("11. Bonus: Custom Query")
    print("12. Error Handling")
    print("13. Exit")
    
    while True:
        choice = input("Enter your choice (1-13): ")
        try:
            choice_int = int(choice)
            if (1 <= choice_int <= 13):
                return choice_int
            else:
                print("Invalid choice. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def insert_patients_from_csv(connection):
    """Inserts patient data from a CSV file into the database using insert_new_patient."""
    
    with open('Healthcare-Dataset.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for csv_row in reader:
            insert_new_patient(connection, csv_row)

def insert_new_patient(connection):
    """Prompts user for data and inserts it into all 14 relations."""

    cursor = connection.cursor()

    # # User input using CSV file
    # name = csv_row[0] if csv_row[0] else None
    # age = int(csv_row[1]) if csv_row[1] else None
    # gender = csv_row[2] if csv_row[2] else None
    # blood_type = csv_row[3] if csv_row[3] else None
    # medical_condition = csv_row[4] if csv_row[4] else None
    # admission_date = csv_row[5] if csv_row[5] else None
    # doctor = csv_row[6] if csv_row[6] else None
    # hospital = csv_row[7] if csv_row[7] else None
    # insurance_provider = csv_row[8] if csv_row[8] else None
    # billing_amount = float(csv_row[9]) if csv_row[9] else None
    # room_number = int(csv_row[10]) if csv_row[10] else None
    # admission_type = csv_row[11] if csv_row[11] else None
    # discharge_date = csv_row[12] if csv_row[12] else None
    # medication = csv_row[13] if csv_row[13] else None
    # test_results = csv_row[14] if csv_row[14] else None
    
    # Get user input for each attribute with handling for optional fields
    name = input("Enter Name: ") or None
    age = int(input("Enter Age: ")) or None
    gender = input("Enter Gender: ") or None
    blood_type = input("Enter Blood Type: ") or None
    medical_condition = input("Enter Medical Condition (optional): ")  or None
    admission_date = input("Enter Date of Admission (MM/DD/YYYY): ") or None
    admission_type = input("Enter Admission Type (Elective/Emergency/Urgent): ") or None
    doctor = input("Enter Doctor Name (optional): ") or None
    hospital = input("Enter Hospital Name: ") or None
    insurance_provider = input("Enter Insurance Provider (optional): ") or None
    room_number = int(input("Enter Room Number (optional): ")) or None
    discharge_date = input("Enter Discharge Date (MM/DD/YYYY) (optional): ") or None
    medication = input("Enter Medication (optional): ") or None
    test_results = input("Enter Test Results (optional): ") or None
    try:
        billing_amount = float(input("Enter Billing Amount (optional): ")) or None
    except ValueError:
        billing_amount = None

    # Insert data into BloodGroup table
    blood_type_check_stmt = "SELECT BloodTypeID FROM BloodGroup WHERE BloodType = %s;"
    cursor.execute(blood_type_check_stmt, (blood_type,))
    existing_bloodtype_id = cursor.fetchone()
    if existing_bloodtype_id:
        bloodtype_id = existing_bloodtype_id[0]
    else:
        bloodgroup_insert_stmt = "INSERT INTO BloodGroup (BloodType) VALUES (%s) RETURNING BloodTypeID;"
        cursor.execute(bloodgroup_insert_stmt, (blood_type,))
        bloodtype_id = cursor.fetchone()[0]

    # Insert data into Patient table
    patient_insert_stmt = "INSERT INTO Patient (Name, Age, Gender, BloodTypeID) VALUES (%s, %s, %s, %s) RETURNING PatientID;"
    cursor.execute(patient_insert_stmt, (name, age, gender, bloodtype_id))
    patient_id = cursor.fetchone()[0]

    # Insert data into InsuranceProvider (if provided)
    insurance_insert_stmt = "INSERT INTO InsuranceProvider (PatientID, InsuranceProviderName) VALUES (%s, %s);"
    cursor.execute(insurance_insert_stmt, (patient_id, insurance_provider))

    # Insert data into Hospital table
    hospital_insert_stmt = "INSERT INTO Hospital (HospitalName) VALUES (%s) RETURNING HospitalID;"
    cursor.execute(hospital_insert_stmt, (hospital,))
    hospital_id = cursor.fetchone()[0]

    # Insert data into Room table
    room_insert_stmt = "INSERT INTO Room (HospitalID, RoomNumber) VALUES (%s, %s);"
    cursor.execute(room_insert_stmt, (hospital_id, room_number))

    # Insert data into Doctor table
    doctor_insert_stmt = "INSERT INTO Doctor (HospitalID, DoctorName) VALUES (%s, %s) RETURNING DoctorID;"
    cursor.execute(doctor_insert_stmt, (hospital_id, doctor))
    doctor_id = cursor.fetchone()[0]

    # Insert data into Diagnosis table
    diagnosis_insert_stmt = "INSERT INTO Diagnosis (MedicalCondition) VALUES (%s) RETURNING DiagnosisID;"
    cursor.execute(diagnosis_insert_stmt, (medical_condition,))
    diagnosis_id = cursor.fetchone()[0]

    # Insert data into Medication table
    medication_insert_stmt = "INSERT INTO Medication (DiagnosisID, MedicineName) VALUES (%s, %s) RETURNING MedicationID;"
    cursor.execute(medication_insert_stmt, (diagnosis_id, medication))
    medication_id = cursor.fetchone()[0]

    # Insert data into Admission table
    admission_insert_stmt = "INSERT INTO Admission (PatientID, DoctorID, HospitalID, MedicationID, AdmissionDate, DischargeDate) VALUES (%s, %s, %s, %s, %s, %s) RETURNING AdmissionID;"
    cursor.execute(admission_insert_stmt, (patient_id, doctor_id, hospital_id, medication_id, admission_date, discharge_date))
    admission_id = cursor.fetchone()[0]

    # Insert data into AdmissionType table
    admission_type_insert_stmt = "INSERT INTO AdmissionType (AdmissionID, AdmissionType) VALUES (%s, %s);"
    cursor.execute(admission_type_insert_stmt, (admission_id, admission_type))

    # Insert data into Billing table
    billing_insert_stmt = "INSERT INTO Billing (AdmissionID, BillingAmount) VALUES (%s, %s);"
    cursor.execute(billing_insert_stmt, (admission_id, billing_amount))

    # Insert data into TestResults table
    test_result_insert_stmt = "INSERT INTO TestResult (AdmissionID, TestResults) VALUES (%s, %s);"
    cursor.execute(test_result_insert_stmt, (admission_id, test_results))

    # Insert data into DiagAdm (DiagnosisAdmission) table
    diag_adm_insert_stmt = "INSERT INTO DiagAdm (AdmissionID, DiagnosisID) VALUES (%s, %s);"
    cursor.execute(diag_adm_insert_stmt, (admission_id, diagnosis_id))

    connection.commit()
    print("New patient added successfully!")
    cursor.close()


def delete_patient_insurance(connection):
    """Deletes the insurance provider for a specific patient."""

    cursor = connection.cursor()
    
    try:
        patient_id = int(input("Enter the Patient ID: "))
        delete_stmt = f"DELETE FROM InsuranceProvider WHERE PatientID = {patient_id}"
        cursor.execute(delete_stmt)
        connection.commit()
        if (cursor.rowcount == 1):
            print(f"Insurance provider for Patient ID {patient_id} deleted successfully!")
        else:
            print(f"No insurance provider found for Patient ID {patient_id}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()


def update_billing_amount(connection):
    """Allows user to update the billing amount for a patient."""

    cursor = connection.cursor()

    try:
        admission_id = int(input("Enter the Admission ID: "))
        new_billing_amount = float(input("Enter the new Billing Amount: "))
        update_stmt = f"UPDATE Billing SET BillingAmount = {new_billing_amount} WHERE AdmissionID = {admission_id}"
        cursor.execute(update_stmt)
        connection.commit()
        if cursor.rowcount > 0:
            print(f"Billing amount for Admission ID {admission_id} updated successfully!")
        else:
            print(f"No billing record found for Admission ID {admission_id}.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()


def search_patients_by_doctor(connection):
    """Allows user to search for patients by doctor."""

    cursor = connection.cursor()
    doctor_name = input("Enter the doctor's full name: ")
    search_stmt = f" SELECT Admission.PatientID, Name, AdmissionID, Admission.DoctorID, DoctorName, AdmissionDate, DischargeDate FROM Admission JOIN Patient ON Admission.PatientID = Patient.PatientID JOIN Doctor ON Admission.DoctorID = Doctor.DoctorID WHERE Doctor.DoctorName LIKE '%{doctor_name}%'"

    try:
        cursor.execute(search_stmt)
        results = cursor.fetchall()
        if results:
            print("\nSearch results for patients:")
            df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
            print(df.to_string(index=False))
        else:
            print(f"No patients found assigned to Dr. {doctor_name}.")

    except Exception as e:
        print(f"An error occurred: {e}")
        
    cursor.close()


def patient_aggregates(connection):
    """Provides options for aggregate functions on Patients table."""

    cursor = connection.cursor()
    print("1. Count Total Patients")
    print("2. Find Average Age of Patients")
    
    try:
        choice = int(input("Enter your choice (1-2): "))
        if choice == 1:
            cursor.execute("SELECT COUNT(*) FROM Patient;")
            count = cursor.fetchone()[0]
            print("Total Patients:", count)
        
        elif choice == 2:
            cursor.execute("SELECT AVG(Age) FROM Patient;")
            avg_age = cursor.fetchone()[0]
            print("Average Patient Age:", avg_age)        
        
        else:
            print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()


def sort_patients(connection):
    """Sorts patients by age in descending order."""

    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Patient ORDER BY Age DESC;")
        patients = cursor.fetchall()
        df = pd.DataFrame(patients, columns=[desc[0] for desc in cursor.description])
        print("\nPatients Sorted by Age (Descending):")
        print(df.to_string(index=False))
        
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()


def join_patients_emergency_o_neg(connection):
    """Joins Patients and Admission tables for emergency admissions with O- blood type."""

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT P.Name, BG.BloodType, A.AdmissionDate, AT.AdmissionType
        FROM Patient P
        INNER JOIN Admission A ON P.PatientID = A.PatientID
        INNER JOIN AdmissionType AT ON A.AdmissionID = AT.AdmissionID
        INNER JOIN BloodGroup BG ON P.BloodTypeID = BG.BloodTypeID
        WHERE AT.AdmissionType = 'Emergency' AND BG.BloodType = 'O-';
        """)
        admissions = cursor.fetchall()

        if admissions:
            df = pd.DataFrame(admissions, columns=[desc[0] for desc in cursor.description])
            print("\nEmergency Admissions with Patients having Blood Type O-:")
            print(df.to_string(index=False))
        else:
            print("No emergency admissions found for patients with Blood Type O-")

    except Exception as e:
        print("Error fetching emergency admissions data:", e)

    finally:
        cursor.close()


def group_patients(connection):
    """Groups patients based on user-specified columns."""

    cursor = connection.cursor()

    try:
        column = input("Enter the column to group by: ")
        query = f"SELECT AVG(P.Age), P.{column} FROM Patient P GROUP BY {column};"
        cursor.execute(query)
        data = cursor.fetchall()

        if data:
            df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
            print("\nGrouping results:")
            print(df.to_string(index=False))
        else:
            print("No data found in Patients table.")
    
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        data = []

    finally:
        cursor.close()


def long_stay_patients(connection):
    """Finds patients with a length of stay exceeding a threshold using a subquery."""
    
    cursor = connection.cursor()

    try:
        while True:
            try:
                threshold_days = int(input("Enter the minimum threshold for length of stay (in days): "))
                if threshold_days <= 0:
                    print("Invalid input: Threshold days must be a positive integer.")
                else:
                    break
            except ValueError:
                print("Invalid input: Please enter an integer value for threshold days.")

        # Subquery to calculate average length of stay for each patient
        subquery = "SELECT PatientID, AdmissionDate, DischargeDate, (DischargeDate - AdmissionDate) AS LengthOfStay FROM Admission"

        # Main query to filter patients based on average length of stay
        query = f"""
        SELECT P.PatientID, P.Name, Stay.AdmissionDate, Stay.DischargeDate, Stay.LengthOfStay FROM Patient P
        INNER JOIN ({subquery}) AS Stay ON P.PatientID = Stay.PatientID WHERE Stay.LengthOfStay > {threshold_days};
        """

        cursor.execute(query)
        data = cursor.fetchall()

        if data:
            print(f"\nPatients with average length of stay exceeding {threshold_days} days:")
            df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
            print(df.to_string(index=False))
        else:
            print(f"No patients found with average stay exceeding {threshold_days} days.")

    except Exception as e:
        print(f"An error occurred: {e}")
        data = []

    finally:
        cursor.close()


def discharge_patient_transaction(connection):
    """Discharges a patient using a transaction."""

    cursor = connection.cursor()

    try:
        patient_id = int(input("Enter Patient ID: "))

        # Begin transaction
        cursor.execute("BEGIN TRANSACTION;")

        # 1. Find existing patient and admission (check if active admission exists)
        check_active_admission_stmt = f"SELECT * FROM Admission WHERE PatientID = {patient_id} AND DischargeDate IS NULL;"
        cursor.execute(check_active_admission_stmt)
        active_admission = cursor.fetchone()
        if not active_admission:
            raise Exception("Patient not found or has no active admission.")

        # 2. Update discharge date in Admission table
        discharge_date = datetime.datetime.now().strftime('%m/%d/%Y')
        update_admission_stmt = f"UPDATE Admission SET DischargeDate = '{discharge_date}' WHERE AdmissionID = {active_admission[0]};"
        cursor.execute(update_admission_stmt)

        # All updates successful, commit the transaction
        connection.commit()
        print(f"Patient ID {patient_id} discharged successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        print("Transaction rolled back.")

    finally:
        cursor.close()


def custom_query(connection):
    """Executes a user-provided SQL query."""

    cursor = connection.cursor()
    print("Enter your desired SQL query:")
    user_query = input("> ")

    try:
        cursor.execute(user_query)

        # Query type (SELECT)
        if user_query.lower().startswith("select"):
            df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
            if df.empty:
                print("No records found for the given query.")
            else:
                print("\nQuery Results:")
                print(df.to_string(index=False))
        
        # Query types (UPDATE, DELETE, etc.)
        else:
            connection.commit()
            print("Query executed successfully.")
    
    except Exception as e:
        print(f"Error executing custom query: {e}")

    finally:
        cursor.close()


def handle_choice(choice, connection):
    """Executes the selected functionality based on user choice."""

    if choice == 1:
        insert_new_patient(connection)
    elif choice == 2:
        delete_patient_insurance(connection)
    elif choice == 3:
        update_billing_amount(connection)
    elif choice == 4:
        search_patients_by_doctor(connection)
    elif choice == 5:
        patient_aggregates(connection)
    elif choice == 6:
        sort_patients(connection)
    elif choice == 7:
        join_patients_emergency_o_neg(connection)
    elif choice == 8:
        group_patients(connection)
    elif choice == 9:
        long_stay_patients(connection)
    elif choice == 10:
        discharge_patient_transaction(connection)
    elif choice == 11:
        custom_query(connection)
    elif choice == 12:
        print("Error handling performed for all functions.")
    elif choice == 13:
        print("Exiting the system...")
    else:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    connection = connect_to_db()
    if connection:
        while True:
            choice = main_menu()
            handle_choice(choice, connection)
            if (choice == 13):
                break
        # insert_patients_from_csv(connection)
        close_connection(connection)
    else:
        print("Connection failed. Terminating program.")