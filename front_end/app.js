async function uploadVideo() {
    console.log("Botão clicado, iniciando upload...");
    const fileInput = document.getElementById('videoInput');
    if (!fileInput.files[0]) {
        alert("Selecione um vídeo!");
        return;
    }
    console.log("Arquivo selecionado:", fileInput.files[0].name);

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    document.getElementById('ivu-value').innerText = "Processando...";

    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Erro na análise');
        }

        const data = await response.json();
        console.log("DADOS RECEBIDOS:", data); // Verifique no F12
        
        // MAPEAMENTO DOS CAMPOS REAIS DO SEU PYTHON
        const ivu = data.urban_vitality_index;
        const fluxo = data.metrics_basic.fluxo.value;
        const perm = data.metrics_basic.permanencia.value;
        const vel = data.metrics_behavioral.velocidade.value;

        // Atualiza a tela
        document.getElementById('ivu-value').innerText = ivu;
        document.getElementById('flux-value').innerText = fluxo;
        document.getElementById('perm-value').innerText = perm + "s";
        document.getElementById('vel-value').innerText = vel + " m/s";

        // Exibe o JSON completo
        document.getElementById('json-output').innerText = JSON.stringify(data, null, 2);

        renderChart(fluxo, perm, ivu, vel);

    } catch (error) {
        console.error("Erro no JS:", error);
        alert("Erro: " + error.message);
    }
}

function renderChart(f, p, i, v) {
    const ctx = document.getElementById('myChart').getContext('2d');
    if (window.chartInstance) window.chartInstance.destroy();

    window.chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Fluxo', 'Permanência (s)', 'IVU', 'Velocidade (m/s)'],
            datasets: [{
                label: 'Métricas da Vitrine',
                data: [f, p, i, v],
                backgroundColor: ['#0984e3', '#00b894', '#6c5ce7', '#fd79a8']
            }]
        }
    });
}