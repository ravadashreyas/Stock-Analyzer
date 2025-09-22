function returnHome() {
    window.location.href = "/";
}

window.onload = function() {
    const companyData = localStorage.getItem('companyData');
    const plotData = localStorage.getItem('plotData');
    
    if (!companyData || !plotData) {
        console.error("Could not find company data in local storage.");
        document.getElementById('companyName').textContent = "Error: Data not found";
        return;
    }

    const cData = JSON.parse(companyData);
    const pData = JSON.parse(plotData);
    const ticker = pData.ticker;
    const tickerName = String(ticker).toUpperCase()

    document.getElementById('companyName').textContent = cData.companyName;
    document.getElementById('tickerSymbol').textContent = tickerName;
    
    fetch("/api/analysis", {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify({ ticker: ticker })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok. Server may have an error.');
        }
        return response.json();
    })
    .then(data => {
        console.log("Received data from server:", data);
        const analysis = data.analysis;
        const stockData = data.stockData;

        const ratingElement = document.getElementById('rating');
        ratingElement.textContent = analysis.rating;
        ratingElement.className = `rating rating-${analysis.rating}`;
        
        document.getElementById('remark').textContent = analysis.remark;

        const tableBody = document.querySelector("#analysisTable tbody");
        tableBody.innerHTML = ''; 
        
        for (const key in analysis) {
            if (key !== 'rating' && key !== 'remark') {
                const row = document.createElement('tr');
                
                const metricCell = document.createElement('td');
                metricCell.textContent = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
                
                const priceCell = document.createElement('td');
                priceCell.textContent = analysis[key] ? `$${analysis[key].toFixed(2)}` : 'N/A';
                
                row.appendChild(metricCell);
                row.appendChild(priceCell);
                tableBody.appendChild(row);
            }
        }
    })
    .catch(error => {
        console.error('Error fetching or processing data:', error);
        document.getElementById('companyName').textContent = "Error";
        document.getElementById('remark').textContent = "Could not load analysis data. Please try again.";
    });
};