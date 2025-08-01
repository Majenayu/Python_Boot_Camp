const ctx = document.getElementById('scoreChart').getContext('2d');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: Array.from({length: window.scoreData.numQuestions}, (_, i) => i),
        datasets: [{
            label: 'Number of Students',
            data: window.scoreData.scoreDistribution,
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true, title: { display: true, text: 'Number of Students' } },
            x: { title: { display: true, text: 'Score' } }
        }
    }
});