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
        })
        .catch(error => {
            console.error('Erro:', error);
        });
});