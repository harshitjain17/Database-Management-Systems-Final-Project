CREATE TABLE Patient (
    PatientID SERIAL PRIMARY KEY,
    BloodTypeID INTEGER REFERENCES BloodGroup(BloodTypeID),
    Name VARCHAR(50),
    Age INTEGER,
    Gender VARCHAR(10)
);

CREATE TABLE BloodGroup (
    BloodTypeID SERIAL PRIMARY KEY,
    BloodType VARCHAR(5) UNIQUE
);

CREATE TABLE InsuranceProvider (
    InsuranceProviderID SERIAL PRIMARY KEY,
    PatientID INTEGER REFERENCES Patient(PatientID),
    InsuranceProviderName VARCHAR(50)
);

CREATE TABLE Admission (
    AdmissionID SERIAL PRIMARY KEY,
    PatientID INTEGER REFERENCES Patient(PatientID),
    DoctorID INTEGER REFERENCES Doctor(DoctorID),
    HospitalID INTEGER REFERENCES Hospital(HospitalID),
    MedicationID INTEGER REFERENCES Medication(MedicationID),
    AdmissionDate DATE,
    DischargeDate DATE
);

CREATE TABLE AdmissionType (
    AdmissionTypeID SERIAL PRIMARY KEY,
    AdmissionID INTEGER REFERENCES Admission(AdmissionID),
    AdmissionType VARCHAR(20)
);

CREATE TABLE Billing (
    BillingID SERIAL PRIMARY KEY,
    AdmissionID INTEGER REFERENCES Admission(AdmissionID),
    BillingAmount DECIMAL(10,2)
);

CREATE TABLE TestResult (
    AdmissionID INTEGER REFERENCES Admission(AdmissionID),
    TestResults TEXT,
    PRIMARY KEY (AdmissionID)
);

CREATE TABLE Hospital (
    HospitalID SERIAL PRIMARY KEY,
    HospitalName VARCHAR(50) NOT NULL
);

CREATE TABLE Room (
    RoomID SERIAL PRIMARY KEY,
    HospitalID INTEGER REFERENCES Hospital(HospitalID),
    RoomNumber INTEGER
);

CREATE TABLE Doctor (
    DoctorID SERIAL PRIMARY KEY,
    HospitalID INTEGER REFERENCES Hospital(HospitalID),
    DoctorName VARCHAR(50) NOT NULL
);

CREATE TABLE Medication (
    MedicationID SERIAL PRIMARY KEY,
    DiagnosisID INTEGER REFERENCES Diagnosis(DiagnosisID),
    MedicineName VARCHAR(50) NOT NULL
);

CREATE TABLE Diagnosis (
    DiagnosisID SERIAL PRIMARY KEY,
    MedicalCondition VARCHAR(100) NOT NULL
);

CREATE TABLE DiagAdm (
    AdmissionID INTEGER REFERENCES Admission(AdmissionID),
    AdmissionID INTEGER REFERENCES Diagnosis(DiagnosisID),
    PRIMARY KEY (AdmissionID, DiagnosisID)
);
