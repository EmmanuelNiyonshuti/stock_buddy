import click
from flask.cli import with_appcontext
import os
from dotenv import load_dotenv
from app.models.user import User
from app import db

load_dotenv()

@click.command(name="create_admin")
@with_appcontext
def create_admin():
    """
    Create an admin user.
    """
    admin = User.query.filter_by(username=os.getenv("ADMIN_USERNAME")).first()
    if not admin:
        admin = User(
            username=os.getenv("ADMIN_USERNAME"),
            email=os.getenv("ADMIN_EMAIL"),
            password=User.hash_password(os.getenv("ADMIN_PASSWORD")),
            role=userRole.ADMIN
        )
        db.session.add(admin)
        db.session.commit()
    click.echo("Admin user created or already exists.")

def register_commands(app):
    """
    Register custom commands with the Flask application.
    """
    app.cli.add_command(create_admin)
