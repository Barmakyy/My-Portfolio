# Personal Portfolio Website with Admin CMS

A modern, responsive personal portfolio website built with Flask, featuring a built-in admin CMS dashboard.

## Features

### Public Website

- Homepage with about section, featured projects, and CTA
- Projects page with grid/list view
- Blog page with post previews and full post views
- Contact form with database storage

### Admin CMS Dashboard

- Protected admin route with login
- CRUD operations for projects and blog posts
- Contact message management
- Image upload support
- User role management

## Tech Stack

- Backend: Flask, SQLAlchemy
- Frontend: HTML, CSS (Bootstrap), JavaScript
- Database: SQLite (configurable for PostgreSQL)
- Authentication: Flask-Login
- Forms: Flask-WTF
- File Upload: Werkzeug

## Setup Instructions

1. Clone the repository:

```bash
git clone <repository-url>
cd portfolio
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:

```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///portfolio.db
UPLOAD_FOLDER=app/static/uploads
```

5. Initialize the database:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Create an admin user:

```bash
flask shell
>>> from app import db
>>> from app.models import User
>>> admin = User(username='admin', email='admin@example.com', is_admin=True)
>>> admin.set_password('your-password')
>>> db.session.add(admin)
>>> db.session.commit()
```

7. Run the development server:

```bash
flask run
```

The website will be available at `http://localhost:5000`
Admin dashboard: `http://localhost:5000/admin`

## Project Structure

```
portfolio/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── main/
│   ├── auth/
│   ├── admin/
│   ├── static/
│   └── templates/
├── migrations/
├── venv/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Deployment

1. Set up a production database (e.g., PostgreSQL)
2. Update the `.env` file with production settings
3. Set up a production WSGI server (e.g., Gunicorn)
4. Configure a reverse proxy (e.g., Nginx)
5. Set up SSL certificates
6. Deploy static files to a CDN (optional)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
