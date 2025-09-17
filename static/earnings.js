function returnHome(){
    window.location.href = "/";
}

window.onload = function() {
    const companyData = localStorage.getItem('companyData');
    const plotData = localStorage.getItem('plotData');
    const pData = JSON.parse(plotData);
    const cData = JSON.parse(companyData);
    const ticker = pData.ticker;
    document.getElementById("earningsTitle").innerText = cData.companyName + "(" + ticker.toUpperCase() + ") Earnings Data";
    if (companyData && plotData) {
        console.log("Retrieved stock data for:", cData.companyName);
        console.log("Retrieved ticker:", pData.ticker);
        console.log("Fetching options data for ticker:", ticker);
    }
    fetch('/api/earnings', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify(pData.ticker)
            })
                .then(response => response.json())
                .then(data => {
                const anEarnings = data.anEarnings;
                const quEarnings = data.quEarnings;
                console.log("Earnings Data:", anEarnings);
                console.log("Earnings Data:", quEarnings);
                const earningsData = {
                    anEarnings: anEarnings,
                    quEarnings: quEarnings
                };
                buildCallsTableAn(anEarnings);
                buildCallsTableQu(quEarnings);
            })
}
function buildCallsTableAn(earnings) {
    table = document.getElementById("anEarningsTableBody");
    for( i= 0; i < earnings.length; i++) {
        row = `<tr> 
            <td>${earnings[i].date}</td>
            <td>${earnings[i].totalRevenue}</td>
            <td>${earnings[i].grossProfit}</td>
            <td>${earnings[i].normalEBITDA}</td>
            <td>${earnings[i].netIncome}</td>
            <td>${earnings[i].dilutedEPS}</td>
            <td>${earnings[i].totalExpenses}</td>
            <td>${earnings[i].operatingIncome}</td>
            </tr>`;
        table.innerHTML += row;
    }
};

function buildCallsTableQu(earnings) {
    table = document.getElementById("quEarningsTableBody");
    for( i= 0; i < earnings.length; i++) {
        row = `<tr> 
            <td>${earnings[i].date}</td>
            <td>${earnings[i].totalRevenue}</td>
            <td>${earnings[i].grossProfit}</td>
            <td>${earnings[i].normalEBITDA}</td>
            <td>${earnings[i].netIncome}</td>
            <td>${earnings[i].dilutedEPS}</td>
            <td>${earnings[i].totalExpenses}</td>
            <td>${earnings[i].operatingIncome}</td>
            </tr>`;
        table.innerHTML += row;
    }
};
            