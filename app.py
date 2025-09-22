from flask import Flask, request, jsonify, send_from_directory, render_template
from trade import stockCheck, stockInfo, checkCond, optionsData, pData, plotGraphW, fundDataAnnual, fundDataQuart, tecAnalysis
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

@app.route('/api/options', methods=['POST'])
def get_options():
    data = request.get_json()
    ticker = data
    calls, puts, callFig, putFig = optionsData(ticker)
    graphCall = json.loads(callFig.to_json())
    graphPut = json.loads(putFig.to_json())
    if calls is None or puts is None:
        print("No data found for ticker")
        return jsonify({"error": "No data found for ticker"})
    return jsonify({"calls": calls, "puts": puts, "callGraph": graphCall, "putGraph": graphPut})

@app.route('/api/earnings', methods=['POST'])
def get_earnings():
    data = request.get_json()
    ticker = data
    anEarnings = fundDataAnnual(ticker)
    quEarnings = fundDataQuart(ticker)
    if anEarnings is None and quEarnings is None:
        print("No data found for ticker")
        return jsonify({"error": "No data found for ticker"})
    return jsonify({"anEarnings": anEarnings, "quEarnings": quEarnings})

@app.route('/api/analysis', methods=['POST'])
def get_analysis():
    data = request.get_json()
    ticker = data['ticker']
    analysis, stockData = tecAnalysis(ticker)
    if analysis is None or stockData is None:
        print("No data found for ticker")
        return jsonify({"error": "No data found for ticker"})
    return jsonify({"analysis": analysis, "stockData": stockData})

@app.route('/')
def serve_frontend():
    return render_template('index.html')

@app.route('/puts.html')
def serve_puts():
    return render_template('puts.html')

@app.route('/calls.html')
def serve_calls():
    return render_template('calls.html')

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
