import psycopg2 as db_connect

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
    print("1. Insert Data")
    print("2. Delete Data")
    print("3. Update Data")
    print("4. Search Data")
    print("5. Aggregate Functions")
    print("6. Sorting")
    print("7. Joins")
    print("8. Grouping")
    print("9. Subqueries")
    print("10. Transactions")
    print("11. Error Handling")
    print("12. Exit")
    
    while True:
        choice = input("Enter your choice (1-12): ")
        try:
            choice_int = int(choice)
            if (1 <= choice_int <= 12):
                return choice_int
            else:
                print("Invalid choice. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def insert_data(connection):
    """Prompts user for data and inserts it into all 14 entities."""

    cursor = connection.cursor()

    # Get user input for each attribute with handling for optional fields
    name = input("Enter Name: ") or None
    age = int(input("Enter Age: ")) or None
    gender = input("Enter Gender: ") or None
    blood_type = input("Enter Blood Type: ") or None
    medical_condition = input("Enter Medical Condition (optional): ")  or None
    admission_date = input("Enter Date of Admission (MM/DD/YYYY): ") or None
    admission_type = input("Enter Admission Type: ") or None
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
        print("Invalid input for billing amount. Skipping.")

    # Insert data into BloodGroup table
    bloodgroup_insert_stmt = "INSERT INTO BloodGroup (BloodType) VALUES (%s) RETURNING BloodTypeID;"
    cursor.execute(bloodgroup_insert_stmt, (blood_type,))
    bloodtype_id = cursor.fetchone()[0]

    # Insert data into Patient table
    patient_insert_stmt = "INSERT INTO Patient (Name, Age, Gender, BloodTypeID) VALUES (%s, %s, %s, %s) RETURNING PatientID;"
    cursor.execute(patient_insert_stmt, (name, age, gender, bloodtype_id))
    patient_id = cursor.fetchone()[0]

    # Insert data into InsuranceProvider (if provided)
    insurance_number = input("Enter Insurance Number: ") or None
    insurance_insert_stmt = "INSERT INTO InsuranceProvider (PatientID, InsuranceNumber, InsuranceProviderName) VALUES (%s, %s, %s)"
    cursor.execute(insurance_insert_stmt, (patient_id, insurance_number, insurance_provider))

    # Insert data into Test table
    test_name = input("Enter Test Name: ") or None
    test_insert_stmt = "INSERT INTO Test (TestName) VALUES (%s) RETURNING TestID;"
    cursor.execute(test_insert_stmt, (test_name,))
    test_id = cursor.fetchone()[0]

    # Insert data into Hospital table
    hospital_insert_stmt = "INSERT INTO Hospital (HospitalName) VALUES (%s) RETURNING HospitalID;"
    cursor.execute(hospital_insert_stmt, (hospital,))
    hospital_id = cursor.fetchone()[0]

    # Insert data into Room table
    room_insert_stmt = "INSERT INTO Room (HospitalID, RoomNumber) VALUES (%s, %s)"
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
    admission_insert_stmt = "INSERT INTO Admission (PatientID, DoctorID, HospitalID, MedicationID, AdmissionDate, DischargeDate VALUES (%s, %s, %s, %s, %s, %s) RETURNING AdmissionID;"
    cursor.execute(admission_insert_stmt, (patient_id, doctor_id, hospital_id, medication_id, admission_date, discharge_date))
    admission_id = cursor.fetchone()[0]

    # Insert data into AdmissionType table
    admission_type_insert_stmt = "INSERT INTO AdmissionType (AdmissionID, AdmissionType) VALUES (%s, %s)"
    cursor.execute(admission_type_insert_stmt, (admission_id, admission_type))
















def handle_choice(choice, connection):
    """Executes the selected functionality based on user choice."""

    if choice == '1':
        print("Insert Data functionality:\n")
        insert_data(connection)
    elif choice == '2':
        print("Delete Data functionality")
    elif choice == '3':
        print("Update Data functionality")
    elif choice == '4':
        print("Search Data functionality")
    elif choice == '5':
        print("Aggregate Functions functionality")
    elif choice == '6':
        print("Sorting functionality")
    elif choice == '7':
        print("Joins functionality")
    elif choice == '8':
        print("Grouping functionality")
    elif choice == '9':
        print("Subqueries functionality")
    elif choice == '10':
        print("Transactions functionality")
    elif choice == '11':
        print("Error Handling functionality")
    elif choice == '12':
        print("Exiting the system...")
    else:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    connection = connect_to_db()
    if connection:
        while True:
            choice = main_menu()
            handle_choice(choice, connection)
            if choice == '12':
                break
        close_connection(connection)
    else:
        print("Connection failed. Terminating program.")


cursor = connection.cursor()

query = "SELECT * FROM Patient"

results = cursor.execute(query).fetchall()
print(results)
