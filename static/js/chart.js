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
          borderColor: 'blue',  // Set line color to blue
          backgroundColor: 'rgba(0, 0, 255, 0.2)',  // Set fill color to light blue
        }],
      },
      options: {
        scales: {
          x: {
            type: 'time',
            time: {
              tooltipFormat: 'MMMM DD, YYYY',
              unit: 'day',
            },
          },
        },
      },
    });
  });
