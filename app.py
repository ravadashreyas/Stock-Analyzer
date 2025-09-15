from flask import Flask, request, jsonify, send_from_directory, render_template
from trade import getTicker, stockCheck, stockInfo, sortData, checkCond, optionsData, pData, plotGraphW, fundData
import json

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
    graphJSON = json.loads(fig.to_json())
    return jsonify(graphJSON) 



@app.route('/')
def serve_frontend():
    return render_template('index.html')

@app.route('/options.html')
def serve_options():
    return render_template('options.html')

@app.route('/earnings.html')
def serve_earnings():
    return render_template('earnings.html')

@app.route('/news.html')
def serve_news():
    return render_template('news.html')

@app.route('/financials.html')
def serve_financials():
    return render_template('financials.html')

@app.route('/analysis.html')
def serve_analysis():
    return render_template('analysis.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
