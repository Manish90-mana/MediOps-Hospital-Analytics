# MediOps – Hospital Operations Analytics Platform

MediOps is a hospital operations analytics project built using Python, SQL, SQLite, and Streamlit. It focuses on analyzing hospital data, monitoring patient admissions, tracking bed occupancy, and understanding clinical and financial performance through an interactive dashboard.

The project includes synthetic hospital data generation, a live data simulator, database management, and interactive visualizations.

## Project Overview

Hospitals generate large amounts of data every day. Managing patient admissions, bed availability, laboratory results, discharge records, and billing information is important for maintaining efficient hospital operations.

MediOps brings this information together in one platform to help analyze hospital performance and understand operational patterns.

The main objectives of this project are:

- Monitor hospital admissions and discharges.
- Track bed occupancy across departments.
- Analyze patient flow and hospital capacity.
- Monitor laboratory test results.
- Explore hospital revenue and billing information.
- Visualize clinical and operational trends.
- Simulate hospital activity using Python.

## Dashboard Modules

### 1. Live Hospital Operations

- Total admissions and active patients.
- Current bed occupancy.
- Department-wise capacity utilization.
- Patient admission and discharge trends.
- Critical laboratory alerts.
- Latest admission activity.

### 2. Patient Flow Analytics

- Daily admission trends.
- Department-wise patient distribution.
- Average length of stay.
- Patient demographic analysis.
- Admission and discharge patterns.

### 3. Financial Analytics

- Total hospital billing.
- Revenue collected.
- Outstanding payments.
- Insurance and self-pay distribution.
- Procedure-wise cost analysis.

### 4. Clinical Analytics

- Laboratory test status.
- Diagnosis frequency.
- Medication prescription analysis.
- Patient readmission rate.

### 5. Data Explorer

- Browse database tables.
- Inspect hospital records.
- Explore individual datasets.
- Export data as CSV files.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and data generation |
| SQLite | Relational database management |
| SQL | Data retrieval and analysis |
| Pandas | Data manipulation and processing |
| Streamlit | Interactive dashboard development |
| Plotly | Charts and data visualization |

## System Architecture

```text
Synthetic Hospital Data
          |
          v
Python Data Generator
          |
          v
SQLite Database
          |
          +-------------------+
          |                   |
          v                   v
   Python Simulator      SQL Queries
          |                   |
          v                   v
   Live Data Updates    Pandas Processing
          |                   |
          +---------+---------+
                    |
                    v
             Streamlit App
                    |
                    v
          Interactive Dashboard
                    |
          +---------+---------+
          |         |         |
          v         v         v
        Live      Clinical  Financial
        Ops       Analytics Analytics
```

## Project Structure

```text
MediOps/
│
├── app.py
├── generator.py
├── simulator.py
├── requirements.txt
├── README.md
├── .gitignore
└── mediops.db
```

### File Descriptions

| File | Description |
|---|---|
| `app.py` | Main Streamlit dashboard and analytics interface |
| `generator.py` | Creates the database and generates synthetic hospital records |
| `simulator.py` | Simulates hospital activity, including patient admissions and discharges |
| `requirements.txt` | Contains the required Python libraries |
| `mediops.db` | SQLite database containing synthetic hospital data |
| `.gitignore` | Specifies files excluded from Git |

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/MediOps-Hospital-Analytics.git
cd MediOps-Hospital-Analytics
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Generate the Database

```bash
python generator.py
```

This creates the SQLite database and populates it with synthetic hospital records.

### 6. Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your default browser.

### 7. Start the Live Simulator

Open another terminal in the project directory, activate the virtual environment, and run:

```bash
python simulator.py
```

The simulator periodically generates new hospital activity and updates the database.

To stop the simulator, press `Ctrl + C`.

## Database Design

MediOps uses SQLite to store and manage hospital information in a relational database.

The database contains the following tables:

| Table | Description |
|---|---|
| `departments` | Hospital departments and their bed capacity |
| `cities` | City reference information |
| `patients` | Patient demographic information |
| `admissions` | Patient admission and discharge records |
| `diagnoses` | Patient diagnosis information |
| `lab_results` | Laboratory test records and results |
| `medications` | Medication prescriptions |
| `procedures` | Medical procedure information |
| `billing` | Patient billing and payment records |
| `sim_clock` | Simulated hospital time |

The database uses primary keys, foreign keys, constraints, and indexes to maintain data consistency and support efficient queries.

## Key Features

- Synthetic hospital dataset generation.
- Relational database design using SQLite.
- Automated patient admission and discharge simulation.
- Interactive hospital operations dashboard.
- Department-wise bed occupancy monitoring.
- Patient flow and demographic analysis.
- Clinical and laboratory data analysis.
- Financial and billing analytics.
- Interactive charts and visualizations.
- CSV data export.

## Learning Outcomes

Through this project, I am exploring and implementing:

- Python programming and application development.
- Relational database design and normalization.
- SQL queries and analytical operations.
- Synthetic data generation.
- Data cleaning and transformation using Pandas.
- Real-time-style data simulation.
- Interactive dashboard development using Streamlit.
- Data visualization using Plotly.
- Healthcare KPI analysis.
- End-to-end project development.

## Future Enhancements

The project can be extended with additional features, including:

- Hospital admission forecasting using machine learning.
- Bed occupancy and demand prediction.
- Emergency department waiting-time prediction.
- Patient readmission risk prediction.
- Automated operational alerts.
- Advanced department performance analysis.
- Cloud deployment.

## Disclaimer

This project uses synthetic hospital data and is developed for educational, analytical, and portfolio purposes. It does not use real patient records and is not intended for clinical diagnosis, treatment recommendations, or actual hospital decision-making.

## Author

**Your Name**

GitHub: # MediOps – Hospital Operations Analytics Platform

MediOps is a hospital operations analytics project built using Python, SQL, SQLite, and Streamlit. It focuses on analyzing hospital data, monitoring patient admissions, tracking bed occupancy, and understanding clinical and financial performance through an interactive dashboard.

The project includes synthetic hospital data generation, a live data simulator, database management, and interactive visualizations.

## Project Overview

Hospitals generate large amounts of data every day. Managing patient admissions, bed availability, laboratory results, discharge records, and billing information is important for maintaining efficient hospital operations.

MediOps brings this information together in one platform to help analyze hospital performance and understand operational patterns.

The main objectives of this project are:

- Monitor hospital admissions and discharges.
- Track bed occupancy across departments.
- Analyze patient flow and hospital capacity.
- Monitor laboratory test results.
- Explore hospital revenue and billing information.
- Visualize clinical and operational trends.
- Simulate hospital activity using Python.

## Dashboard Modules

### 1. Live Hospital Operations

- Total admissions and active patients.
- Current bed occupancy.
- Department-wise capacity utilization.
- Patient admission and discharge trends.
- Critical laboratory alerts.
- Latest admission activity.

### 2. Patient Flow Analytics

- Daily admission trends.
- Department-wise patient distribution.
- Average length of stay.
- Patient demographic analysis.
- Admission and discharge patterns.

### 3. Financial Analytics

- Total hospital billing.
- Revenue collected.
- Outstanding payments.
- Insurance and self-pay distribution.
- Procedure-wise cost analysis.

### 4. Clinical Analytics

- Laboratory test status.
- Diagnosis frequency.
- Medication prescription analysis.
- Patient readmission rate.

### 5. Data Explorer

- Browse database tables.
- Inspect hospital records.
- Explore individual datasets.
- Export data as CSV files.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and data generation |
| SQLite | Relational database management |
| SQL | Data retrieval and analysis |
| Pandas | Data manipulation and processing |
| Streamlit | Interactive dashboard development |
| Plotly | Charts and data visualization |

## System Architecture

```text
Synthetic Hospital Data
          |
          v
Python Data Generator
          |
          v
SQLite Database
          |
          +-------------------+
          |                   |
          v                   v
   Python Simulator      SQL Queries
          |                   |
          v                   v
   Live Data Updates    Pandas Processing
          |                   |
          +---------+---------+
                    |
                    v
             Streamlit App
                    |
                    v
          Interactive Dashboard
                    |
          +---------+---------+
          |         |         |
          v         v         v
        Live      Clinical  Financial
        Ops       Analytics Analytics
```

## Project Structure

```text
MediOps/
│
├── app.py
├── generator.py
├── simulator.py
├── requirements.txt
├── README.md
├── .gitignore
└── mediops.db
```

### File Descriptions

| File | Description |
|---|---|
| `app.py` | Main Streamlit dashboard and analytics interface |
| `generator.py` | Creates the database and generates synthetic hospital records |
| `simulator.py` | Simulates hospital activity, including patient admissions and discharges |
| `requirements.txt` | Contains the required Python libraries |
| `mediops.db` | SQLite database containing synthetic hospital data |
| `.gitignore` | Specifies files excluded from Git |

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/MediOps-Hospital-Analytics.git
cd MediOps-Hospital-Analytics
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Generate the Database

```bash
python generator.py
```

This creates the SQLite database and populates it with synthetic hospital records.

### 6. Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your default browser.

### 7. Start the Live Simulator

Open another terminal in the project directory, activate the virtual environment, and run:

```bash
python simulator.py
```

The simulator periodically generates new hospital activity and updates the database.

To stop the simulator, press `Ctrl + C`.

## Database Design

MediOps uses SQLite to store and manage hospital information in a relational database.

The database contains the following tables:

| Table | Description |
|---|---|
| `departments` | Hospital departments and their bed capacity |
| `cities` | City reference information |
| `patients` | Patient demographic information |
| `admissions` | Patient admission and discharge records |
| `diagnoses` | Patient diagnosis information |
| `lab_results` | Laboratory test records and results |
| `medications` | Medication prescriptions |
| `procedures` | Medical procedure information |
| `billing` | Patient billing and payment records |
| `sim_clock` | Simulated hospital time |

The database uses primary keys, foreign keys, constraints, and indexes to maintain data consistency and support efficient queries.

## Key Features

- Synthetic hospital dataset generation.
- Relational database design using SQLite.
- Automated patient admission and discharge simulation.
- Interactive hospital operations dashboard.
- Department-wise bed occupancy monitoring.
- Patient flow and demographic analysis.
- Clinical and laboratory data analysis.
- Financial and billing analytics.
- Interactive charts and visualizations.
- CSV data export.

## Learning Outcomes

Through this project, I am exploring and implementing:

- Python programming and application development.
- Relational database design and normalization.
- SQL queries and analytical operations.
- Synthetic data generation.
- Data cleaning and transformation using Pandas.
- Real-time-style data simulation.
- Interactive dashboard development using Streamlit.
- Data visualization using Plotly.
- Healthcare KPI analysis.
- End-to-end project development.

## Future Enhancements

The project can be extended with additional features, including:

- Hospital admission forecasting using machine learning.
- Bed occupancy and demand prediction.
- Emergency department waiting-time prediction.
- Patient readmission risk prediction.
- Automated operational alerts.
- Advanced department performance analysis.
- Cloud deployment.

## Disclaimer

This project uses synthetic hospital data and is developed for educational, analytical, and portfolio purposes. It does not use real patient records and is not intended for clinical diagnosis, treatment recommendations, or actual hospital decision-making.

## Author

**Your Name**

GitHub: # MediOps – Hospital Operations Analytics Platform

MediOps is a hospital operations analytics project built using Python, SQL, SQLite, and Streamlit. It focuses on analyzing hospital data, monitoring patient admissions, tracking bed occupancy, and understanding clinical and financial performance through an interactive dashboard.

The project includes synthetic hospital data generation, a live data simulator, database management, and interactive visualizations.

## Project Overview

Hospitals generate large amounts of data every day. Managing patient admissions, bed availability, laboratory results, discharge records, and billing information is important for maintaining efficient hospital operations.

MediOps brings this information together in one platform to help analyze hospital performance and understand operational patterns.

The main objectives of this project are:

- Monitor hospital admissions and discharges.
- Track bed occupancy across departments.
- Analyze patient flow and hospital capacity.
- Monitor laboratory test results.
- Explore hospital revenue and billing information.
- Visualize clinical and operational trends.
- Simulate hospital activity using Python.

## Dashboard Modules

### 1. Live Hospital Operations

- Total admissions and active patients.
- Current bed occupancy.
- Department-wise capacity utilization.
- Patient admission and discharge trends.
- Critical laboratory alerts.
- Latest admission activity.

### 2. Patient Flow Analytics

- Daily admission trends.
- Department-wise patient distribution.
- Average length of stay.
- Patient demographic analysis.
- Admission and discharge patterns.

### 3. Financial Analytics

- Total hospital billing.
- Revenue collected.
- Outstanding payments.
- Insurance and self-pay distribution.
- Procedure-wise cost analysis.

### 4. Clinical Analytics

- Laboratory test status.
- Diagnosis frequency.
- Medication prescription analysis.
- Patient readmission rate.

### 5. Data Explorer

- Browse database tables.
- Inspect hospital records.
- Explore individual datasets.
- Export data as CSV files.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and data generation |
| SQLite | Relational database management |
| SQL | Data retrieval and analysis |
| Pandas | Data manipulation and processing |
| Streamlit | Interactive dashboard development |
| Plotly | Charts and data visualization |

## System Architecture

```text
Synthetic Hospital Data
          |
          v
Python Data Generator
          |
          v
SQLite Database
          |
          +-------------------+
          |                   |
          v                   v
   Python Simulator      SQL Queries
          |                   |
          v                   v
   Live Data Updates    Pandas Processing
          |                   |
          +---------+---------+
                    |
                    v
             Streamlit App
                    |
                    v
          Interactive Dashboard
                    |
          +---------+---------+
          |         |         |
          v         v         v
        Live      Clinical  Financial
        Ops       Analytics Analytics
```

## Project Structure

```text
MediOps/
│
├── app.py
├── generator.py
├── simulator.py
├── requirements.txt
├── README.md
├── .gitignore
└── mediops.db
```

### File Descriptions

| File | Description |
|---|---|
| `app.py` | Main Streamlit dashboard and analytics interface |
| `generator.py` | Creates the database and generates synthetic hospital records |
| `simulator.py` | Simulates hospital activity, including patient admissions and discharges |
| `requirements.txt` | Contains the required Python libraries |
| `mediops.db` | SQLite database containing synthetic hospital data |
| `.gitignore` | Specifies files excluded from Git |

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/MediOps-Hospital-Analytics.git
cd MediOps-Hospital-Analytics
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Generate the Database

```bash
python generator.py
```

This creates the SQLite database and populates it with synthetic hospital records.

### 6. Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your default browser.

### 7. Start the Live Simulator

Open another terminal in the project directory, activate the virtual environment, and run:

```bash
python simulator.py
```

The simulator periodically generates new hospital activity and updates the database.

To stop the simulator, press `Ctrl + C`.

## Database Design

MediOps uses SQLite to store and manage hospital information in a relational database.

The database contains the following tables:

| Table | Description |
|---|---|
| `departments` | Hospital departments and their bed capacity |
| `cities` | City reference information |
| `patients` | Patient demographic information |
| `admissions` | Patient admission and discharge records |
| `diagnoses` | Patient diagnosis information |
| `lab_results` | Laboratory test records and results |
| `medications` | Medication prescriptions |
| `procedures` | Medical procedure information |
| `billing` | Patient billing and payment records |
| `sim_clock` | Simulated hospital time |

The database uses primary keys, foreign keys, constraints, and indexes to maintain data consistency and support efficient queries.

## Key Features

- Synthetic hospital dataset generation.
- Relational database design using SQLite.
- Automated patient admission and discharge simulation.
- Interactive hospital operations dashboard.
- Department-wise bed occupancy monitoring.
- Patient flow and demographic analysis.
- Clinical and laboratory data analysis.
- Financial and billing analytics.
- Interactive charts and visualizations.
- CSV data export.

## Learning Outcomes

Through this project, I am exploring and implementing:

- Python programming and application development.
- Relational database design and normalization.
- SQL queries and analytical operations.
- Synthetic data generation.
- Data cleaning and transformation using Pandas.
- Real-time-style data simulation.
- Interactive dashboard development using Streamlit.
- Data visualization using Plotly.
- Healthcare KPI analysis.
- End-to-end project development.

## Future Enhancements

The project can be extended with additional features, including:

- Hospital admission forecasting using machine learning.
- Bed occupancy and demand prediction.
- Emergency department waiting-time prediction.
- Patient readmission risk prediction.
- Automated operational alerts.
- Advanced department performance analysis.
- Cloud deployment.

## Disclaimer

This project uses synthetic hospital data and is developed for educational, analytical, and portfolio purposes. It does not use real patient records and is not intended for clinical diagnosis, treatment recommendations, or actual hospital decision-making.

## Author

Sivaratri Manish

GitHub:(https://github.com/Manish90-mana)

---

If you find this project interesting, feel free to explore the repository and share your feedback.

