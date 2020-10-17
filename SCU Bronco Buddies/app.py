from flask import Flask

app = Flask(__name__)

# users directed here upon login
@app.route('/')
def main():
    return render_template('index.html')