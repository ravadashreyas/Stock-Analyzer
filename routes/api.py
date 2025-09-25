from flask import Blueprint, request, jsonify
import json
from trade import pData, plotGraphW, optionsData, fundDataAnnual, fundDataQuart, tecAnalysis
from .utils.helpers import create_response, get_ticker_from_json

api_bp = Blueprint('api', __name__)

@api_bp.route('/message', methods=['POST'])
def get_message():
    ticker = request.get_json()
    return jsonify({"message": pData(ticker)})

@api_bp.route('/plot', methods=['POST'])
def get_plot():
    data = request.get_json()
    ticker = data.get('ticker')
    timeFrame = data.get('timeFrame')
    fig = plotGraphW(ticker, timeFrame)
    if fig is None:
        return jsonify({"error": "No data found for ticker"})
    graphJSON = json.loads(fig.to_json())
    return jsonify(graphJSON) 

@api_bp.route('/options', methods=['POST'])
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

@api_bp.route('/earnings', methods=['POST'])
def get_earnings():
    data = request.get_json()
    ticker = data
    anEarnings = fundDataAnnual(ticker)
    quEarnings = fundDataQuart(ticker)
    if anEarnings is None and quEarnings is None:
        print("No data found for ticker")
        return jsonify({"error": "No data found for ticker"})
    return jsonify({"anEarnings": anEarnings, "quEarnings": quEarnings})

@api_bp.route('/analysis', methods=['POST'])
def get_analysis():
    data = request.get_json()
    ticker = data['ticker']
    analysis, stockData = tecAnalysis(ticker)
    if analysis is None or stockData is None:
        print("No data found for ticker")
        return jsonify({"error": "No data found for ticker"})
    return jsonify({"analysis": analysis, "stockData": stockData})