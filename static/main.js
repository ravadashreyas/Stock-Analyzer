 function enterTicker() {
        const ticker = document.getElementById("myTicker").value;
        console.log("Ticker entered:", ticker);

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
                    document.getElementById("companyName").innerText = "Company Name: " + data.message["Company Name"];
                    document.getElementById("sector").innerText = "Sector: " + data.message['Sector'];
                    document.getElementById("industry").innerText = "Industry: " + data.message['Industry'];
                    document.getElementById("marketCap").innerText = "Market Cap: " + data.message["Market Cap"];
                })
                .catch(error => console.error('Error:', error));
        }
 function createPlot(timeFrame){
    const stockBut = document.querySelector('.TimeFrame');
    stockBut.classList.remove('hidden');
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
            Plotly.newPlot(plotDiv, data.data, data.layout);
            }
        })
        .catch(error => console.error('Error:', error));
 }
