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

            if (typeof data === 'string') {
                document.getElementById('clima-info').innerHTML = `<h3>${data}</h3>`;
                return;
            }

            const temperatura = Math.round(data.temperature);
            const tipoClima = data.tipo_clima || 'Condição desconhecida';
            const previsao5Dias = data.previsao_5_dias || [];

            const linhasPrevisao = previsao5Dias.map((dia) => {
                const dataFormatada = new Date(`${dia.data}T00:00:00`).toLocaleDateString('pt-BR', {
                    weekday: 'short',
                    day: '2-digit'
                });

                const tempMax = dia.temp_max != null ? Math.round(dia.temp_max) : '-';
                const tempMin = dia.temp_min != null ? Math.round(dia.temp_min) : '-';

                return `
            <div class="forecast-row">
                <span class="dia">${dataFormatada}</span>
                <span class="tipo">${dia.tipo_clima}</span>
                <span class="temp">
                    <strong>${tempMax}°</strong>
                    <span>${tempMin}°</span>
                </span>
            </div>
        `;
            }).join('');

            document.getElementById('main').style.display = 'none';
            const climaInfo = document.getElementById('clima-info');

            climaInfo.innerHTML = `
        <section class="current-weather">
            <h3>${data.cidade_formatada || cidade}</h3>
            <h1>${temperatura} °C</h1>
            <span class="spam-tipo-clima">${tipoClima}</span>
        </section>

        <section class="forecast-box">
            <h2>Próximos 5 dias</h2>
            ${linhasPrevisao}
        </section>
    `;
        })
        .catch(error => {
            console.error('Erro:', error);
        });
});