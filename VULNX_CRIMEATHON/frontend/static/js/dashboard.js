document.addEventListener('DOMContentLoaded', () => {
    const runButton = document.getElementById('runAssessment');
    const assessmentForm = document.getElementById('assessmentForm');
    const reportButton = document.getElementById('downloadReport');

    if (runButton) {
        runButton.addEventListener('click', async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/assessment', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mode: 'vulnerable' })
                });
                const data = await response.json();
                const list = document.getElementById('findingsList');
                if (list) {
                    list.innerHTML = data.findings.map(f => `<li>${f.title} — ${f.severity}</li>`).join('');
                }
                document.getElementById('totalAssessments').textContent = '1';
                document.getElementById('vulnerabilities').textContent = String(data.findings.length);
                document.getElementById('highSeverity').textContent = String(data.findings.filter(f => f.severity === 'high').length);
            } catch (error) {
                console.error(error);
            }
        });
    }

    if (assessmentForm) {
        assessmentForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const mode = document.getElementById('mode').value;
            const response = await fetch('http://127.0.0.1:5000/api/assessment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mode })
            });
            const data = await response.json();
            document.getElementById('assessmentOutput').textContent = JSON.stringify(data, null, 2);
        });
    }

    if (reportButton) {
        reportButton.addEventListener('click', async () => {
            const response = await fetch('http://127.0.0.1:5000/api/reports');
            const data = await response.json();
            document.getElementById('reportOutput').textContent = JSON.stringify(data, null, 2);
        });
    }
});
