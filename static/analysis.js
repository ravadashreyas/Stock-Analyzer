function returnHome(){
    window.location.href = "/";
}

window.onload = function() {
    const companyData = localStorage.getItem('companyData');
    const plotData = localStorage.getItem('plotData');
    const pData = JSON.parse(plotData);
    const cData = JSON.parse(companyData);
    ticker = pData.ticker;
    if (companyData && plotData) {
        console.log("Retrieved stock data for:", cData.companyName);
        console.log("Retrieved ticker:", pData.ticker);
        console.log("Fetching options data for ticker:", ticker);
    } 
    fetch("/api/analysis",{
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(ticker)
    })
        .then(response => response.json())
        .then(data => {
            console.log("Parsed options data from server:", data);  
    })
}    