"""Advance the simulated hospital clock and create live activity.

Run: python simulator.py
Optional faster/busier simulation: python simulator.py --rate 2.5
Stop with Ctrl+C.
"""
from __future__ import annotations
import argparse
import random
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from generator import DB_PATH, connect, create_admission

RNG = random.Random()

def tick(con: sqlite3.Connection, rate: float = 1.0) -> dict:
    """Advance hospital time by one simulated hour.

    `rate` scales the average arrival count. A rate above 1 simulates a surge.
    """
    row = con.execute("SELECT hospital_time FROM sim_clock WHERE clock_id=1").fetchone()
    if row is None:
        raise RuntimeError("sim_clock is empty. Run `python generator.py` first.")
    hospital_time = datetime.fromisoformat(row["hospital_time"]) + timedelta(hours=1)

    # Discharge due patients. Discharge is based on each admission's planned stay.
    due = con.execute(
        """SELECT admission_id, admission_date, length_of_stay
           FROM admissions
           WHERE discharge_date IS NULL AND outcome='Admitted'"""
    ).fetchall()
    discharged = 0
    for admission in due:
        admitted_at = datetime.fromisoformat(admission["admission_date"])
        if hospital_time >= admitted_at + timedelta(days=admission["length_of_stay"]):
            outcome = RNG.choices(["Discharged","Transferred","Expired"], [96,3,1], k=1)[0]
            con.execute("UPDATE admissions SET discharge_date=?, outcome=? WHERE admission_id=?",
                        (hospital_time.isoformat(timespec="seconds"), outcome, admission["admission_id"]))
            con.execute("""UPDATE medications SET end_date=COALESCE(end_date,?)
                           WHERE admission_id=?""",
                        (hospital_time.isoformat(timespec="seconds"), admission["admission_id"]))
            bill = con.execute("SELECT billed_amount FROM billing WHERE admission_id=?",
                               (admission["admission_id"],)).fetchone()
            if bill:
                billed = float(bill["billed_amount"])
                collected = round(billed * RNG.uniform(0.65, 1.0), 2)
                con.execute("""UPDATE billing SET collected_amount=?, bill_date=?, payment_status=?
                               WHERE admission_id=?""",
                            (collected, hospital_time.isoformat(timespec="seconds"),
                             "Paid" if collected >= billed * .95 else "Partial",
                             admission["admission_id"]))
            discharged += 1

    # Daytime arrivals are higher than overnight arrivals.
    hour = hospital_time.hour
    day_factor = 1.55 if 8 <= hour <= 20 else 0.55
    arrivals = min(12, RNG.poissonvariate(1.6 * rate * day_factor)) if hasattr(RNG, "poissonvariate") else min(
        12, sum(1 for _ in range(12) if RNG.random() < min(0.95, (1.6 * rate * day_factor) / 12))
    )
    for _ in range(arrivals):
        create_admission(con, hospital_time, force_active=True)

    con.execute("UPDATE sim_clock SET hospital_time=?, last_tick=? WHERE clock_id=1",
                (hospital_time.isoformat(timespec="seconds"), datetime.now().isoformat(timespec="seconds")))
    con.commit()
    return {"hospital_time": hospital_time, "arrivals": arrivals, "discharges": discharged}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rate", type=float, default=1.0,
                        help="Arrival intensity multiplier; >1 creates a patient surge")
    parser.add_argument("--interval", type=float, default=2.0,
                        help="Real seconds between simulated hospital hours")
    args = parser.parse_args()
    if args.rate <= 0 or args.interval <= 0:
        parser.error("--rate and --interval must be greater than zero")
    db = Path(DB_PATH)
    if not db.exists():
        raise SystemExit("Database not found. Run `python generator.py` first.")
    con = connect()
    print(f"MediOps simulator running (rate={args.rate}, interval={args.interval}s). Ctrl+C to stop.")
    try:
        while True:
            result = tick(con, args.rate)
            print(f"{result['hospital_time']:%Y-%m-%d %H:%M} | "
                  f"+{result['arrivals']} admissions | -{result['discharges']} discharges")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nSimulator stopped.")
    finally:
        con.close()

if __name__ == "__main__":
    main()
