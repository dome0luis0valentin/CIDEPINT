from src.web import create_app
from flask_mail import Mail


app = create_app()
mail = Mail(app)

if __name__ == '__name__':
    app.run(ssl_context="adhoc")
