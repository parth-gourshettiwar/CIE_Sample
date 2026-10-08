# DevOps CIE-01 Practical Assessment Project
# added new line
This is a simple, reliable Python Flask API created specifically for demonstrating a full DevOps CI/CD pipeline and monitoring stack.

## Project Structure
```text
devops-task-api/
├── app/
│   ├── __init__.py     # Flask app factory, initializes routes and metrics
│   ├── routes.py       # API endpoints (/health, /tasks, etc.)
│   └── metrics.py      # Prometheus metrics configuration
├── tests/
│   └── test_api.py     # pytest file to test API endpoints
├── k8s/
│   ├── deployment.yaml # Kubernetes Deployment manifest (replicas, probes)
│   └── service.yaml    # Kubernetes Service manifest (NodePort)
├── prometheus/
│   └── prometheus.yml  # Prometheus configuration for scraping the API
├── Dockerfile          # Instructions to build the Docker image
├── requirements.txt    # Python dependencies
├── .gitignore          # Files to ignore in Git (venv, pycache)
├── Jenkinsfile         # CI/CD pipeline definition
└── run.py              # Entry point to run the Flask application
```

## How to Run Locally

1. Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python run.py
   ```
   The API will be available at `http://localhost:5000`.

## How to Run Tests

Run pytest inside the activated virtual environment:
```bash
pytest
```
Tests will execute without needing a database or external services.

## How to Build/Run Docker

1. Build the image:
   ```bash
   docker build -t devops-task-api:1.0 .
   ```
2. Run the container:
   ```bash
   docker run -d -p 5000:5000 --name devops-api devops-task-api:1.0
   ```
3. Verify it is running:
   ```bash
   docker ps
   docker logs devops-api
   ```
   Access `http://localhost:5000/health`.

## How to Deploy to Kubernetes

1. Apply the manifests:
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```
2. Verify deployment:
   ```bash
   kubectl get pods
   kubectl get svc
   ```
   The application will be accessible via the assigned NodePort (e.g., 30005).

## How Prometheus Connects

The API exposes a `/metrics` endpoint using the `prometheus_client` library. The `prometheus.yml` file configures Prometheus to scrape this endpoint every 5 seconds. You can start Prometheus passing this config file, and it will collect metrics like `app_request_count` and `app_request_latency_seconds`.

## How Grafana Connects

1. Add Prometheus as a Data Source in Grafana (URL: `http://localhost:9090` or Prometheus Service IP).
2. Create a dashboard using PromQL queries.
   - **Request Count**: `sum(rate(app_request_count_total[1m])) by (endpoint)`
   - **Error Rate**: `sum(rate(app_request_count_total{http_status="500"}[1m]))`

## How Jenkins Connects to Git

The `Jenkinsfile` contains a pipeline. When integrated with Jenkins (e.g., using GitHub Webhooks or polling), Jenkins pulls the code from Git. The `checkout scm` step automatically checks out the branch that triggered the build.

---

## Why Each DevOps Tool Is Used

**Git:**
*What problem does Git solve?* It solves the problem of tracking changes in code over time and allowing multiple developers to collaborate without overwriting each other's work.

**CI/CD (Jenkins/GitHub Actions):**
*Why automate build/test/deployment?* Manual testing and deployment are slow and error-prone. CI/CD ensures that every change is automatically tested and reliably deployed, reducing human error.

**Docker:**
*Why package the application into a container?* "It works on my machine" is a common problem. Docker packages the app and its dependencies together, guaranteeing it runs the exact same way everywhere.

**Kubernetes:**
*Why use Kubernetes when Docker can already run a container?* Docker runs single containers well, but managing hundreds of containers, scaling them, and replacing them if they crash is difficult. Kubernetes automates the management, scaling, and recovery of containers.

**Prometheus:**
*Why collect application metrics?* We need to know if the application is healthy, how much traffic it receives, and if it's slow. Prometheus constantly collects this data.

**Grafana:**
*Why visualize Prometheus metrics?* Raw metric numbers are hard to interpret. Grafana turns Prometheus data into visual graphs and dashboards, making it easy for humans to understand system health at a glance.

**The Complete Relationship:**
Code is stored in **Git** → Changes trigger **CI/CD** → CI/CD tests code and builds a **Docker** image → CI/CD deploys the image to **Kubernetes** → The app runs in Kubernetes while **Prometheus** scrapes its metrics → **Grafana** displays those metrics on a dashboard.

---

## CIE Demonstration Mapping

**Git:**
- **Commands**: `git clone`, `git status`, `git add`, `git commit`, `git push`.
- **Branching**: Create a `feature/new-endpoint` branch to show isolated changes.
- **Verification**: Show commit history via `git log` or GitHub UI.

**Jenkins:**
- **Pipeline configuration**: Show `Jenkinsfile`.
- **Trigger**: Push code to trigger pipeline.
- **Deployment**: Show pipeline stages succeeding (Checkout -> Test -> Build -> Deploy).

**Docker:**
- **Dockerfile**: Explain `FROM`, `WORKDIR`, `COPY`, `RUN`.
- **Image**: `docker images` to show the built image.
- **Execution**: `docker run` to show it works independently.

**Kubernetes:**
- **Deployment**: `kubectl apply -f k8s/deployment.yaml`.
- **Scaling**: `kubectl scale deployment devops-task-api --replicas=3`.
- **Troubleshooting**: `kubectl get pods`, `kubectl describe pod`.

**Prometheus:**
- **Configuration**: Show `prometheus.yml`.
- **Targets**: Open Prometheus UI (`/targets`) to show the API is UP.
- **Metrics**: Query `app_request_count_total` in Prometheus UI.

**Grafana:**
- **Dashboard**: Show the configured HTTP request count graph.
- **Query**: Demonstrate modifying a PromQL query.

**Group / End-to-End:**
Make a code change (e.g., change `/health` response) → Push to Git → Watch Jenkins build and deploy → See the new version in Kubernetes → Generate traffic and watch Grafana graphs spike.

---

## Git Demonstration Plan

1. **Initialize**: (Run prior to demo) `git init`, `git add .`, `git commit -m "Initial commit"`.
2. **Branch**: `git checkout -b feature/update-message`.
3. **Edit**: Change description in `app/routes.py`.
4. **Commit**: `git status`, `git add .`, `git commit -m "Update API description"`.
5. **Merge/Push**: Checkout main, merge branch, and push.

---

## End-to-End CIE Demonstration Plan

1. **Start**: Show the running Kubernetes pods and Grafana dashboard.
2. **Trigger**: Push a small code change to Git.
3. **CI/CD**: Open Jenkins and watch the pipeline stages progress.
4. **Deploy**: Run `kubectl get pods -w` to show the old pods terminating and new pods starting.
5. **Verify**: Hit the `/health` endpoint to show the new version is live.
6. **Monitor**: Run a small script to generate traffic (`while true; do curl localhost:5000/tasks; sleep 0.5; done`) and watch the Grafana dashboard update in real-time.

---

## Troubleshooting Guide

**1. Git push does not trigger CI/CD**
- *Symptom*: Code is on GitHub but Jenkins build hasn't started.
- *Likely Cause*: Webhook is misconfigured or Jenkins is not polling.
- *Check*: Check GitHub webhook delivery history. Manually click "Build Now" in Jenkins.

**2. CI/CD build fails at Testing stage**
- *Symptom*: Pipeline is red at "Install Dependencies & Test".
- *Likely Cause*: Syntax error in Python code or missing dependency.
- *Check*: Click the Jenkins stage logs. Read the `pytest` output to find the exact line of failure.

**3. Docker container runs but application is inaccessible**
- *Symptom*: `docker ps` shows container running, but `curl localhost:5000` fails.
- *Likely Cause*: Port mapping is missing or app is bound to `127.0.0.1` instead of `0.0.0.0`.
- *Check*: `docker ps` to verify `0.0.0.0:5000->5000/tcp`. `docker logs <id>` to see if Flask says `Running on http://127.0.0.1:5000`.

**4. Kubernetes Pod enters CrashLoopBackOff**
- *Symptom*: `kubectl get pods` shows status `CrashLoopBackOff`.
- *Likely Cause*: Application crashes on startup (e.g., bad configuration, missing env var).
- *Check*: 
  - `kubectl describe pod <pod-name>` (look at Events).
  - `kubectl logs <pod-name>` (look at Python traceback).

**5. Prometheus target is DOWN**
- *Symptom*: Prometheus UI shows target status as DOWN.
- *Likely Cause*: Prometheus cannot reach the application network, or app is returning 500 on `/metrics`.
- *Check*: Verify network connectivity. Run `curl http://<target-ip>:5000/metrics` manually.

**6. Grafana shows "No Data"**
- *Symptom*: Panels are empty.
- *Likely Cause*: Wrong time range, wrong PromQL query, or Prometheus is not scraping correctly.
- *Check*: Change time range to "Last 5 minutes". Try the PromQL query directly in Prometheus UI.

---

## Important Viva Questions and Answers

**Q: What is the difference between Docker and Kubernetes?**
A: Docker is an engine to build and run individual containers. Kubernetes is an orchestration tool that manages multiple containers across multiple servers, handling scaling, healing, and networking.

**Q: Why do we need a CI/CD pipeline?**
A: To eliminate manual processes. It ensures code is automatically tested and deployed consistently, which speeds up delivery and reduces bugs.

**Q: What is the role of `kubectl apply`?**
A: It tells the Kubernetes API server to change the cluster's state to match what is defined in the YAML file.

**Q: How does Prometheus get metrics from our application?**
A: Prometheus uses a "pull" model. It periodically makes HTTP requests to our application's `/metrics` endpoint to scrape the data.

**Q: What happens if a Kubernetes pod crashes?**
A: The Deployment controller notices the actual replicas (e.g., 1) don't match the desired replicas (2). It will automatically schedule and start a new pod to replace the crashed one.

---

## Assumptions and Limitations

- **No Database**: To minimize failure points during the CIE, tasks are stored in memory. They will reset when the container restarts.
- **Local Jenkins**: The pipeline assumes Jenkins has access to the local Docker daemon and `kubectl` context.
- **Docker/K8s Environment**: Assumes a local cluster (like Minikube or Docker Desktop) is running for the `kubectl` and Docker commands to work directly on the host machine.
