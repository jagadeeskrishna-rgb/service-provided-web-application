# Service Provided Web Application Source

This Django application implements a role-based home service booking platform. Customers create service requests, providers accept and update jobs, and admin users monitor service categories, bookings, providers, feedback, and support tickets. Admin users can add, edit, remove, or deactivate service types, approve or block provider signup requests, reassign bookings, and resolve customer tickets. Providers can select multiple service types and upload photos while completing or cancelling work. Completed bookings require exactly one customer feedback entry.

## Quick Start

1. Create a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and update values.
4. Run `python manage.py migrate`.
5. Run `python manage.py seed_demo_data`.
6. Start the server with `python manage.py runserver`.

Demo users are created by the seed command and are documented in `documentation/SETUP_GUIDE.md`.
