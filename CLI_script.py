import psycopg2 as db_connect
import pandas as pd
import datetime

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
    print("9. Finds patients who have been admitted more than once using a subquery")
    print("10. Discharges a patient using a transaction")
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


def insert_new_patient(connection):
    """Prompts user for data and inserts it into all 14 relations."""

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
    hospital_check_stmt = "SELECT HospitalID FROM Hospital WHERE HospitalName = %s;"
    cursor.execute(hospital_check_stmt, (hospital,))
    existing_hospital_id = cursor.fetchone()
    if existing_hospital_id:
        hospital_id = existing_hospital_id[0]
    else:
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
    patient_id = int(input("Enter the Patient ID: "))
    delete_stmt = f"DELETE FROM InsuranceProvider WHERE PatientID = {patient_id}"

    try:
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
    admission_id = int(input("Enter the Admission ID: "))
    new_billing_amount = float(input("Enter the new Billing Amount: "))
    update_stmt = f"UPDATE Billing SET BillingAmount = {new_billing_amount} WHERE AdmissionID = {admission_id}"

    try:
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
    choice = input("Enter your choice (1-2): ")
    
    try:
        if choice == '1':
            cursor.execute("SELECT COUNT(*) FROM Patient;")
            count = cursor.fetchone()[0]
            print("Total Patients:", count)
        
        elif choice == '2':
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
        print("\nPatients Sorted by Age (Descending):")
        for patient in patients:
            print(f"Patient ID: {patient[0]}, Name: {patient[1]}, Age: {patient[2]}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()


def join_patients_emergency_o_neg(connection):
    """Joins Patients and Admission tables for emergency admissions with O- blood type."""

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT P.Name, A.AdmissionDate
        FROM Patient P
        INNER JOIN Admission A ON P.PatientID = A.PatientID
        INNER JOIN AdmissionType AT ON A.AdmissionID = AT.AdmissionID
        INNER JOIN BloodGroup BG ON P.BloodTypeID = BG.BloodTypeID
        WHERE AT.AdmissionType = 'Emergency' AND BG.BloodType = 'O-';
        """)
        admissions = cursor.fetchall()
        cursor.close()

        if admissions:
            print("\nEmergency Admissions with Patients having Blood Type O-:")
            for admission in admissions:
                print(f"Patient Name: {admission[0]}, Admission Date: {admission[1]}")
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
        column1 = input("Enter the first column to group by: ")
        column2 = input("Enter the second column to group by (optional): ")
        query = f"SELECT {column1}"
        if column2:
            query += f", {column2}"
        query += " FROM Patient GROUP BY " + query.split("SELECT ")[-1]
        cursor.execute(query)
        data = cursor.fetchall()

        if data:
            df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
            print("\nGrouping results:")
            if column2:
                grouped_data = df.groupby([column1, column2]).size().unstack()
                print(grouped_data)
            else:
                grouped_data = df.groupby(column1).size()
                print(grouped_data)
        else:
            print("No data found in Patients table.")
    
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        data = []

    finally:
        cursor.close()


def find_readmitted_patients(connection):
    """Finds patients who have been admitted more than once using a subquery."""

    cursor = connection.cursor()

    try:
        subquery = "SELECT PatientID FROM Admission GROUP BY PatientID HAVING COUNT(*) > 1"
        query = f"SELECT * FROM Patient WHERE PatientID IN ({subquery});"
        cursor.execute(query)
        data = cursor.fetchall()

        if data:
            print("\nPatients who have been readmitted:")
            df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
            print(df.to_string(index=False))
        else:
            print("No patients found who have been readmitted.")

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
        update_admission_stmt = f"UPDATE Admission SET DischargeDate = {discharge_date} WHERE AdmissionID = {active_admission[0]};"
        cursor.execute(update_admission_stmt)

        # All updates successful, commit the transaction
        connection.commit()
        print(f"Patient ID {patient_id} discharged successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        print("Transaction rolled back. Patient not discharged.")

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
        find_readmitted_patients(connection)
    elif choice == 10:
        discharge_patient_transaction(connection)
    elif choice == 11:
        print("Error handling performed for all functions.")
    elif choice == 12:
        print("Exiting the system...")
    else:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    connection = connect_to_db()
    if connection:
        while True:
            choice = main_menu()
            handle_choice(choice, connection)
            if (choice == 12):
                break
        close_connection(connection)
    else:
        print("Connection failed. Terminating program.")