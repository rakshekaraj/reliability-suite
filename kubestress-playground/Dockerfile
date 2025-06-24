# FROM python:3.9-slim

# WORKDIR /app
# COPY . .

# # Install curl and download kubectl safely
# RUN apt-get update && apt-get install -y curl && \
#     curl -LO https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kubectl && \
#     install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
#     rm kubectl && \
#     apt-get remove -y curl && apt-get clean

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 8501

# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]

FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y curl && \
    curl -LO https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kubectl && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl && \
    apt-get remove -y curl && apt-get clean

# For KUBECONFIG
RUN mkdir -p /root/.kube

# Python deps
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
