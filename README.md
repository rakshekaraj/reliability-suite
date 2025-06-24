# Reliability Suite
 Try out the idea w dummy pods here : https://reliability-suite.onrender.com

A complete suite for simulating and visualizing reliability behavior in Kubernetes environments. This project combines failure injection with real-time Kubernetes autoscaling and resource monitoring via dashboards.

## Project Structure

This repo contains two main components:
- **reliability-simulator**: Kubernetes deployment with Prometheus + pod failure injector.
- **kubestress-playground**: Streamlit dashboard to simulate stress and visualize CPU metrics live.

## reliability-simulator

This module simulates a microservice workload, applies resource stress through a shell script, and exposes metrics through Prometheus.

### Features

- Horizontal Pod Autoscaler (HPA) for scaling based on CPU metrics
- Prometheus for scraping pod metrics
- AlertManager configuration scaffolded
- Failure injection via simple subprocess call or stress script

### How to Run

```bash
cd reliability-simulator
kubectl apply -f k8s/
bash scripts/inject_failure.sh
```

Optional: Set up Prometheus port forwarding for local access.

```bash
kubectl port-forward svc/prometheus-service 9090
```

## kubestress-playground

This dashboard enables direct interaction with running Kubernetes pods. Users can:

- List current pods
- Select and stress a pod’s CPU in real-time
- Visualize CPU usage over time
- Enable auto-refresh of the chart

### Local Setup

Make sure `kubectl` is installed and configured (e.g., via minikube).

```bash
cd kubestress-playground
streamlit run app.py
```

### Docker Build (for deployment)

```bash
docker build -t kubestress-dashboard .
docker run -p 8501:8501 kubestress-dashboard
```

## Deployment on Render

To deploy the Streamlit dashboard:

1. Push this repository to GitHub
2. Link to Render (choose "Web Service")
3. Use Docker as the deployment method
4. Set port to 8501
5. Optional: Mount Kubernetes credentials inside the container

If you use minikube locally, the dashboard assumes `kubectl` can access the cluster.

## Stack Overview

- Python 3.9
- Streamlit
- Plotly
- Prometheus
- Kubernetes (via kubectl)
- Docker
- Bash scripting

## Author

Raksheka Rajakumar  
Portfolio: [raksheka.me](https://raksheka.me)  
GitHub: [github.com/rakshekaraj](https://github.com/rakshekaraj)

## License

This project is licensed under the MIT License.
