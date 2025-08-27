# CozaStore - Django E-commerce Platform

This project is an advanced e-commerce web application built with Django and MongoDB, developed as a comprehensive software engineering assignment. It features a modular architecture, CI/CD integration, and modern development practices.

## Technology Stack

*   **Backend:** Python, Django
*   **Database:** MongoDB (with Djongo)
*   **API:** Django Rest Framework
*   **Frontend:** HTML, CSS, JavaScript (from CozaStore Template)
*   **Testing:** PyTest, Selenium, Apache JMeter, OWASP ZAP
*   **CI/CD:** GitHub Actions
*   **Containerization:** Docker, Kubernetes

## Project Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YourUsername/django-ecommerce-project.git
    cd django-ecommerce-project
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your database:**
    *   Update the `DATABASES` setting in `ecommerce/settings.py` with your MongoDB connection details.

5.  **Run migrations and start the server:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

    