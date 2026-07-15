# Deploying ML Model using Flask — with CI/CD (GitHub Actions + Docker)

This is a simple project demonstrating how to deploy a Machine Learning model using a Flask API — extended with automated testing, containerization, and a full CI/CD pipeline using GitHub Actions and Docker.

Forked from [MaajidKhan/DeployMLModel-Flask](https://github.com/MaajidKhan/DeployMLModel-Flask).

## What's New in This Fork

- Upgraded dependencies (Flask, scikit-learn, pandas, numpy) to modern, non-conflicting versions
- Added `gunicorn` as a production WSGI server
- Added automated model tests with `pytest`
- Added a production-ready `Dockerfile`
- Added a GitHub Actions CI/CD pipeline that tests, builds, and pushes a Docker image to Docker Hub on every push to `master`

## Prerequisites

- Python 3.11+
- pip
- Docker (optional, for containerized runs)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

This project has the following major parts:

1. **`model.py`** — Trains a Linear Regression model to predict employee salaries based on training data in `hiring.csv`, and serializes it to `model.pkl`.
2. **`application.py`** — Contains the Flask API that receives employee details through the GUI or API calls, computes the predicted value using the model, and returns it.
3. **`test_model.py`** — Automated `pytest` tests that validate the trained model produces sane, positive, in-range salary predictions.
4. **`templates/`** — Contains the HTML template (`index.html`) for user input and displaying predictions.
5. **`static/css/`** — Contains `style.css` for styling `index.html`.
6. **`Dockerfile`** — Builds a production image: installs dependencies, trains the model at build time, and serves the app with Gunicorn.
7. **`.github/workflows/mlops-pipeline.yml`** — GitHub Actions workflow with two jobs: CI (test & validate) and CD (build & push Docker image).

## Running the Project Locally

1. Ensure you're in the project home directory and your virtual environment is active. Create the machine learning model:
```bash
   python model.py
```
   This generates a serialized model file, `model.pkl`.

2. Run the automated tests to validate the model:
```bash
   pytest test_model.py -v
```

3. Start the Flask API:
```bash
   python application.py
```
   By default, Flask runs on port 5000.

4. Navigate to `http://127.0.0.1:5000/` (or `http://localhost:5000`).

   Enter valid numerical values in all 3 input boxes and hit **Predict**. You should see the predicted salary on the page. The prediction endpoint is also reachable at `http://127.0.0.1:5000/predict`.

## Running with Docker

Build and run the containerized app (Gunicorn-served, model trained at build time):

```bash
docker build -t deployml-flask:local .
docker run -p 5000:5000 deployml-flask:local
```

Visit `http://localhost:5000`.

Or pull the image already published by CI/CD:

```bash
docker pull <your-dockerhub-username>/deployml-flask:latest
docker run -p 5000:5000 <your-dockerhub-username>/deployml-flask:latest
```

## CI/CD Pipeline

Every push/PR to `master` triggers `.github/workflows/mlops-pipeline.yml`:

- **CI — Test & Validate**: installs dependencies, trains the model, runs `pytest`, and lints the code with `flake8`.
- **CD — Build & Release** *(runs only after CI passes, and only on pushes)*: logs in to Docker Hub, builds the image, and pushes it tagged both `:latest` and with the commit SHA.

Required repository secrets (**Settings → Secrets and variables → Actions**):

| Secret | Description |
|---|---|
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub access token |

You can monitor pipeline runs under the **Actions** tab of this repository.

## License

MIT — see [LICENSE](LICENSE).
