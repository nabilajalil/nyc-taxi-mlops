# NYC Taxi Trip Duration — Six-Module MLOps Portfolio Project

This project follows all six MLOps Zoomcamp modules: introduction/modeling, experiment tracking, orchestration, deployment, monitoring, and engineering best practices.

## Requirements
Linux, Python 3.11, Docker and Docker Compose (optional), and sufficient RAM for training. An AWS account is optional and incurs charges. Commands below run from the repository root.

## 1. Install
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Download data and compare three models (Modules 1–2)
```bash
bash scripts/download_data.sh
python -m src.train_compare
bash scripts/run_mlflow.sh
```
Open MLflow at http://127.0.0.1:5000. Ridge, Random Forest, and HistGradientBoosting runs are logged. The lowest February validation RMSE wins; `models/taxi_model.joblib` is exported for the API. Models train on bounded random samples by default to keep the demo feasible on a laptop. Never claim these sample results are production-grade.

## 3. Evaluate untouched March holdout
```bash
bash scripts/download_test_data.sh
python scripts/evaluate_test.py
```
Do not tune hyperparameters using March scores. March is a one-time independent check, not a guarantee of production quality.

## 4. Orchestrate training (Module 3)
```bash
python -m pipelines.training_flow
```
This is a local Prefect flow with tasks, retries and observable runs. To schedule recurring execution, configure a Prefect deployment and worker for your chosen infrastructure; this demo does not enable an unattended schedule by default.

## 5. Serve and deploy (Module 4)
```bash
bash scripts/run_local.sh
bash scripts/test_api.sh
```
UI: http://localhost:8000. Health: `/health`. API: `POST /predict` with JSON `PULocationID`, `DOLocationID`, `pickup_hour`, `day_of_week`. Gunicorn serves the Flask app. To containerize after training:
```bash
docker build -t nyc-taxi-mlops .
docker run --rm -p 8000:8000 nyc-taxi-mlops
```
Or start API + Prometheus + Grafana:
```bash
docker compose up --build
```
Prometheus: http://localhost:9090; Grafana: http://localhost:3000 (configure a Prometheus data source pointing to `http://prometheus:9090`). **Change default Grafana credentials** before exposing it. Do not publicly expose Grafana or Prometheus. `docker-compose.yml` is intended for localhost development only.

## 6. Monitor (Module 5)
```bash
python -m monitoring.drift_report
```
Creates `reports/drift.html` comparing January and February feature distributions. The API exposes `/metrics` for Prometheus, with request counts and inference latency. **Feature drift is not model accuracy**; accurate performance monitoring requires delayed ground-truth trip durations. This is a historical drift demonstration, not a live feedback loop.

## 7. Test, CI, Terraform (Module 6)
```bash
pytest -q
python -m compileall -q src app pipelines monitoring
terraform -chdir=infra init
terraform -chdir=infra plan -var='ami_id=ami-REPLACE' -var='ssh_public_key=ssh-ed25519 REPLACE' -var='allowed_ssh_cidr=YOUR_IP/32'
```
The GitHub Actions workflow runs compile and pytest checks. Terraform provisions an EC2 instance and security group; **it does not deploy Docker automatically**. Supply a real regional Ubuntu AMI and your own SSH key, inspect plan and cost, and run `terraform destroy` after testing. For a public service, add HTTPS/reverse proxy, authentication/rate limits, secrets management, and security hardening. The exposed demo port 8000 is not recommended for production.

## Caveats
- The dataset downloads at first use; no raw data or trained model is bundled.
- `joblib` models are trusted local artifacts; never load untrusted model files.
- Prediction inputs are taxi zone IDs, hour and weekday, with no post-trip information.
- The train/validation split is Jan/Feb 2023, with March 2023 as untouched holdout.
- No automatic model registry promotion, auto-retraining trigger, continuous delivery, or real-time labeled performance monitoring is implemented. Those are future extensions, not claims for a CV.
