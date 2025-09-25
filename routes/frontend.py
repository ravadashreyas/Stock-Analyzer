from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def serve_frontend():
    return render_template('index.html')

@frontend_bp.route('/puts.html')
def serve_puts():
    return render_template('puts.html')

@frontend_bp.route('/calls.html')
def serve_calls():
    return render_template('calls.html')

@frontend_bp.route('/earnings.html')
def serve_earnings():
    return render_template('earnings.html')

@frontend_bp.route('/news.html')
def serve_news():
    return render_template('news.html')

@frontend_bp.route('/financials.html')
def serve_financials():
    return render_template('financials.html')

@frontend_bp.route('/analysis.html')
def serve_analysis():
    return render_template('analysis.html')