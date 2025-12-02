# Detailed Project Documentation

This document provides a comprehensive explanation of the Mini CI/CD project, its architecture, components, and how to operate it.

## 1. High-Level Overview

This project is a simple "welcome book" web application built with Flask. Its primary purpose is to demonstrate a complete and automated CI/CD pipeline that deploys the application to a realistic cloud environment on AWS.

The architecture consists of:
*   A **web server** running the Flask application, publicly accessible.
*   A **database server** running MariaDB in a private network, only accessible from the web server.
*   A **CI/CD pipeline** built with GitHub Actions that automates testing, infrastructure provisioning, and application deployment.

## 2. Application Backend

The backend is a standard Flask application with the following structure:

*   `app/`: The main application package.
    *   `__init__.py`: Initializes the Flask app, extensions (SQLAlchemy, LoginManager), and loads configuration from environment variables.
    *   `models.py`: Defines the database models (`User`, `Message`) using Flask-SQLAlchemy.
    *   `routes.py`: Contains the application's routes and view logic (e.g., signup, login, index, message posting).
    *   `forms.py`: Defines the application's forms (e.g., signup, login, message) using Flask-WTF.
*   `run.py`: The entry point for the application, used by Gunicorn to start the app. It also contains logic to initialize the database tables.
*   `requirements.txt`: Lists the Python dependencies for the project.

## 3. Infrastructure as Code (IaC)

The entire AWS infrastructure is managed using CloudFormation templates located in the `cloudformation/` directory. The infrastructure is modular and deployed in layers.

*   **`0-prerequisites.yml`**:
    *   Creates an AWS Systems Manager (SSM) Parameter to store the ID of the latest golden AMI. This allows the compute stack to dynamically use the most up-to-date machine image.

*   **`1-vpc-network.yml`**:
    *   **VPC**: Creates a Virtual Private Cloud (VPC) to provide a logically isolated network for the resources.
    *   **Subnets**: Creates a public subnet (for the web server) and a private subnet (for the database server).
    *   **Internet Gateway**: Allows resources in the public subnet to access the internet.
    *   **NAT Gateway**: Allows resources in the private subnet (the database server) to access the internet for software updates, while remaining inaccessible from the public internet.
    *   **Route Tables**: Configures routing for the public and private subnets.

*   **`2-security-groups.yml`**:
    *   **WebSecurityGroup**: A firewall for the web server. It allows incoming HTTP traffic (port 80) and SSH traffic (port 22) from the internet.
    *   **DBSecurityGroup**: A firewall for the database server. It allows incoming MySQL traffic (port 3306) and SSH traffic (port 22) **only** from the `WebSecurityGroup`. This is a critical security measure that prevents direct access to the database from the internet.

*   **`3-iam-roles.yml`**:
    *   Creates an IAM Role and an Instance Profile for the EC2 instances. This role grants the instances permissions to interact with other AWS services, such as CloudWatch for logging and monitoring.

*   **`4-compute.yml`**:
    *   **EC2 Instances**: Creates the `WebAppInstance` and `DBInstance`.
    *   It uses the `{{resolve:ssm:/mini-ci-cd/latest-ami-id}}` dynamic reference to get the AMI ID from the SSM parameter.
    *   **UserData**: The template contains `UserData` scripts that run when an instance is first created.
        *   The web server's script installs Python, Nginx, and other dependencies.
        *   The database server's script installs and configures MariaDB.

## 4. CI/CD Pipeline

The project uses GitHub Actions for CI/CD. The workflows are defined in the `.github/workflows/` directory.

### Continuous Integration (`ci.yml`)

*   **Trigger**: Runs on every `push` and `pull_request` to the `main` branch.
*   **Jobs**:
    *   `build-and-test`:
        1.  Checks out the code.
        2.  Sets up a Python environment.
        3.  **Caches** pip dependencies to speed up subsequent runs.
        4.  Installs the project dependencies.
        5.  **Lints** the code with `flake8` to check for style and syntax errors.
        6.  **Runs** the unit tests with `pytest`.

### Continuous Deployment (`deploy.yml`)

This is the main workflow for deploying the application.

*   **Trigger**: Manually triggered via the GitHub Actions UI (`workflow_dispatch`). It takes a boolean input `first_run`.
*   **Jobs**:
    *   `deploy`:
        1.  **Configure AWS Credentials**: Uses the secrets stored in the GitHub repository to configure access to AWS.
        2.  **Deploy Infrastructure**: Deploys the CloudFormation stacks in the correct order: prerequisites, network, security, IAM roles, and finally compute. The workflow is designed to handle updates to existing stacks and to recover from `ROLLBACK_COMPLETE` states by deleting and recreating the failed stack.
        3.  **Get Infrastructure IPs**: Retrieves the public IP of the web server and the private IP of the database server from the CloudFormation stack outputs.
        4.  **Deploy Code via SSH**: This is the core application deployment step. It connects to the web server via SSH and runs a script that:
            *   Clones or updates the application code from the Git repository.
            *   Sets up the Python virtual environment and installs dependencies.
            *   Creates the `.env` file with the secrets passed from the GitHub workflow.
            *   **Initializes the database**: It substitutes the placeholders in `database/init.sql` with the real username and password and runs the script using the `root` user and the `DB_ROOT_PASSWORD`.
            *   Configures and restarts the `gunicorn` and `nginx` services.
        5.  **Bake AMI**: If the `first_run` parameter is `true`, this step creates a new "golden AMI" from the freshly configured web server instance and stores its ID in the SSM parameter for future deployments.

## 5. Deployment and Operational Guide

### Initial Deployment

1.  **Create an EC2 Key Pair** in the `us-east-1` region named `mini-project-key`.
2.  **Find the latest Ubuntu 24.04 AMI ID** for `us-east-1` and update the `cloudformation/0-prerequisites.yml` file.
3.  **Create the required GitHub secrets**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `EC2_SSH_PRIVATE_KEY`, `SECRET_KEY`, `DATABASE_USERNAME`, `DATABASE_PASSWORD`, and `DB_ROOT_PASSWORD`.
4.  **Run the `Deploy Classic App` workflow** with `first_run` set to `true`.

### Subsequent Deployments

For any subsequent code changes, run the `Deploy Classic App` workflow with `first_run` set to `false`. The pipeline will use the pre-baked AMI and will be much faster.

### Debugging via SSH

You can connect to the web server instance using the `mini-project-key.pem` file and the public IP address of the instance.
```bash
ssh -i /path/to/your/mini-project-key.pem ubuntu@<public-ip-address>
```
Once on the instance, you can check the application logs with:
```bash
sudo journalctl -u app.service
```

## 6. Troubleshooting

*   **CloudFormation Failures**: Check the `StackEvents` in the AWS CloudFormation console for the failed stack to get a detailed error message. Common issues include invalid AMI IDs or incorrect IAM permissions.
*   **502 Bad Gateway**: This usually means the Gunicorn application is not running correctly. SSH into the web server and check the application logs with `sudo journalctl -u app.service` to find the root cause.
*   **Database Connection Errors**: If the application cannot connect to the database, ensure that the security groups are correctly configured and that the database user has the correct permissions. The automated database initialization in the deployment workflow should handle this, but if you have made manual changes, this can be a source of errors.
