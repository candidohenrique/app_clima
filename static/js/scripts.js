document.getElementById('busca').addEventListener("submit", function (event) {
    event.preventDefault();
    const cidade = document.getElementById('cidade').value

    fetch('/clima', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
        },
        body: JSON.stringify({ cidade: cidade }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const temperatura = Math.round(data.temperature);
            const ventos = Math.round(data.windspeed);

            document.getElementById('busca').style.display = 'none';
            const climaInfo = document.getElementById('clima-info');
            climaInfo.innerHTML = `
                <p><strong>${cidade}</strong></p>
                <p>Temperatura: ${temperatura}°C</p>
                <p>Ventos: ${ventos} km/h</p>
            `;
        })
        .catch(error => {
            console.error('Erro:', error);
        });
});