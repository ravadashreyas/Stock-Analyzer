function returnHome(){
    window.location.href = "/";
}
window.onload = function() {
    const companyData = localStorage.getItem('companyData');
    const plotData = localStorage.getItem('plotData');
    
    if (companyData && plotData) {
        const pData = JSON.parse(plotData);
        const cData = JSON.parse(companyData);
        console.log("Retrieved stock data for:", cData.companyName);
        console.log("Retrieved ticker:", pData.ticker);
    }
};