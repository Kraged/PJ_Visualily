from flask import Blueprint, render_template

# 1. Define the blueprint
home_bp = Blueprint('home_bp', __name__, template_folder='../templates')

# 2. Define the route
@home_bp.route('/Home')
def display_home():
    # This looks for Home.html inside your templates folder
    return render_template('Home.html')