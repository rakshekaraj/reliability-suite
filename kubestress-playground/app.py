import streamlit as st
import pandas as pd
import plotly.express as px
import time
from kubectl_utils import get_pods, exec_cpu_load, get_pod_metrics, get_hpa_status

# --- SESSION STATE FOR HISTORY ---
if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = {}

# --- POD LOAD CONTROL UI ---
st.title("🧪 KubeStress Playground")
st.markdown("Simulate load on Kubernetes pods and watch autoscaling in action!")

# Get current pods
pods = get_pods()
st.subheader("📦 Current Pods")
st.json(pods)

selected_pod = st.selectbox("Select a pod to stress", pods)

if st.button("🔥 Simulate CPU Load"):
    exec_cpu_load(selected_pod)
    st.success(f"Started CPU stress on pod: {selected_pod}")

# --- METRICS ---
st.subheader("📊 Pod Metrics (`kubectl top pods`)")
metrics_raw = get_pod_metrics()
st.code(metrics_raw)

st.subheader("📈 HPA Status (`kubectl get hpa`)")
st.code(get_hpa_status())

# --- CPU METRIC HISTORY + CHART ---
def parse_pod_metrics(raw_output):
    lines = raw_output.strip().split("\n")[1:]  # Skip header
    data = []
    timestamp = pd.Timestamp.now()
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:
            name, cpu = parts[0], parts[1]
            if cpu.endswith("m"):
                cpu_val = int(cpu.replace("m", ""))
            else:
                cpu_val = int(cpu) * 1000  # fallback
            data.append((name, cpu_val, timestamp))
    return data

metrics_data = parse_pod_metrics(metrics_raw)
for name, cpu, ts in metrics_data:
    if name not in st.session_state.cpu_history:
        st.session_state.cpu_history[name] = []
    st.session_state.cpu_history[name].append({"time": ts, "cpu": cpu})

st.markdown("---")

# Only one selectbox with a unique key
chart_pod = st.selectbox(
    "📈 View CPU chart for pod",
    [d[0] for d in metrics_data] if metrics_data else [],
    key="chart_selectbox"
)

# Plot chart if pod has history
if chart_pod and chart_pod in st.session_state.cpu_history:
    history_df = pd.DataFrame(st.session_state.cpu_history[chart_pod])
    if not history_df.empty:
        fig = px.line(history_df, x="time", y="cpu", title=f"CPU Usage Over Time: {chart_pod} (millicores)")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No pod selected or no CPU history available.")

# --- AUTO REFRESH ---
auto_refresh = st.checkbox("🔄 Auto-refresh every 5 seconds", value=True)
if auto_refresh:
    time.sleep(5)
    st.rerun()
