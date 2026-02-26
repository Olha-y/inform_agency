# Inform Agency

Inform Agency is a Django-based web application designed to help
track editor activity, manage newspapers, and analyze publication workload.

Access to the system is available only for authenticated editors.
All authorized users can view and manage information through a unified dashboard.

---

## Technology Stack

- Python 3.10+
- Django 4+
- Bootstrap 5
- HTML / CSS

---

## Functionality

- authentication
- Editor activity tracking and workload analysis
- Newspapers and topics management
- Search, create, update, and filter publications
- Responsive UI built with Bootstrap 5

---

## Installation

This project uses pip as a package manager.

### Create and activate a virtual environment

If you are using PyCharm, it may automatically suggest creating a virtual
environment and installing dependencies.

Otherwise, create it manually:
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)

___

### Install dependencies
pip install -r requirements.txt

___

### Apply migrations and run the server
python manage.py migrate
python manage.py runserver




![ER Diagram](docs/tracking_system_diagram.png)

