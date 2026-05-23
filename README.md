# Python Flask ML Demo Project with CI/CD

| 1. CI Status <br>(build and test) | 2. CD status <br>(docker build and push in DockerHub) | 3. CD Status <br>(AWS EC2 / AZURE - docker pull and run) |
| ---- | ---- | ---- |
| [![ci-build-python-app](https://github.com/matiaspakua/ml-demo-project/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/matiaspakua/ml-demo-project/actions/workflows/python-app.yml) | [![cd-build-publish-docker-image](https://github.com/matiaspakua/ml-demo-project/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/matiaspakua/ml-demo-project/actions/workflows/docker-image.yml) | [![run-docker-image](https://github.com/matiaspakua/ml-demo-project/actions/workflows/docker-run.yml/badge.svg?branch=main)](https://github.com/matiaspakua/ml-demo-project/actions/workflows/docker-run.yml) or [![cd-pull-and-run-docker-image-azure](https://github.com/matiaspakua/ml-demo-project/actions/workflows/deploy-azure.yml/badge.svg?branch=main)](https://github.com/matiaspakua/ml-demo-project/actions/workflows/deploy-azure.yml)|

![](https://github.com/matiaspakua/ml-demo-project/blob/6fc5d9fdc0420bba543e1fa9322527c45772c173/images/image_classificator.jpg)

## Project Overview

A Flask web application for real-time image classification using **MobileNetV2** and **MobileNetV3 Large**, lightweight convolutional neural networks pre-trained on ImageNet. Users upload a `.jpg` photo, select a model, and the server returns the top 3 predictions with confidence scores — all in under a second.

Built as part of the Duke University **Building Cloud Computing Solutions at Scale** specialization by Noah Gift.

- [Specialization on Coursera](https://www.coursera.org/specializations/building-cloud-computing-solutions-at-scale)
- [Personal study notes](https://matiaspakua.github.io/tech.notes.io/pages/general_topic/specialization_building_cloud_computing_solutions_at_scale.html)
- [MobileNetV2 on PyTorch Hub](https://pytorch.org/hub/pytorch_vision_mobilenet_v2/)
- [TensorFlow](https://www.tensorflow.org/)
- [Pre-trained Model Hub](https://www.kaggle.com/models?tfhub-redirect=true)

## Live App

| Provider | URL |
|----------|-----|
| Azure | [ml-demo.azurewebsites.net](https://ml-demo.azurewebsites.net/) |
| AWS EC2 | [ec2-34-207-152-164.compute-1.amazonaws.com:8080](http://ec2-34-207-152-164.compute-1.amazonaws.com:8080) |

## How It Works

The inference pipeline runs in 4 stages:

```
Upload → Preprocess → Model Inference → Results
```

| Step | Description |
|------|-------------|
| **Upload** | User selects a `.jpg` file via drag-and-drop or file picker |
| **Preprocess** | Image is resized to 224×224 and normalized with the selected model's `preprocess_input` |
| **Model** | MobileNetV2 (3.5M params, 71.8% top-1) or MobileNetV3 Large (5.4M params, 75.8% top-1) |
| **Results** | Top-3 predictions displayed with animated confidence bars and timing per stage |

Each stage's duration is measured and displayed on the results page.

### Model Selection

Users can switch between models via a dropdown on the landing page. Models are loaded lazily and cached after first inference. The selected model's details (name, params, accuracy) appear on the results page.

| Model | Parameters | Top-1 Accuracy | Preprocess Function |
|-------|-----------|----------------|-------------------|
| MobileNetV2 | 3.5M | 71.8% | `mobilenet_v2_preprocess_input` |
| MobileNetV3 Large | 5.4M | 75.8% | `mobilenet_v3_preprocess_input` |

## Run Locally

**Prerequisites:** Python 3.11 (TensorFlow does not support Python 3.12+)

```bash
# 1. Clone
git clone https://github.com/matiaspakua/ml-demo-project.git
cd ml-demo-project

# 2. Create virtual environment with Python 3.11
python3.11 -m venv .venv
source .venv/bin/activate

# 3. Install pinned dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open [http://localhost:8111](http://localhost:8111) in your browser.

## Project Structure

```
.
├── .github/workflows/       # CI/CD pipeline definitions
│   ├── python-app.yml       # Build, lint, format, test
│   ├── docker-image.yml     # Docker build and push to DockerHub
│   ├── docker-run.yml       # Deploy to AWS EC2
│   ├── deploy-azure.yml     # Deploy to Azure Container Instances
│   └── pages.yml            # Deploy landing page to GitHub Pages
├── src/                     # Application package
│   ├── __init__.py          # Package marker
│   ├── app.py               # Flask routes, model selection, error handling
│   ├── image_utils.py       # Image preprocessing, file validation
│   └── model_loader.py      # Model registry, lazy loading, decode dispatch
├── templates/
│   ├── view.html            # Landing page with model selector and architecture viz
│   └── result.html          # Results page with confidence bars and timing
├── tests/
│   ├── conftest.py          # Shared fixtures (Flask client, mock models, test images)
│   └── test_app.py          # 30 tests (home, prepare_image, allowed_file, registry, predict)
├── images/test/             # Sample images for acceptance testing
├── app.py                   # Entry point delegating to src.app
├── requirements.txt         # Pinned Python dependencies
├── Dockerfile               # Container image definition
└── locustfile.py            # Load testing with Locust
```

## Testing

The project uses **pytest** with 30 tests covering the full application:

```bash
python -m pytest -v tests/
```

Add `--html=report.html` for an HTML report.

### Test Coverage

| Test Class | Tests | Description |
|-----------|-------|-------------|
| `TestHomeEndpoint` | 5 | Status codes, content types, form elements, model selector |
| `TestPrepareImage` | 4 | Valid image, file-like object, invalid path, model name param |
| `TestAllowedFile` | 5 | Extension validation (.jpg, .JPG, .png, no ext, empty) |
| `TestModelRegistry` | 4 | Registry entries, model info lookup, unknown model error |
| `TestPredictEndpoint` | 12 | Valid prediction, HTML, model selection (V2, V3, unknown), missing file, wrong extension, corrupted file, empty filename, method not allowed |

The ML models are mocked in tests to avoid slow inference.

## Error Handling

| Scenario | Response |
|----------|----------|
| No file uploaded | 400 — "No image file provided." |
| Non-.jpg extension | 400 — "Only .jpg images are allowed." |
| Corrupted .jpg file | 400 — "The uploaded file is not a valid image." |
| Empty filename | 400 — "Only .jpg images are allowed." |
| GET request to /predict | 405 — Method Not Allowed |

Both client-side (JavaScript) and server-side validation is enforced.

## Deployment

The CI/CD pipeline consists of three chained GitHub Actions workflows:

1. **python-app.yml** — On push/PR to `main`: installs deps, lints with flake8, formats with black, runs pytest
2. **docker-image.yml** — On successful CI: builds Docker image and pushes to DockerHub
3. **docker-run.yml / deploy-azure.yml** — On successful Docker push: pulls and runs on AWS EC2 or Azure

The landing page is also deployed to **GitHub Pages** on every push.

## Load Testing

Using [Locust](https://locust.io/):

```bash
locust -f locustfile.py --host=http://localhost:8111
```

## Tech Stack

- **Python 3.11** — Runtime
- **Flask** — Web framework
- **TensorFlow / Keras** — MobileNetV2 and MobileNetV3 Large
- **Pillow** — Image handling
- **NumPy** — Array operations
- **pytest** — Testing framework
- **Docker** — Containerization
- **GitHub Actions** — CI/CD
