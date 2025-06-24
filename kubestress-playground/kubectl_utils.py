import subprocess

def get_pods(label="app=reliability-api"):
    result = subprocess.run(
        ["kubectl", "get", "pods", "-l", label, "-o", "jsonpath={.items[*].metadata.name}"],
        capture_output=True, text=True
    )
    return result.stdout.strip().split()

def exec_cpu_load(pod_name):
    command = f"kubectl exec {pod_name} -- python3 -c \"while True: sum([i*i for i in range(1000)])\""
    return subprocess.Popen(command, shell=True)

def get_hpa_status():
    result = subprocess.run(
        ["kubectl", "get", "hpa", "reliability-api-hpa"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def get_pod_metrics():
    try:
        result = subprocess.run(
            ["kubectl", "top", "pods"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return str(e)
