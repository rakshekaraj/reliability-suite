import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# ------------------ MOCK DATA ------------------
FAKE_PODS = ["reliability-api-abc123", "reliability-api-def456", "reliability-api-ghi789"]

FAKE_HPA_STATUS = """NAME                   REFERENCE                     TARGETS         MINPODS   MAXPODS
reliability-api-hpa   Deployment/reliability-api   75%/50%          2         5
"""

if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = {pod: [] for pod in FAKE_PODS}

# ------------------ PAGE LAYOUT ------------------
st.set_page_config(layout="wide")
st.title("🧪 KubeStress Playground (Simulated)")
st.markdown("Simulate load on Kubernetes pods and watch autoscaling **mocked** in action!")

# ------------------ POD SIMULATION ------------------
st.subheader("📦 Current Pods")
st.json(FAKE_PODS)

selected_pod = st.selectbox("Select a pod to stress", FAKE_PODS, key="stress")

if st.button("🔥 Simulate CPU Load"):
    new_cpu = random.randint(40, 100)
    now = pd.Timestamp.now()
    st.session_state.cpu_history[selected_pod].append({"time": now, "cpu": new_cpu})
    st.success(f"Mock CPU stress on {selected_pod} at {new_cpu} millicores")

# ------------------ METRICS ------------------
st.subheader("📊 Pod Metrics")
st.code("Mock: kubectl top pods")
for pod in FAKE_PODS:
    usage = st.session_state.cpu_history[pod][-1]["cpu"] if st.session_state.cpu_history[pod] else 0
    st.text(f"{pod} - {usage} millicores")

st.subheader("📈 HPA Status (Mock)")
st.code(FAKE_HPA_STATUS)

# ------------------ CPU HISTORY CHART ------------------
st.markdown("---")
chart_pod = st.selectbox("📈 View CPU chart for pod", FAKE_PODS, key="chart")

if chart_pod in st.session_state.cpu_history and st.session_state.cpu_history[chart_pod]:
    df = pd.DataFrame(st.session_state.cpu_history[chart_pod])
    fig = px.line(df, x="time", y="cpu", title=f"CPU Usage Over Time: {chart_pod} (millicores)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No CPU history for this pod yet.")

# ------------------ AUTO REFRESH ------------------
auto_refresh = st.checkbox("🔄 Auto-refresh every 5 seconds", value=True)
if auto_refresh:
    time.sleep(5)
    st.rerun()
