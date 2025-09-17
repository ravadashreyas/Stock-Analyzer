function returnHome(){
    window.location.href = "/";
}

window.onload = function() {
    const companyData = localStorage.getItem('companyData');
    const plotData = localStorage.getItem('plotData');
    const pData = JSON.parse(plotData);
    const cData = JSON.parse(companyData);
    ticker = pData.ticker;
    document.getElementById("putsTitle").innerText = cData.companyName + "(" + ticker.toUpperCase() + ") Puts Options Data";
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
                const plotPut = document.getElementById('putPlot');
                console.log("Calls Data:", calls);
                console.log("Puts Data:", puts);
                const optionsData = {
                    calls: calls,
                    puts: puts
                };
                buildCallsTable(puts);
                Plotly.newPlot(plotPut, data.putGraph.data, data.putGraph.layout);
            })
}; 

function buildCallsTable(puts) {
    var table = document.getElementById("putsTable");
    for (var i = 0; i < (puts.length); i++) {
        var row = `<tr> 
                     <td>${puts[i].contractSymbol}</td> 
                    <td>${puts[i].lastTradeDate}</td>
                     <td>${puts[i].strike}</td> 
                     <td>${puts[i].lastPrice}</td> 
                     <td>${puts[i].bid}</td> 
                     <td>${puts[i].ask}</td>
                    <td>${puts[i].change}</td>
                     <td>${puts[i].percentChange}</td>
                     <td>${puts[i].volume}</td>
                     <td>${puts[i].openInterest}</td>
                     <td>${puts[i].impliedVolatility}</td>
                     </tr>`;
        table.innerHTML += row;
    }
};

