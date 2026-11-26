# MediOps — Live Hospital Operations & Analytics Dashboard

MediOps is an end-to-end healthcare analytics portfolio project. It creates a normalized synthetic hospital database, simulates live admissions/discharges, and visualizes operational, clinical, and financial metrics in Streamlit.

> **Data safety:** All records are synthetic. This project is for learning and portfolio demonstration only; it is not a clinical decision-support system.

## Features

- SQLite relational schema with primary keys, foreign keys, constraints and indexes
- Synthetic patient and admission history (default: 180 days)
- Related diagnoses, laboratory results, medications, procedures and billing
- Live simulator with a hospital clock, patient arrivals and discharges
- Streamlit dashboard with live KPIs and five sections:
  - Live Ops: occupancy, capacity alerts, patient flow, recent admissions and critical labs
  - Trends: admissions, outcomes, stay, age/gender and arrival heatmap
  - Financial: billed vs collected, payer mix and procedure costs
  - Clinical: diagnoses, medications, lab status and 30-day readmissions
  - Data Explorer: inspect and export tables as CSV

## Requirements

- Python 3.10+
- VS Code recommended
- SQLite (included with Python)

## Setup

Open this folder in VS Code. In the VS Code terminal:

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python generator.py
```

If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generator.py
```

## Run the application

Use three terminals in VS Code.

**Terminal 1 — dashboard**

```bash
streamlit run app.py
```

Open the local URL Streamlit prints, normally `http://localhost:8501`.

**Terminal 2 — live simulator**

```bash
python simulator.py
```

The simulator advances one hospital hour every two real seconds.

**Optional Terminal 3 — patient surge**

```bash
python simulator.py --rate 2.5
```

Use this only as an additional simulator process if you want to stress the capacity alerts. Stop a simulator with `Ctrl+C`.

## Rebuild the database

```bash
python generator.py
```

Optional data volume:

```bash
python generator.py --days 180 --patients 1000
```

This rebuilds `mediops.db` from scratch. Stop the simulator and dashboard first if you are regenerating the database.

## Project structure

```text
MediOps/
├── app.py             # Streamlit UI, SQL analytics and Plotly charts
├── generator.py       # Database schema, synthetic records and seed process
├── simulator.py       # Simulated hospital clock, admissions and discharges
├── requirements.txt   # Python dependencies
├── README.md          # Setup, architecture and learning notes
└── mediops.db         # Generated SQLite database (created by generator.py)
```

## Database model

- `departments` 1 → many `admissions`
- `cities` 1 → many `patients`
- `patients` 1 → many `admissions`
- `admissions` 1 → many `diagnoses`
- `admissions` 1 → many `lab_results`
- `admissions` 1 → many `medications`
- `admissions` 1 → many `procedures`
- `admissions` 1 → 1 `billing`
- `sim_clock` stores the simulated hospital time

The dashboard queries related tables separately or aggregates them before joining. This avoids the common row multiplication problem caused by joining several one-to-many tables (for example, 3 diagnoses × 4 labs × 2 medications can create 24 joined rows for one admission).

## Important definitions

- **Active inpatient:** `discharge_date IS NULL` and `outcome = 'Admitted'`.
- **Bed occupancy:** active inpatients divided by configured department bed capacity.
- **Planned length of stay:** `admissions.length_of_stay`.
- **Actual length of stay:** discharge timestamp minus admission timestamp, calculated in analytics.
- **Lab status:** Normal is inside the reference range; Abnormal is outside; Critical is more than half a reference-range width beyond a boundary.
- **30-day readmission:** a new admission for the same synthetic patient within 30 days of discharge.

## Learning roadmap

1. Read `SCHEMA` in `generator.py` and identify primary/foreign keys.
2. Run the generator and inspect `mediops.db` with a SQLite viewer.
3. Read `create_patient()` and `create_admission()` to understand record generation.
4. Read `tick()` in `simulator.py` and watch new admissions/discharges.
5. In `app.py`, study `q()`, `scalar()`, `occupancy()` and `kpi_snapshot()`.
6. Change the capacity alert thresholds (75% and 90%) and observe the dashboard.
7. Add an analysis, such as average bill by patient city/region.
8. Capture screenshots, write findings and publish the repository.

## Ideas for the next version

- Staff workload and patient-to-doctor ratios
- Length-of-stay prediction (with a properly separated train/test dataset)
- Alert history table and alert acknowledgement workflow
- Readmission risk model with transparent evaluation
- Export a carefully aggregated fact table for Power BI/Tableau
- Authentication and role-based access for a production-style demo

## GitHub publishing

Do not commit a virtual environment. The generated database is small and can be committed for a reproducible demo, but regenerate it on startup for cloud deployment if preferred. Add a `.gitignore` for `.venv/`, `__pycache__/`, `*.pyc`, and SQLite WAL sidecar files.
