# Hospital Management System CLI Documentation

## Table of Contents
- [A. Introduction](#a-introduction)
- [B. Getting Started](#b-getting-started)
- [C. Main Menu Options](#c-main-menu-options)
  - [1. Insert a new patient](#1-insert-a-new-patient)
  - [2. Delete the expired insurance on file for a patient](#2-delete-the-expired-insurance-on-file-for-a-patient)
  - [3. Update the billing amount for a patient](#3-update-the-billing-amount-for-a-patient)
  - [4. Search for patients by the doctor assigned to them](#4-search-for-patients-by-the-doctor-assigned-to-them)
  - [5. Aggregate Functions on Patient table](#5-aggregate-functions-on-patient-table)
  - [6. Sort patients by age in descending order](#6-sort-patients-by-age-in-descending-order)
  - [7. Joins Patients and Admission tables for emergency admissions with O- blood type](#7-joins-patients-and-admission-tables-for-emergency-admissions-with-o--blood-type)
  - [8. Group patients based on user-specified columns](#8-group-patients-based-on-user-specified-columns)
  - [9. Find patients with a length of stay exceeding a threshold using a subquery](#9-find-patients-with-a-length-of-stay-exceeding-a-threshold-using-a-subquery)
  - [10. Discharge a patient using a transaction](#10-discharge-a-patient-using-a-transaction)
  - [11. Bonus: Custom Query](#11-bonus-custom-query)
  - [12. Error Handling](#12-error-handling)
  - [13. Exit](#13-exit)
- [D. Conclusion](#d-conclusion)



## A. Introduction
The Hospital Management System CLI is a Python-based interface for interacting with a PostgreSQL database. It allows users to perform various operations related to patient management, including adding new patients, updating billing information, searching for patients by doctor, and more.

***

## B. Getting Started

### Prerequisites:
- Python 3.x ([Download Python](https://www.python.org/downloads/))
- PostgreSQL database server ([Download PostgreSQL](https://www.postgresql.org/download/))
- psycopg2 library (installation using `pip install psycopg2`)

### 1. Clone the Repository:
- Sign up for a free GitHub account at [GitHub](https://github.com) if you don't have one already.
- Once logged in, navigate to the repository containing the hospital management system code.
- Click on the green "Clone or download" button and select "Clone with HTTPS".
- Use the provided URL to clone the repository to your local machine using a Git client or the command line:
   `git clone https://github.com/harshitjain17/Database-Management-Systems-CMPSC-431W-Final-Project.git`

### 2. Database Script:
- Locate the file named `project.sql` within the repository. This file contains the SQL statements to create the database schema.
- Open the `project.sql` file in a text editor and use those commands in PostgreSQL to create the tables.
- Run the following command to execute the project.sql script and create the database schema in your newly created database:
   `psql -U <your_username> -d <your_database_name> < project.sql`

### 3. Start Using the CLI:
- To start the CLI, run the `main.py` script in your terminal using the following command: `python main.py`
- Refer to the Section C for detailed instructions on using the CLI interface functionalities.
***

## C. Main Menu Options

### 1. Insert a new patient
   This option allows users to insert information for a new patient into the database.

   <u>Usage:</u>
   - Choose option 1 from the main menu.
   - Follow the prompts to enter the required information for the new patient, such as name, age, gender, etc.
   - Press Enter for optional fields or provide the requested information.

   <u>Interpretation of Query Output:</u>
   Upon successful insertion, the CLI will display the patient ID and admission ID of the newly inserted patient.

### 2. Delete the expired insurance on file for a patient
   This option allows users to delete the expired insurance information for a specific patient.

   <u>Usage:</u>
   - Choose option 2 from the main menu.
   - Enter the patient ID for which you want to delete the expired insurance.
   - Press Enter to execute the deletion.

   <u>Interpretation of Query Output:</u>
   The CLI will confirm the deletion of the expired insurance provider for the specified patient.

### 3. Update the billing amount for a patient
   This option allows users to update the billing amount for a patient's admission.

   <u>Usage:</u>
   - Choose option 3 from the main menu.
   - Enter the admission ID for which you want to update the billing amount.
   - Enter the new billing amount.
   - Press Enter to execute the update.

   <u>Interpretation of Query Output:</u>
   The CLI will confirm the successful update of the billing amount for the specified admission.

### 4. Search for patients by the doctor assigned to them
   This option allows users to search for patients based on the doctor assigned to them.

   <u>Usage:</u>
   - Choose option 4 from the main menu.
   - Enter the full name of the doctor.
   - Press Enter to execute the search.

   <u>Interpretation of Query Output:</u>
   The CLI will display the patient ID, name, admission ID, doctor name, admission date, and discharge date for each patient found.

### 5. Aggregate Functions on Patient table
   This option provides various aggregate functions on the patient table, such as counting total patients and finding the average age of patients.

   <u>Usage:</u>
   - Choose option 5 from the main menu.
   - Select the desired option from the sub-menu.
   - Press Enter to execute the chosen aggregate function.

   <u>Interpretation of Query Output:</u>
   The CLI displays the result of the chosen aggregate function, such as total patients or average patient age.

### 6. Sort patients by age in descending order
   This option allows users to sort patients by age in descending order.

   <u>Usage:</u>
   - Choose option 6 from the main menu.
   - The CLI will display the sorted list of patients along with their details.

   <u>Interpretation of Query Output:</u>
   The CLI displays the sorted list of patients with details including name, age, gender, etc., arranged in descending order of age.

### 7. Joins Patients and Admission tables for emergency admissions with O- blood type
   This option joins the Patients and Admission tables to find emergency admissions with O- blood type.

   <u>Usage:</u>
   - Choose option 7 from the main menu.
   - The CLI will display emergency admissions with patients having O- blood type along with their details.

   <u>Interpretation of Query Output:</u>
   The CLI will display emergency admissions with details including patient name, blood type, admission date, and admission type.

### 8. Group patients based on user-specified columns
   This option allows users to group patients based on user-specified columns and find the average age of each group.

   <u>Usage:</u>
   - Choose option 8 from the main menu.
   - Enter the column name to group by.
   - The CLI will display the average age of patients in each group.

   <u>Interpretation of Query Output:</u>
   The CLI will display the average age of patients in each group along with the specified column.

### 9. Find patients with a length of stay exceeding a threshold using a subquery
   This option finds patients with a length of stay exceeding a user-specified threshold using a subquery.

   <u>Usage:</u>
   - Choose option 9 from the main menu.
   - Enter the minimum threshold for length of stay in days.
   - The CLI will display patients with a length of stay exceeding the specified threshold.

   <u>Interpretation of Query Output:</u>
   The CLI will display patients with details including patient ID, name, admission date, discharge date, and length of stay.
   
### 10. Discharge a patient using a transaction
   This option allows users to discharge a patient using a transaction.

   <u>Usage:</u>
   - Choose option 10 from the main menu.
   - Enter the patient ID of the patient to be discharged.
   - The CLI will confirm the successful discharge of the patient.

   <u>Interpretation of Query Output:</u>
   The CLI will confirm the successful discharge of the patient.

### 11. Bonus: Custom Query
   This option allows users to execute custom SQL queries on the database.

   <u>Usage:</u>
   - Choose option 11 from the main menu.
   - Enter the desired SQL query when prompted.
   - The CLI will execute the query and display the results, if any.

   <u>Interpretation of Query Output:</u>
   The CLI will display the query results if applicable.

### 12. Error Handling
   Error handling is performed throughout the CLI to handle various exceptions and provide informative error messages.

### 13. Exit
   This option exits the CLI and closes the database connection.

***

## D. Conclusion

The Hospital Management System CLI provides a convenient interface for managing patient data in a PostgreSQL database. With a range of functionalities available through simple CLI commands, users can efficiently perform operations such as patient insertion, update, search, and more. For any queries or issues, refer to the documentation or contact the system administrator.