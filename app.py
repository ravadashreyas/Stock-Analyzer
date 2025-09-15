from flask import Flask, request, jsonify, send_from_directory, render_template
from trade import getTicker, stockCheck, stockInfo, sortData, checkCond, optionsData, pData, plotGraphW, fundData

app = Flask(__name__, static_folder='static')
@app.route('/api/message', methods=['POST'])
def get_message():
    ticker = request.get_json()
    return jsonify({"message": pData(ticker)})

@app.route('/api/plot', methods=['POST'])
def get_plot():
    data = request.get_json()
    ticker = data.get('ticker')
    timeFrame = data.get('timeFrame')
    fig = plotGraphW(ticker, timeFrame)
    if fig is None:
        return jsonify({"error": "No data found for ticker"})
    graphJSON = fig.to_json()
    return graphJSON  


@app.route('/')
def serve_frontend():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)