"""Create and seed the MediOps SQLite hospital database.

Run: python generator.py
The generator is safe to rerun: it rebuilds the database from scratch.
"""
from __future__ import annotations

import argparse
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).with_name("mediops.db")
RNG = random.Random(42)

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL UNIQUE,
    bed_capacity INTEGER NOT NULL CHECK (bed_capacity > 0)
);

CREATE TABLE IF NOT EXISTS cities (
    city_id INTEGER PRIMARY KEY,
    city_name TEXT NOT NULL UNIQUE,
    region TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL CHECK (gender IN ('Female','Male','Other')),
    city_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

CREATE TABLE IF NOT EXISTS admissions (
    admission_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    admission_date TEXT NOT NULL,
    discharge_date TEXT,
    admission_type TEXT NOT NULL,
    admission_source TEXT NOT NULL,
    length_of_stay INTEGER NOT NULL,
    outcome TEXT NOT NULL DEFAULT 'Admitted',
    attending_physician TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE IF NOT EXISTS diagnoses (
    diagnosis_id INTEGER PRIMARY KEY,
    admission_id INTEGER NOT NULL,
    diagnosis_code TEXT NOT NULL,
    diagnosis_name TEXT NOT NULL,
    diagnosis_type TEXT NOT NULL,
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

CREATE TABLE IF NOT EXISTS lab_results (
    lab_id INTEGER PRIMARY KEY,
    admission_id INTEGER NOT NULL,
    test_name TEXT NOT NULL,
    result_value REAL NOT NULL,
    unit TEXT NOT NULL,
    reference_low REAL NOT NULL,
    reference_high REAL NOT NULL,
    result_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

CREATE TABLE IF NOT EXISTS medications (
    medication_id INTEGER PRIMARY KEY,
    admission_id INTEGER NOT NULL,
    medication_name TEXT NOT NULL,
    dose TEXT NOT NULL,
    route TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

CREATE TABLE IF NOT EXISTS procedures (
    procedure_id INTEGER PRIMARY KEY,
    admission_id INTEGER NOT NULL,
    procedure_name TEXT NOT NULL,
    procedure_category TEXT NOT NULL,
    procedure_date TEXT NOT NULL,
    procedure_cost REAL NOT NULL,
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

CREATE TABLE IF NOT EXISTS billing (
    bill_id INTEGER PRIMARY KEY,
    admission_id INTEGER NOT NULL UNIQUE,
    payer_type TEXT NOT NULL,
    billed_amount REAL NOT NULL,
    collected_amount REAL NOT NULL,
    bill_date TEXT NOT NULL,
    payment_status TEXT NOT NULL,
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

CREATE TABLE IF NOT EXISTS sim_clock (
    clock_id INTEGER PRIMARY KEY CHECK (clock_id = 1),
    hospital_time TEXT NOT NULL,
    last_tick TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_admissions_date ON admissions(admission_date);
CREATE INDEX IF NOT EXISTS idx_admissions_department ON admissions(department_id);
CREATE INDEX IF NOT EXISTS idx_admissions_active ON admissions(discharge_date);
CREATE INDEX IF NOT EXISTS idx_labs_status ON lab_results(status);
CREATE INDEX IF NOT EXISTS idx_billing_payer ON billing(payer_type);
"""

DEPARTMENTS = [
    ("Emergency", 35), ("Cardiology", 28), ("Neurology", 22),
    ("Orthopedics", 30), ("General Medicine", 40), ("ICU", 18),
    ("Pediatrics", 24), ("Surgery", 26),
]
CITIES = [
    ("Brahmapur", "Odisha"), ("Bhubaneswar", "Odisha"),
    ("Cuttack", "Odisha"), ("Visakhapatnam", "Andhra Pradesh"),
    ("Kolkata", "West Bengal"), ("Ranchi", "Jharkhand"),
    ("Raipur", "Chhattisgarh"), ("Hyderabad", "Telangana"),
]
FIRST_NAMES = ["Aarav","Vivaan","Aditya","Ishita","Ananya","Diya","Rohan","Meera",
               "Kabir","Saanvi","Arjun","Priya","Aisha","Rahul","Neha","Ishan"]
LAST_NAMES = ["Sharma","Patel","Das","Reddy","Mohanty","Singh","Kumar","Rao",
              "Mishra","Nair","Jena","Gupta"]
PHYSICIANS = ["Dr. A. Sharma","Dr. R. Das","Dr. P. Mohanty","Dr. S. Rao",
              "Dr. M. Singh","Dr. N. Patel","Dr. K. Reddy"]
DIAGNOSES = [
    ("I10","Essential hypertension","Chronic"),
    ("J18.9","Pneumonia, unspecified","Primary"),
    ("E11.9","Type 2 diabetes mellitus","Chronic"),
    ("I21.9","Acute myocardial infarction","Primary"),
    ("S72.0","Fracture of neck of femur","Primary"),
    ("G40.9","Epilepsy, unspecified","Primary"),
    ("N39.0","Urinary tract infection","Primary"),
    ("K35.8","Acute appendicitis","Primary"),
    ("J45.9","Asthma, unspecified","Chronic"),
    ("A09","Gastroenteritis","Primary"),
]
LABS = [
    ("Hemoglobin", 13.5, 12.0, 16.0, "g/dL"),
    ("WBC", 8.0, 4.0, 11.0, "10^3/uL"),
    ("Creatinine", 1.0, 0.6, 1.2, "mg/dL"),
    ("Sodium", 140.0, 135.0, 145.0, "mmol/L"),
    ("Potassium", 4.2, 3.5, 5.1, "mmol/L"),
    ("Glucose", 105.0, 70.0, 140.0, "mg/dL"),
]
MEDICATIONS = ["Paracetamol","Amoxicillin","Metformin","Amlodipine","Atorvastatin",
               "Ceftriaxone","Salbutamol","Pantoprazole","Insulin"]
PROCEDURES = [
    ("ECG","Diagnostics",450), ("X-Ray","Imaging",900),
    ("CT Scan","Imaging",4500), ("MRI","Imaging",8500),
    ("Blood Panel","Laboratory",1200), ("Ultrasound","Imaging",1800),
    ("Minor Surgery","Surgery",12000), ("Angiography","Cardiology",28000),
]
PAYER_TYPES = ["Private Insurance","Government Scheme","Self Pay","Corporate"]

def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    con = sqlite3.connect(db_path, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    con.execute("PRAGMA journal_mode = WAL")
    return con

def initialize(con: sqlite3.Connection) -> None:
    con.executescript(SCHEMA)
    con.executemany("INSERT OR IGNORE INTO departments(department_name,bed_capacity) VALUES (?,?)", DEPARTMENTS)
    con.executemany("INSERT OR IGNORE INTO cities(city_name,region) VALUES (?,?)", CITIES)
    con.commit()

def lab_status(value: float, low: float, high: float) -> str:
    if low <= value <= high:
        return "Normal"
    width = high - low
    if value < low - 0.5 * width or value > high + 0.5 * width:
        return "Critical"
    return "Abnormal"

def create_patient(con: sqlite3.Connection, when: datetime) -> int:
    city_id = RNG.randint(1, len(CITIES))
    dob = when - timedelta(days=RNG.randint(18 * 365, 90 * 365))
    cur = con.execute(
        """INSERT INTO patients(first_name,last_name,date_of_birth,gender,city_id,created_at)
           VALUES (?,?,?,?,?,?)""",
        (RNG.choice(FIRST_NAMES), RNG.choice(LAST_NAMES), dob.date().isoformat(),
         RNG.choice(["Female","Male","Other"]), city_id, when.isoformat(timespec="seconds"))
    )
    return int(cur.lastrowid)

def create_admission(con: sqlite3.Connection, when: datetime, patient_id: int | None = None,
                     force_active: bool = False) -> int:
    """Insert one admission and its related clinical/financial records."""
    if patient_id is None:
        patient_id = create_patient(con, when)
    dept_id = RNG.randint(1, len(DEPARTMENTS))
    planned_los = RNG.randint(1, 12)
    active = force_active or RNG.random() < 0.12
    discharge = None if active else when + timedelta(days=planned_los, hours=RNG.randint(0, 18))
    outcome = "Admitted" if active else RNG.choices(
        ["Discharged","Transferred","Expired"], weights=[94,5,1], k=1
    )[0]
    cur = con.execute(
        """INSERT INTO admissions(patient_id,department_id,admission_date,discharge_date,
           admission_type,admission_source,length_of_stay,outcome,attending_physician)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (patient_id, dept_id, when.isoformat(timespec="seconds"),
         discharge.isoformat(timespec="seconds") if discharge else None,
         RNG.choice(["Emergency","Elective","Urgent"]),
         RNG.choice(["Emergency Room","Clinic","Referral","Transfer"]),
         planned_los, outcome, RNG.choice(PHYSICIANS))
    )
    admission_id = int(cur.lastrowid)

    chosen = RNG.sample(DIAGNOSES, k=RNG.randint(1, 3))
    for idx, (code, name, dtype) in enumerate(chosen):
        con.execute("""INSERT INTO diagnoses(admission_id,diagnosis_code,diagnosis_name,diagnosis_type)
                       VALUES (?,?,?,?)""", (admission_id, code, name, "Primary" if idx == 0 else dtype))

    lab_count = RNG.randint(2, 5)
    for _ in range(lab_count):
        name, base, low, high, unit = RNG.choice(LABS)
        value = max(0.1, RNG.gauss(base, (high-low) * 0.48))
        lab_date = when + timedelta(hours=RNG.randint(1, 48))
        con.execute("""INSERT INTO lab_results(admission_id,test_name,result_value,unit,
                       reference_low,reference_high,result_date,status) VALUES (?,?,?,?,?,?,?,?)""",
                    (admission_id, name, round(value, 2), unit, low, high,
                     lab_date.isoformat(timespec="seconds"), lab_status(value, low, high)))

    for _ in range(RNG.randint(1, 4)):
        start = when + timedelta(hours=RNG.randint(1, 24))
        con.execute("""INSERT INTO medications(admission_id,medication_name,dose,route,start_date,end_date)
                       VALUES (?,?,?,?,?,?)""",
                    (admission_id, RNG.choice(MEDICATIONS), RNG.choice(["250 mg","500 mg","1 g","10 mg"]),
                     RNG.choice(["Oral","IV","Injection","Inhalation"]),
                     start.isoformat(timespec="seconds"),
                     (start + timedelta(days=planned_los)).isoformat(timespec="seconds") if not active else None))

    procedure_total = 0.0
    for _ in range(RNG.randint(0, 3)):
        pname, category, cost = RNG.choice(PROCEDURES)
        cost = cost * RNG.uniform(0.85, 1.25)
        procedure_total += cost
        proc_date = when + timedelta(hours=RNG.randint(2, 72))
        con.execute("""INSERT INTO procedures(admission_id,procedure_name,procedure_category,
                       procedure_date,procedure_cost) VALUES (?,?,?,?,?)""",
                    (admission_id, pname, category, proc_date.isoformat(timespec="seconds"), round(cost, 2)))

    base_bill = RNG.uniform(8000, 65000) + procedure_total
    billed = round(base_bill, 2)
    collected = round(billed * RNG.uniform(0.55, 1.0), 2) if not active else 0.0
    payer = RNG.choice(PAYER_TYPES)
    bill_date = (discharge or when).isoformat(timespec="seconds")
    con.execute("""INSERT INTO billing(admission_id,payer_type,billed_amount,collected_amount,
                   bill_date,payment_status) VALUES (?,?,?,?,?,?)""",
                (admission_id, payer, billed, collected, bill_date,
                 "Pending" if active else ("Paid" if collected >= billed * 0.95 else "Partial")))
    return admission_id

def seed(days: int = 180, patients: int = 520, db_path: Path = DB_PATH) -> None:
    if db_path.exists():
        db_path.unlink()
    # Remove stale WAL sidecars when rebuilding.
    for suffix in ("-wal", "-shm"):
        sidecar = Path(str(db_path) + suffix)
        if sidecar.exists():
            sidecar.unlink()
    con = connect(db_path)
    initialize(con)
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    start = now - timedelta(days=days)
    try:
        for i in range(patients):
            admission_time = start + timedelta(hours=RNG.randint(0, days * 24 - 1))
            create_admission(con, admission_time)
            if (i + 1) % 100 == 0:
                con.commit()
        # Ensure there is a useful current inpatient population.
        for _ in range(35):
            create_admission(con, now - timedelta(hours=RNG.randint(1, 72)), force_active=True)
        con.execute("""INSERT OR REPLACE INTO sim_clock(clock_id,hospital_time,last_tick)
                       VALUES (1,?,?)""", (now.isoformat(timespec="seconds"), now.isoformat(timespec="seconds")))
        con.commit()
    finally:
        con.close()
    print(f"Created {db_path} with {patients + 35} admissions across approximately {days} days.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the MediOps synthetic hospital database.")
    parser.add_argument("--days", type=int, default=180, help="History window in days (default: 180)")
    parser.add_argument("--patients", type=int, default=520, help="Historical admissions to generate")
    args = parser.parse_args()
    seed(args.days, args.patients)
