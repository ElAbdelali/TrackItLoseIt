let delayed = false;
fetch('/weight_and_date.json')
  .then(response => response.json())
  .then(responseJson => {
    const data = responseJson.data.map(item => ({
      x: new Date(item.date),
      y: item.weight,
    }));

    // Sort the data array by date
    data.sort((a, b) => a.x - b.x);

    new Chart(document.querySelector('#line-chart'), {
      type: 'line',
      data: {
        datasets: [{
          label: 'Weight',
          data,
          borderColor: 'black',
          backgroundColor: 'rgba(0, 0, 255, 0.2)',
        }],
      },
      options: {
        animation: {
          delay: (context) => {
            let delay = 0;
            if (context.type === 'data' && context.mode === 'default' && !delayed) {
              delay = context.dataIndex * 300 + context.datasetIndex * 100;
            }
            return delay;
          },
          onComplete: () => {
            delayed = true;
          },
        },
        interaction: {
          intersect: false,
          mode: 'nearest'
        },
        responsive: true,
        scales: {
          x: {
            type: 'time',
            time: {
              tooltipFormat: 'MMMM DD, YYYY',
              unit: 'day',
            },
            title: {
              display: true,
              text: 'Date'
            }
          },
          y: {
            title: {
              display: true,
              text: 'Weight (lbs)'
            }
          }
        },
      },
    });
  });
