# customer-service - Standard Python Application

A simple ready-to-run Python REST-style Customer Service API for the
AI Cloud Delivery assessment.

## Application details

- Application name: customer-service
- Language: Python
- Framework/dependencies: Python standard library only
- Port: 8080
- External database: None
- Container/cloud deployment: Not included; this project is intended for the simulated deployment assessment

## Project structure

customer-service/
├── app.py
├── requirements.txt
├── README.md
├── run.bat
└── venv/

## Run on Windows

Open PowerShell or Command Prompt in the project folder.

### Option 1 - Use the included virtual environment

PowerShell:

    .\venv\Scripts\Activate.ps1
    python app.py

Command Prompt:

    venv\Scripts\activate.bat
    python app.py

If PowerShell blocks activation, run:

    .\venv\Scripts\python.exe app.py

## If the included venv cannot run

A Python virtual environment is platform-specific. If you move this ZIP to
another operating system or Python installation, recreate the venv:

    python -m venv venv
    venv\Scripts\python.exe -m pip install -r requirements.txt
    venv\Scripts\python.exe app.py

There are no third-party packages to download for this application.

## Test the application

Open in a browser:

    http://localhost:8080/

Health check:

    http://localhost:8080/health

Get all customers:

    http://localhost:8080/customers

Get one customer:

    http://localhost:8080/customers/1

## Create a customer

POST:

    http://localhost:8080/customers

JSON:

    {
      "name": "Amit",
      "email": "amit@example.com"
    }

## Why this application is suitable for the assignment

The application is intentionally small so freshers can focus on:

1. Understanding application deployment requirements
2. Asking AI to suggest deployment configuration
3. Generating Kubernetes Deployment YAML
4. Generating Kubernetes Service YAML
5. Reviewing configuration
6. Finding configuration issues
7. Troubleshooting a port mismatch
8. Validating the AI recommendation

Docker, Kubernetes, kubectl and a cloud account are not required for
the simulated assessment.

## Important

Do not claim that the application was deployed to Kubernetes or the cloud.
The assignment is a simulation unless those environments are actually used.
