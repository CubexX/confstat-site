/**
 * Created by cubexx on 04.07.16.
 */
function getData(name, labels, data) {
    return {
        labels: labels,
        datasets: [
            {
                label: name,
                fill: true,
                lineTension: 0.15,
                backgroundColor: "rgba(144, 202, 249, 0.5)",
                borderColor: "#1976D2",
                borderWidth: 2,
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "#64B5F6",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 2,
                pointHoverRadius: 4,
                pointHoverBackgroundColor: "#1976D2",
                pointHoverBorderColor: "#1976D2",
                pointHoverBorderWidth: 2,
                pointRadius: 3.5,
                pointHitRadius: 10,
                data: data
            }
        ]
    };
}

function createLineChart(elementId, data, name) {
    var ctx = document.getElementById(elementId);

    return new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            title: {
                display: false,
                position: 'bottom',
                text: name
            },
            legend: {
                display: false
            }
        }
    });
}