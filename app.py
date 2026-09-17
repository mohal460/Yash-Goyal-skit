from flask import Flask, render_template, redirect, url_for, session
from database import db
import os

def create_app():
    # Setup Flask and point it to your templates/static folders
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'super-secret-key-for-hackathon'
    
    # Configure SQLite database inside the 'instance' folder
    os.makedirs('instance', exist_ok=True)
    db_path = os.path.join(os.getcwd(), 'instance', 'cafe_rewards.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import Blueprints (API Routes)
    from routes.auth import auth_bp
    from routes.members import members_bp
    from routes.purchases import purchases_bp
    from routes.redemptions import redemptions_bp

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(members_bp, url_prefix='/api/members')
    app.register_blueprint(purchases_bp, url_prefix='/api/purchases')
    app.register_blueprint(redemptions_bp, url_prefix='/api/redemptions')

    # Create tables automatically
    with app.app_context():
        db.create_all()

    # --- HTML PAGE ROUTES ---
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/register')
    def register_page():
        return render_template('register.html')

    @app.route('/dashboard')
    def dashboard_page():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return render_template('dashboard.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)