"""MediOps Streamlit hospital operations dashboard."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DB_PATH = Path(__file__).with_name("mediops.db")
st.set_page_config(page_title="MediOps | Hospital Intelligence", page_icon="🏥",
                   layout="wide", initial_sidebar_state="expanded")

# ---------- Visual system ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #F4F7FB; }
section[data-testid="stSidebar"] { background: #14263D; }
section[data-testid="stSidebar"] * { color: #EAF1FA !important; }
.block-container { padding-top: 1.7rem; padding-bottom: 2rem; max-width: 1500px; }
h1,h2,h3 { font-family: 'Manrope', sans-serif; color: #172B45; }
[data-testid="stMetric"] { background: white; padding: 16px 18px; border: 1px solid #E6ECF3; border-radius: 13px; box-shadow: 0 2px 8px rgba(20,38,61,.035); }
[data-testid="stMetricLabel"] { color: #718096; font-weight: 600; }
[data-testid="stMetricValue"] { color: #172B45; font-weight: 800; }
div[data-testid="stTabs"] button { font-weight: 650; }
div[data-testid="stDataFrame"] { border: 1px solid #E6ECF3; border-radius: 10px; }
.muted { color: #718096; font-size: 0.88rem; }
.eyebrow { color: #2685C7; font-weight: 800; letter-spacing: .11em; font-size: .72rem; }
.hero { background: linear-gradient(115deg,#14263D,#203F61); padding: 22px 26px; border-radius: 16px; color: white; margin-bottom: 18px; }
.hero h1 { color: white; margin: 3px 0 4px 0; font-size: 1.8rem; }
.hero p { color: #C9D8E8; margin: 0; }
</style>
""", unsafe_allow_html=True)

def get_connection():
    if not DB_PATH.exists():
        st.error("Database not found. In the project terminal run: `python generator.py`")
        st.stop()
    con = sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)
    con.execute("PRAGMA foreign_keys=ON")
    return con

def q(sql: str, params=()) -> pd.DataFrame:
    """Run a parameterized SQL query and return its result as a DataFrame."""
    with get_connection() as con:
        return pd.read_sql_query(sql, con, params=params)

def scalar(sql: str, params=(), default=0):
    df = q(sql, params)
    if df.empty or pd.isna(df.iloc[0, 0]):
        return default
    return df.iloc[0, 0]

def money(value):
    return f"₹{value:,.0f}"

def empty_state(message):
    st.info(message)

def chart_layout(fig, height=320):
    fig.update_layout(height=height, margin=dict(l=10,r=10,t=35,b=10),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="DM Sans", color="#526174"),
                      legend_title_text="")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#E9EEF5", zeroline=False)
    return fig

def occupancy():
    """Calculate active inpatients by department, joined to bed capacity."""
    return q("""
        SELECT d.department_name, d.bed_capacity,
               COUNT(a.admission_id) AS occupied_beds,
               ROUND(100.0 * COUNT(a.admission_id) / d.bed_capacity, 1) AS occupancy_pct
        FROM departments d
        LEFT JOIN admissions a ON a.department_id=d.department_id
          AND a.discharge_date IS NULL AND a.outcome='Admitted'
        GROUP BY d.department_id, d.department_name, d.bed_capacity
        ORDER BY occupancy_pct DESC
    """)

def kpi_snapshot():
    active = int(scalar("SELECT COUNT(*) FROM admissions WHERE discharge_date IS NULL AND outcome='Admitted'"))
    capacity = int(scalar("SELECT SUM(bed_capacity) FROM departments"))
    admitted_24 = int(scalar("SELECT COUNT(*) FROM admissions WHERE admission_date >= datetime('now','-1 day')"))
    discharged_24 = int(scalar("SELECT COUNT(*) FROM admissions WHERE discharge_date >= datetime('now','-1 day')"))
    avg_stay = float(scalar("""SELECT AVG((julianday(discharge_date)-julianday(admission_date)))
                               FROM admissions WHERE discharge_date IS NOT NULL""", default=0))
    critical = int(scalar("SELECT COUNT(*) FROM lab_results WHERE status='Critical' AND result_date >= datetime('now','-1 day')"))
    return active, capacity, admitted_24, discharged_24, avg_stay, critical

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🏥 MediOps")
    st.caption("HOSPITAL INTELLIGENCE PLATFORM")
    st.divider()
    st.markdown("**CONTROL CENTER**")
    refresh = st.selectbox("Dashboard refresh", ["5 seconds","10 seconds","30 seconds","Manual"], index=1)
    refresh_seconds = {"5 seconds":5,"10 seconds":10,"30 seconds":30,"Manual":None}[refresh]
    departments = q("SELECT department_name FROM departments ORDER BY department_name")["department_name"].tolist()
    selected_depts = st.multiselect("Departments", departments, default=departments)
    st.divider()
    clock_df = q("SELECT hospital_time,last_tick FROM sim_clock WHERE clock_id=1")
    if not clock_df.empty:
        st.caption("SIMULATED HOSPITAL TIME")
        st.markdown(f"**{pd.to_datetime(clock_df.iloc[0]['hospital_time']).strftime('%d %b %Y, %H:%M')}**")
        st.caption("Start `python simulator.py` in another terminal to stream activity.")
    st.divider()
    st.caption("DEMO DATA · SYNTHETIC ONLY")
    st.caption("MediOps v1.0")

# ---------- Header and filters ----------
st.markdown("""<div class="hero"><div class="eyebrow">HOSPITAL COMMAND CENTER</div>
<h1>Operations overview</h1><p>Monitor patient flow, clinical signals and financial performance in one place.</p></div>""",
            unsafe_allow_html=True)
today = datetime.now().date()
date_range = st.date_input("Analytics date range", value=(today - timedelta(days=30), today),
                           max_value=today, help="Controls the date-based charts and tables below.")
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = today - timedelta(days=30), today
start_ts = datetime.combine(start_date, datetime.min.time()).isoformat()
end_ts = datetime.combine(end_date + timedelta(days=1), datetime.min.time()).isoformat()
dept_filter = selected_depts or departments
placeholders = ",".join("?" for _ in dept_filter)

tab_ops, tab_trends, tab_fin, tab_clin, tab_data = st.tabs(
    ["⚡ Live Ops","📈 Trends","💳 Financial","🧬 Clinical","🗂 Data Explorer"])

# Live fragment: only this section reruns on the selected interval.
@st.fragment(run_every=refresh_seconds)
def live_operations():
    active, capacity, admitted_24, discharged_24, avg_stay, critical = kpi_snapshot()
    occupancy_rate = (active / capacity * 100) if capacity else 0
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Inpatients", f"{active:,}", help="Currently admitted patients")
    c2.metric("Bed occupancy", f"{occupancy_rate:.1f}%", help=f"{active} occupied of {capacity} beds")
    c3.metric("Admissions · 24h", f"{admitted_24:,}")
    c4.metric("Discharges · 24h", f"{discharged_24:,}")
    c5.metric("Average stay", f"{avg_stay:.1f} days")
    c6.metric("Critical labs · 24h", f"{critical:,}")
    st.markdown("### Capacity watch")
    occ = occupancy()
    if not occ.empty:
        occ["alert"] = occ["occupancy_pct"].apply(lambda x: "Critical" if x >= 90 else ("Watch" if x >= 75 else "Normal"))
        left,right = st.columns([1.35,1])
        with left:
            fig = px.bar(occ.sort_values("occupancy_pct"), x="occupancy_pct", y="department_name",
                         orientation="h", color="occupancy_pct", color_continuous_scale=["#2BAE86","#F2B84B","#D9534F"],
                         range_color=[0,100], text="occupancy_pct")
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig.update_layout(coloraxis_showscale=False, xaxis_title="Occupied beds (%)", yaxis_title="")
            st.plotly_chart(chart_layout(fig, 300), use_container_width=True)
        with right:
            st.dataframe(occ[["department_name","occupied_beds","bed_capacity","occupancy_pct","alert"]],
                         hide_index=True, use_container_width=True,
                         column_config={"occupancy_pct":st.column_config.ProgressColumn("Occupancy",min_value=0,max_value=120,format="%.1f%%")})
        alerts = occ[occ["occupancy_pct"] >= 75]
        if alerts.empty:
            st.success("All departments are below the 75% watch threshold.")
        else:
            for _, row in alerts.iterrows():
                if row["occupancy_pct"] >= 90:
                    st.error(f"Capacity alert · {row['department_name']} is at {row['occupancy_pct']:.1f}% occupancy.")
                else:
                    st.warning(f"Capacity watch · {row['department_name']} is at {row['occupancy_pct']:.1f}% occupancy.")
    st.markdown("### Patient flow · recent 48 hours")
    flow = q("""WITH hours AS (
                  SELECT strftime('%Y-%m-%d %H:00', admission_date) AS hour,
                         COUNT(*) AS admissions, 0 AS discharges
                  FROM admissions WHERE admission_date >= datetime('now','-48 hours')
                  GROUP BY hour
                  UNION ALL
                  SELECT strftime('%Y-%m-%d %H:00', discharge_date) AS hour,
                         0, COUNT(*) FROM admissions
                  WHERE discharge_date >= datetime('now','-48 hours') GROUP BY hour
                )
                SELECT hour, SUM(admissions) admissions, SUM(discharges) discharges
                FROM hours GROUP BY hour ORDER BY hour""")
    if not flow.empty:
        flow_long = flow.melt(id_vars="hour",var_name="event",value_name="patients")
        fig = px.area(flow_long, x="hour", y="patients", color="event",
                      color_discrete_map={"admissions":"#3182CE","discharges":"#2BAE86"})
        st.plotly_chart(chart_layout(fig,260),use_container_width=True)
    a,b = st.columns(2)
    with a:
        st.markdown("### Latest admissions")
        latest = q("""SELECT a.admission_id, p.first_name || ' ' || p.last_name AS patient,
                      d.department_name, a.admission_type, a.admission_date
                      FROM admissions a JOIN patients p USING(patient_id)
                      JOIN departments d USING(department_id)
                      ORDER BY a.admission_date DESC LIMIT 8""")
        st.dataframe(latest,hide_index=True,use_container_width=True)
    with b:
        st.markdown("### Critical laboratory results")
        labs = q("""SELECT l.test_name,l.result_value,l.unit,l.status,l.result_date,
                    p.first_name || ' ' || p.last_name AS patient
                    FROM lab_results l JOIN admissions a USING(admission_id)
                    JOIN patients p USING(patient_id)
                    WHERE l.status='Critical' ORDER BY l.result_date DESC LIMIT 8""")
        if labs.empty: empty_state("No critical results in the available data.")
        else: st.dataframe(labs,hide_index=True,use_container_width=True)

with tab_ops:
    live_operations()

with tab_trends:
    st.markdown("### Patient activity and outcomes")
    admissions = q("""SELECT a.*,d.department_name,p.gender,
                      CAST((julianday(a.admission_date)-julianday(p.date_of_birth))/365.25 AS INTEGER) age
                      FROM admissions a JOIN departments d USING(department_id)
                      JOIN patients p USING(patient_id)
                      WHERE a.admission_date >= ? AND a.admission_date < ?""",(start_ts,end_ts))
    if admissions.empty:
        empty_state("No admissions found for this date range.")
    else:
        c1,c2 = st.columns(2)
        with c1:
            daily = admissions.assign(day=pd.to_datetime(admissions.admission_date).dt.date).groupby("day").size().reset_index(name="admissions")
            st.plotly_chart(chart_layout(px.line(daily,x="day",y="admissions",markers=True,title="Admissions per day")),use_container_width=True)
        with c2:
            outcome = admissions.groupby("outcome").size().reset_index(name="patients")
            st.plotly_chart(chart_layout(px.pie(outcome,names="outcome",values="patients",hole=.55,title="Admission outcomes")),use_container_width=True)
        c3,c4 = st.columns(2)
        with c3:
            by_dept = admissions.groupby("department_name").agg(admissions=("admission_id","count"),
                avg_planned_stay=("length_of_stay","mean")).reset_index()
            st.plotly_chart(chart_layout(px.bar(by_dept,x="department_name",y="admissions",title="Admissions by department")),use_container_width=True)
        with c4:
            admissions["age_band"] = pd.cut(admissions["age"],[0,18,30,45,60,75,110],
                                              labels=["0–17","18–29","30–44","45–59","60–74","75+"])
            age_gender = admissions.groupby(["age_band","gender"],observed=False).size().reset_index(name="patients")
            st.plotly_chart(chart_layout(px.bar(age_gender,x="age_band",y="patients",color="gender",barmode="group",title="Age and gender profile")),use_container_width=True)
        completed = admissions[admissions.discharge_date.notna()].copy()
        if not completed.empty:
            completed["actual_stay"] = (pd.to_datetime(completed.discharge_date)-pd.to_datetime(completed.admission_date)).dt.total_seconds()/86400
            st.plotly_chart(chart_layout(px.box(completed,x="department_name",y="actual_stay",color="department_name",title="Actual length of stay by department")),use_container_width=True)
        heat = admissions.assign(day=pd.to_datetime(admissions.admission_date).dt.day_name(),
                                 hour=pd.to_datetime(admissions.admission_date).dt.hour).groupby(["day","hour"]).size().reset_index(name="arrivals")
        pivot = heat.pivot(index="day",columns="hour",values="arrivals").fillna(0)
        order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        pivot=pivot.reindex(order)
        st.plotly_chart(chart_layout(px.imshow(pivot,aspect="auto",labels=dict(x="Hour of day",y="Day",color="Admissions"),title="Arrival intensity heatmap"),330),use_container_width=True)

with tab_fin:
    st.markdown("### Revenue cycle")
    billing = q("""SELECT b.*,a.department_id,d.department_name,a.admission_date
                   FROM billing b JOIN admissions a USING(admission_id)
                   JOIN departments d USING(department_id)
                   WHERE b.bill_date >= ? AND b.bill_date < ?""",(start_ts,end_ts))
    if billing.empty:
        empty_state("No billing records found for this date range.")
    else:
        billed=billing.billed_amount.sum()
        collected=billing.collected_amount.sum()
        rate=collected/billed*100 if billed else 0
        x1,x2,x3=st.columns(3)
        x1.metric("Total billed",money(billed))
        x2.metric("Collected",money(collected))
        x3.metric("Collection rate",f"{rate:.1f}%")
        c1,c2=st.columns(2)
        with c1:
            payer=billing.groupby("payer_type")[["billed_amount","collected_amount"]].sum().reset_index()
            fig=px.bar(payer,x="payer_type",y=["billed_amount","collected_amount"],barmode="group",title="Billed vs collected by payer")
            st.plotly_chart(chart_layout(fig),use_container_width=True)
        with c2:
            mix=billing.groupby("payer_type").billed_amount.sum().reset_index()
            st.plotly_chart(chart_layout(px.pie(mix,names="payer_type",values="billed_amount",hole=.5,title="Payer mix by billed amount")),use_container_width=True)
        top=q("""SELECT procedure_name,procedure_category,SUM(procedure_cost) total_cost,
                 COUNT(*) procedure_count FROM procedures p
                 JOIN admissions a USING(admission_id)
                 WHERE p.procedure_date >= ? AND p.procedure_date < ?
                 GROUP BY procedure_name,procedure_category ORDER BY total_cost DESC LIMIT 10""",(start_ts,end_ts))
        st.plotly_chart(chart_layout(px.bar(top.sort_values("total_cost"),x="total_cost",y="procedure_name",orientation="h",color="procedure_category",title="Top procedures by cost")),use_container_width=True)
        st.caption("Amounts are synthetic demonstration values, displayed in Indian rupees (₹).")

with tab_clin:
    st.markdown("### Clinical intelligence")
    labs=q("""SELECT l.*,a.admission_date FROM lab_results l JOIN admissions a USING(admission_id)
              WHERE l.result_date >= ? AND l.result_date < ?""",(start_ts,end_ts))
    diagnoses=q("""SELECT dg.diagnosis_name,dg.diagnosis_code,dg.diagnosis_type,
                   COUNT(*) patients FROM diagnoses dg JOIN admissions a USING(admission_id)
                   WHERE a.admission_date >= ? AND a.admission_date < ?
                   GROUP BY dg.diagnosis_name,dg.diagnosis_code,dg.diagnosis_type
                   ORDER BY patients DESC LIMIT 10""",(start_ts,end_ts))
    c1,c2=st.columns(2)
    with c1:
        if labs.empty: empty_state("No lab results in this date range.")
        else:
            mix=labs.groupby("status").size().reset_index(name="results")
            st.plotly_chart(chart_layout(px.pie(mix,names="status",values="results",hole=.5,title="Laboratory status distribution")),use_container_width=True)
    with c2:
        if diagnoses.empty: empty_state("No diagnoses in this date range.")
        else: st.plotly_chart(chart_layout(px.bar(diagnoses.sort_values("patients"),x="patients",y="diagnosis_name",orientation="h",title="Most frequent diagnoses")),use_container_width=True)
    meds=q("""SELECT m.medication_name,COUNT(*) prescriptions FROM medications m
              JOIN admissions a USING(admission_id) WHERE a.admission_date >= ? AND a.admission_date < ?
              GROUP BY m.medication_name ORDER BY prescriptions DESC LIMIT 10""",(start_ts,end_ts))
    st.plotly_chart(chart_layout(px.bar(meds,x="medication_name",y="prescriptions",title="Most prescribed medications")),use_container_width=True)
    readmit=q("""WITH discharged AS (
        SELECT patient_id,admission_id,discharge_date FROM admissions
        WHERE discharge_date IS NOT NULL AND discharge_date >= ? AND discharge_date < ?
    ), flagged AS (
        SELECT d.admission_id, CASE WHEN EXISTS (
          SELECT 1 FROM admissions next
          WHERE next.patient_id=d.patient_id AND next.admission_date > d.discharge_date
            AND julianday(next.admission_date)-julianday(d.discharge_date) <= 30
        ) THEN 1 ELSE 0 END AS readmitted FROM discharged d
    ) SELECT COUNT(*) eligible,COALESCE(SUM(readmitted),0) readmissions FROM flagged""",(start_ts,end_ts))
    eligible=int(readmit.iloc[0]["eligible"]) if not readmit.empty else 0
    readmissions=int(readmit.iloc[0]["readmissions"]) if not readmit.empty else 0
    st.metric("30-day readmission rate",f"{readmissions/eligible*100:.1f}%" if eligible else "N/A",
              help=f"{readmissions} readmissions among {eligible} eligible discharges in selected discharge window")
    st.caption("Readmission is defined here as another admission for the same synthetic patient within 30 days.")

with tab_data:
    st.markdown("### Database explorer")
    tables=q("""SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name""")["name"].tolist()
    chosen=st.selectbox("Choose a database table",tables)
    limit=st.select_slider("Rows to preview",options=[25,50,100,250,500],value=100)
    data=q(f'SELECT * FROM "{chosen}" LIMIT ?', (limit,))
    st.caption(f"Showing up to {limit} rows from `{chosen}`.")
    st.dataframe(data,use_container_width=True,hide_index=True)
    st.download_button("⬇ Download this table as CSV",data=data.to_csv(index=False).encode("utf-8"),
                       file_name=f"mediops_{chosen}.csv",mime="text/csv")

st.markdown("---")
st.markdown('<p class="muted">MediOps is an educational analytics prototype using synthetic data. It is not a clinical decision-support system.</p>',
            unsafe_allow_html=True)
