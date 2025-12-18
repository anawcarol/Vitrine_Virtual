let uploadInProgress = false; // Flag para prevenir saída durante upload
window.addEventListener('beforeunload', function (e) {
    if (uploadInProgress) {
        e.preventDefault();
        e.returnValue = 'Upload em andamento. Deseja sair?';
        return e.returnValue;
    }
});
async function uploadVideo() {
    const fileInput = document.getElementById('videoInput');
    if (!fileInput.files[0]) return alert("Selecione um vídeo!");
    uploadInProgress = true;
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('start_time', '00:00:00');
    document.getElementById('ivu-value').innerText = "Processando..."; // Feedback visual
    const xhr = new XMLHttpRequest(); // Usa XMLHttpRequest ao invés de fetch para melhor controle de timeout
    xhr.timeout = 1800000; // 30 minutos
    xhr.open('POST', 'http://127.0.0.1:8000/api/v1/analyze', true);
    xhr.onload = function() {
        uploadInProgress = false;
        if (xhr.status === 200) {
            try {
                const data = JSON.parse(xhr.responseText);
                atualizarInterface(data);
            } catch (error) {
                alert("Erro ao processar resposta");
                document.getElementById('ivu-value').innerText = "--";
            }
        } else {
            alert("Erro no servidor");
            document.getElementById('ivu-value').innerText = "--";
        }
    };
    xhr.onerror = () => {
        uploadInProgress = false;
        alert("Erro de conexão!");
        document.getElementById('ivu-value').innerText = "--";
    };
    xhr.ontimeout = () => {
        uploadInProgress = false;
        alert("Timeout! Processamento demorou muito.");
        document.getElementById('ivu-value').innerText = "--";
    };
    xhr.send(formData);
}
function atualizarInterface(data) {
    const ivu = data.urban_vitality_index;  // Extração dos dados
    const fluxo = data.metrics_basic.fluxo.value;
    const permanencia = data.metrics_basic.permanencia.value;
    const velocidade = data.metrics_behavioral.velocidade.value;
    document.getElementById('ivu-value').innerText = ivu; // Atualização dos Cards
    document.getElementById('flux-value').innerText = fluxo;
    document.getElementById('perm-value').innerText = permanencia + "s";
    const velElement = document.getElementById('vel-value');
    if (velElement) velElement.innerText = velocidade + " m/s";
    const jsonElement = document.getElementById('json-output'); // Exibe o JSON completo
    if (jsonElement) jsonElement.innerText = JSON.stringify(data, null, 2); 
    renderizarGrafico(fluxo, permanencia, ivu, velocidade); // Atualização do Gráfico
}
function renderizarGrafico(f, p, i, v) {
    const ctx = document.getElementById('myChart').getContext('2d');
    if (window.chartInstance) window.chartInstance.destroy();
window.chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Fluxo', 'Permanência (s)', 'IVU', 'Velocidade'],
            datasets: [{
                label: 'Métricas da Vitrine',
                data: [f, p, i, v],
                backgroundColor: ['#0984e3', '#00b894', '#6c5ce7', '#fd79a8']
            }]
        }
    });
}