---
title: Pii Redactor
emoji: 🕵️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8000
---

# PII Redactor Environment for OpenEnv

A reinforcement learning environment for redacting personally identifiable information (PII).

## Tasks

- **Easy**: Redact email addresses.
- **Medium**: Redact phone numbers and credit card numbers.
- **Hard**: Redact names and Social Security Numbers (SSNs) embedded in natural language.

## Reward Function

The reward is continuous (0.0 to 1.0):
- **1.0**: Perfect redaction.
- **Partial**: Rewards based on the number of correct redactions and penalizes for mismatches in non-PII parts of the text.

## Installation

```bash
# Install dependencies
pip install -r server/requirements.txt
pip install openenv-core
```

## Running the Server

```bash
python server/app.py
```

## Running Inference

```bash
# Set environment variables
export API_BASE_URL="http://localhost:8000"
export MODEL_NAME="gpt-3.5-turbo"
export API_KEY="your-api-key"

# Run inference
python inference.py
```

## Docker

Build and run the environment using Docker:

```bash
docker build -f server/Dockerfile -t pii-redactor-env .
docker run -p 8000:8000 pii-redactor-env
```

## Files

- `models.py`: Pydantic models for Action, Observation, and State.
- `server/environment.py`: Core logic for PII generation and reward calculation.
- `server/app.py`: FastAPI server implementation.
- `client.py`: HTTPEnvClient implementation.
- `inference.py`: Automated inference script with OpenEnv-compliant logging.
