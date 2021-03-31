from flask import Flask
from flask import send_file, send_from_directory, safe_join, abort
app = Flask(__name__)


@app.route('/files/seen.txt')
def hello():
    return send_file("seen.txt", as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port =6969)