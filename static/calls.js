function returnHome(){
    window.location.href = "/";
}

window.onload = function() {
    const companyData = localStorage.getItem('companyData');
    const plotData = localStorage.getItem('plotData');
    const pData = JSON.parse(plotData);
    const cData = JSON.parse(companyData);
    ticker = pData.ticker;
    document.getElementById("callsTitle").innerText = cData.companyName + "(" + ticker.toUpperCase() + ") Calls Options Data";
    if (companyData && plotData) {
        console.log("Retrieved stock data for:", cData.companyName);
        console.log("Retrieved ticker:", pData.ticker);
        console.log("Fetching options data for ticker:", ticker);
    }
    fetch('/api/options', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify(pData.ticker)
            })
                .then(response => response.json())
                .then(data => {
                const calls = data.calls;
                const puts = data.puts;
                const plotCall = document.getElementById('callPlot');
                const optionsData = {
                    calls: calls,
                    puts: puts
                };
                buildCallsTable(calls);
                Plotly.newPlot(plotCall, data.callGraph.data, data.callGraph.layout);
            })
}; 

function buildCallsTable(calls) {
    var table = document.getElementById("callsTable");
    for (var i = 0; i < (calls.length); i++) {
        var row = `<tr> 
                     <td>${calls[i].contractSymbol}</td> 
                     <td>${calls[i].lastTradeDate}</td>
                     <td>${calls[i].strike}</td> 
                     <td>${calls[i].lastPrice}</td> 
                     <td>${calls[i].bid}</td> 
                     <td>${calls[i].ask}</td>
                     <td>${calls[i].change}</td>
                     <td>${calls[i].percentChange}</td>
                     <td>${calls[i].volume}</td>
                     <td>${calls[i].openInterest}</td>
                     <td>${calls[i].impliedVolatility}</td>
                     </tr>`;
        table.innerHTML += row;
    }
};

