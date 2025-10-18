from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route("/user/<name>")
def user(name):
    if name.isdigit():
        return f"Enter only words"
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(debug=True)