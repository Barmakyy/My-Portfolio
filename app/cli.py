import click
from flask.cli import with_appcontext
from app.models import User
from app import db

@click.command('create-admin')
@click.argument('username')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_admin(username, email, password):
    """Create an admin user."""
    if User.query.filter_by(username=username).first():
        click.echo('Error: Username already exists.')
        return
    if User.query.filter_by(email=email).first():
        click.echo('Error: Email already exists.')
        return
    
    admin = User(username=username, email=email, is_admin=True)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    click.echo(f'Admin user {username} created successfully!') 