from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')
@app.route('/api/message')
def get_message():
    return jsonify({"message": "Hello from the Python backend!"})
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)