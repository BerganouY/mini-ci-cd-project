# Mini CI/CD Project

This project is a simple web application that serves as a "welcome book." It demonstrates a complete CI/CD pipeline for automated testing and deployment to AWS, including Infrastructure as Code and automated machine image creation.

## Features

*   **User Authentication:** Users can sign up, log in, and log out.
*   **Message Board:** Authenticated users can post messages to a public board.
*   **Admin Panel:** Administrative users have the ability to view and delete any message.
*   **CI/CD Pipeline:** The project is configured with GitHub Actions for continuous integration and deployment.
*   **Infrastructure as Code (IaC):** The entire AWS infrastructure is defined and managed using CloudFormation templates.
*   **Automated AMI Baking:** The deployment pipeline is optimized to create a "golden AMI" after the first run, which significantly speeds up subsequent deployments.

## Tech Stack

*   **Backend:** Python, Flask, SQLAlchemy, PyMySQL
*   **Database:** MariaDB
*   **CI/CD:** GitHub Actions
*   **Infrastructure:** AWS (EC2, VPC, IAM, CloudFormation, Systems Manager)

## Project Structure

```
.
├── .github/              # GitHub Actions workflows
│   └── workflows/
│       ├── ci.yml        # Continuous Integration
│       └── deploy.yml    # Continuous Deployment
├── backend/              # Flask application code
│   ├── app/              # Main application module
│   ├── tests/            # Unit tests
│   └── ...
├── cloudformation/       # CloudFormation templates
│   ├── 0-prerequisites.yml
│   ├── 1-vpc-network.yml
│   ├── 2-security-groups.yml
│   ├── 3-iam-roles.yml
│   └── 4-compute.yml
└── database/             # Database initialization script
    └── init.sql
```

## Local Setup and Installation

To run the application locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd mini-ci-cd-project
    ```

2.  **Set up a Python virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file inside the `backend` directory. You can use the `backend/.env.example` file as a template. It should contain the following variables:
    ```
    SECRET_KEY=your_super_secret_key
    DATABASE_HOST=localhost
    DATABASE_USERNAME=your_db_user
    DATABASE_PASSWORD=your_db_password
    DATABASE_NAME=your_db_name
    ```

5.  **Run the application:**
    ```bash
    python backend/run.py
    ```

## Deployment

The deployment process is automated through the GitHub Actions workflow in `.github/workflows/deploy.yml`.

### Prerequisites

Before you can deploy, you must configure the following secrets in your GitHub repository's settings (`Settings` > `Secrets and variables` > `Actions`):

*   `AWS_ACCESS_KEY_ID`: Your AWS Access Key ID.
*   `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Access Key.
*   `EC2_SSH_PRIVATE_KEY`: The SSH private key for accessing the EC2 instances.
*   `SECRET_KEY`: A secret key for the Flask application.
*   `DATABASE_USERNAME`: The username for the database.
*   `DATABASE_PASSWORD`: The password for the database.
*   `DATABASE_NAME`: The name of the database.

### How to Deploy

The deployment workflow is triggered manually.

1.  Go to the **Actions** tab in your GitHub repository.
2.  Select the **Deploy Classic App** workflow.
3.  Click on **Run workflow**.
4.  You will be prompted to specify if this is the **first run**.

    *   **First Run (`true`):** If this is the very first time you are deploying, set the `first_run` input to `true`. This will execute the initial setup scripts on the EC2 instances. After the deployment, it will create a "golden AMI" for future runs.
    *   **Subsequent Runs (`false`):** For all subsequent deployments, set `first_run` to `false`. The pipeline will use the pre-baked AMI, resulting in a much faster deployment.

## CI/CD Pipeline

*   **Continuous Integration (`ci.yml`):** This workflow runs automatically on every push or pull request to the `main` branch. It performs linting on the code with `flake8` and runs the unit tests with `pytest`.
*   **Continuous Deployment (`deploy.yml`):** This workflow handles the deployment of the infrastructure and the application to AWS. It is triggered manually as described above.
