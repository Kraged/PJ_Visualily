from flask import Flask, render_template
from programs.home import home_bp # Import the blueprint object
from programs.playground import playground_bp

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(playground_bp)

@app.route('/')
def home():
    return render_template('index.html', myvar='Be motivate!!!')

if __name__ == '__main__':
    app.run(debug=True)