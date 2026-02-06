from flask import Blueprint, request, jsonify, session
import json
from methods.trade import pData
from methods.plot_main import plotGraphW
from methods.options import optionsData
from methods.earnings import fundDataAnnual, fundDataQuart
from methods.technical_analysis import tecAnalysis 
from methods.add_stock import add_equity
from methods.Get_Functions.get_portfolio import get_user_holdings
from methods.portfolio_value import get_user_equity
    
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
    if callFig is not None and putFig is not None:
        graphCall = json.loads(callFig.to_json())
        graphPut = json.loads(putFig.to_json())
    if calls is None or puts is None:
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
    analysis = tecAnalysis(ticker)
    if analysis is None:
        print("No data found for ticker")
        return jsonify({"error": "No data found for ticker"})
    return jsonify({"analysis": analysis})

@api_bp.route('/buyTrade', methods=['POST'])
def add_to_db():
    data = request.get_json()
    user_id = session.get('user_id')
    ticker = data['ticker']
    number_of_shares = data['number_of_shares']
    date_purchased = data["date_purchased"]
    if add_equity(user_id, ticker, number_of_shares, date_purchased) == False:
        return jsonify({"error": "Invalid Input"})
    return jsonify({"Result": "Successful Trade"})

@api_bp.route('/sellTrade', methods=['POST'])
def remove_from_db():
    data = request.get_json()
    user_id = session.get('user_id')
    ticker = data['ticker']
    number_of_shares = data['number_of_shares']
    if add_equity(user_id, ticker, number_of_shares) == False:
        return jsonify({"error": "Invalid Input"})
    return jsonify({"Result": "Successful Trade"})

@api_bp.route('/portfolio', methods=['GET'])
def get_portfolio():
    user_id = session.get('user_id')
    holdings = get_user_holdings(user_id)
    return jsonify(holdings)

@api_bp.route('/portfolioPlot', methods=['POST'])
def get_portfolioPlot():
    user_id = session.get('user_id')
    data = request.get_json() or {}
    time_frame = data.get('timeFrame', '3M')
    plot = get_user_equity(user_id, time_frame)
    return jsonify(plot)

