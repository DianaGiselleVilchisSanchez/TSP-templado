function enviarDatos() {
    const origen = document.getElementById("origen").value.trim();
    const destino = document.getElementById("destino").value.trim();
    const tempInicial = document.getElementById("tempInicial").value;
    const tempMin = document.getElementById("tempMin").value;
    const velocidad = document.getElementById("velocidad").value;

    fetch("/optimizar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            origen: origen,
            destino: destino,
            temperatura: tempInicial,
            minima: tempMin,
            velocidad: velocidad
        })
    })
    .then(response => response.json())
    .then(data => {
        const resultadoDiv = document.getElementById("resultado");
        resultadoDiv.innerHTML = "<h2>Ruta Optimizada:</h2><ul>" +
            data.ruta.map(ciudad => `<li>${ciudad}</li>`).join('') +
            `</ul><p><strong>Distancia Total:</strong> ${data.distancia}</p>`;
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
