 function enterTicker() {
        const ticker = document.getElementById("myTicker").value;
        console.log("Ticker entered:", ticker);
        createPlot('1Y');
        //getPrice()
        fetch('/api/message', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify(ticker)
            })
                .then(response => response.json())
                .then(data => {
                    console.log("Parsed data from server:", data); 
                    document.getElementById("companyName").innerText = data.message["Company Name"] + " (" + ticker.toUpperCase() + ")";
                    document.getElementById("currentPrice").innerText = data.message["Current Price"];
                    document.getElementById("sector").innerText = "Sector: " + data.message['Sector'];
                    document.getElementById("industry").innerText = "Industry: " + data.message['Industry'];
                    document.getElementById("marketCap").innerText = "Market Cap: " + data.message["Market Cap"];
                    const companyData = {
                        companyName: data.message["Company Name"],
                        currentPrice: data.message["Current Price"],
                        sector: data.message['Sector'],
                        industry: data.message['Industry'],
                        marketCap: data.message["Market Cap"]
                    };
                    localStorage.setItem('companyData', JSON.stringify(companyData));
                })
                .catch(error => console.error('Error:', error));
}


function createPlot(timeFrame){
    const stockBut = document.querySelector('.TimeFrame');
    const navB = document.querySelector('.navBar');
    const ticker = document.getElementById("myTicker").value;
    const stockData = {
        'ticker': ticker, 
        'timeFrame': timeFrame
    };
    fetch('/api/plot', {
        method: 'POST', 
        headers: {
             'Content-Type': 'application/json' 
        },
        body: JSON.stringify(stockData)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Parsed plot data from server:", data); 
            const plotDiv = document.getElementById('plot');
            if (data.data && data.layout) {
                data.layout.width = 1400;
                data.layout.height = 550;  
                stockBut.classList.remove('hidden');
                navB.classList.remove('hidden');
                 const plotData = {
                    ticker: ticker,
                    plotData: data.data,
                    plotLayout: data.layout
                };
                localStorage.setItem('plotData', JSON.stringify(plotData));
                Plotly.newPlot(plotDiv, data.data, data.layout);
            }
        })
        .catch(error => console.error('Error:', error));
 }

window.onload = function() {
    const companyData = localStorage.getItem('companyData');
    const plotData = localStorage.getItem('plotData');
    
    if (companyData && plotData) {
        const pData = JSON.parse(plotData);
        const cData = JSON.parse(companyData);
        console.log("Retrieved stock data for:", cData.companyName);
        console.log("Retrieved ticker:", pData.ticker);
        document.getElementById('myTicker').value = pData.ticker;
        createPlot('ALL');
        enterTicker();
    }
};

