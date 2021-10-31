from flask import Flask

app = Flask(__name__)
app.env = "Development"

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
   app.run(debug=True)