# Felicit App

This is a simple Flask web application that serves as a guestbook or "welcome book".

## Features

-   **User Authentication**: Users can sign up, log in, and log out.
-   **Post Messages**: Authenticated users can post messages.
-   **User Roles and Permissions**:
    -   **Normal User**: Can post only one message.
    -   **Special User (ID=2)**: Can post multiple messages and include their first and last name.
    -   **Admin User**: Can view all messages and delete any message. Admins cannot post messages.

## Technologies Used

-   **Backend**:
    -   Python
    -   Flask
    -   Flask-SQLAlchemy (for database interaction)
    -   Flask-Login (for handling user sessions)
    -   Flask-WTF (for forms)
-   **Database**:
    -   MariaDB
-   **Frontend**:
    -   HTML
    -   Jinja2 (template engine)

## Usage

1.  **Create a `.env` file**:

    Create a `.env` file in the root of the project and add the following environment variables:

    ```
    DATABASE_USERNAME=carnet_user
    DATABASE_PASSWORD=admin123
    DATABASE_HOST=db
    DATABASE_NAME=carnet_db
    ```

2.  **Run with Docker Compose**:

    ```bash
    docker-compose up -d --build
    ```

3.  **Access the application**:

    Open your web browser and go to `http://127.0.0.1:5000`.

## Docker Compose

1.  **Run with Docker Compose**:
    ```bash
    docker-compose up -d
    ```

## Docker

1.  **Build the Docker image**:
    ```bash
    docker build -t felicit-app .
    ```

2.  **Run the Docker container**:
    ```bash
    docker run -p 5000:5000 felicit-app
    ```

## Folder Structure

```
/home/yabe/PycharmProjects/felicit_app/
├───run.py                # Main entry point of the application
├───app/                  # Application package
│   ├───__init__.py       # Application factory and configuration
│   ├───forms.py          # WTForms for handling forms
│   ├───models.py         # SQLAlchemy database models
│   ├───routes.py         # Application routes
│   └───templates/        # HTML templates
│       ├───base.html
│       ├───index.html
│       ├───login.html
│       └───signup.html
├───instance/

└───static/               # Static files (CSS, JavaScript, images)
```
