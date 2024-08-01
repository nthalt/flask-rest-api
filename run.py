from flask.cli import FlaskGroup
from app import create_app, db
from app.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

@cli.command("create_admin")
def create_admin():
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    first_name = input("Enter admin first name: ")
    last_name = input("Enter admin last name: ")
    
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        role='Admin',
        is_active=True
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print(f"Admin user {username} created successfully.")

if __name__ == '__main__':
    cli()