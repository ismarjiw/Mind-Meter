'use strict'; 

console.log('Connected!')

fetch('/meditations_this_week.json')
.then((response) => response.json())
.then((responseJson) => {
    const data = responseJson.data.map((dailyTotal) => ({
    x: dailyTotal.date,
    y: dailyTotal.length,
    }));

    new Chart(document.querySelector('#line-time'), {
    type: 'line',
    data: {
        datasets: [
        {
            label: 'All sessions',
            data, // equivalent to data: data
        },
        ],
    },
    options: {
        scales: {
        x: {
            type: 'time',
            time: {
            tooltipFormat: 'LLLL dd', // Luxon format string
            unit: 'day',
            },
        },
        },
    },
    });
});