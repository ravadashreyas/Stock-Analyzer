import yfinance as yf
import numpy as np

def fundDataQuart(ticker):
    stock = yf.Ticker(ticker)
    anEarnings = stock.quarterly_income_stmt

    if anEarnings is None or anEarnings.empty:
        print(f"No income statement data found for {ticker}.")
        return None

    anEarnings = anEarnings.transpose()
    anEarnings.dropna(how='all', inplace=True)
    anEarnings.reset_index(inplace=True)
    anEarnings = anEarnings.replace({np.nan: None})
    anEarnings = anEarnings.rename(columns={
        'index': 'date', 
        'Total Revenue': 'totalRevenue',
        'Gross Profit': 'grossProfit',
        'Normalized EBITDA': 'normalEBITDA',
        'Net Income': 'netIncome',
        'Diluted EPS': 'dilutedEPS',
        'Total Expenses': 'totalExpenses',
        'Operating Income': 'operatingIncome'
    })
   
    anEarnings['date'] = anEarnings['date'].dt.strftime('%Y-%m-%d')
    anEarningsJSON = anEarnings.to_dict(orient='records')
    
    return anEarningsJSON

def fundDataAnnual(ticker):
    stock = yf.Ticker(ticker)
    anEarnings = stock.income_stmt

    if anEarnings is None or anEarnings.empty:
        print(f"No income statement data found for {ticker}.")
        return None

    anEarnings = anEarnings.transpose()
    anEarnings.dropna(how='all', inplace=True)
    anEarnings.reset_index(inplace=True)
    anEarnings = anEarnings.replace({np.nan: None})
    anEarnings = anEarnings.rename(columns={
        'index': 'date', 
        'Total Revenue': 'totalRevenue',
        'Gross Profit': 'grossProfit',
        'Normalized EBITDA': 'normalEBITDA',
        'Net Income': 'netIncome',
        'Diluted EPS': 'dilutedEPS',
        'Total Expenses': 'totalExpenses',
        'Operating Income': 'operatingIncome'
    })
   
    anEarnings['date'] = anEarnings['date'].dt.strftime('%Y-%m-%d')
    anEarningsJSON = anEarnings.to_dict(orient='records')
    
    return anEarningsJSON