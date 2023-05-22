function createChart() {
    const ctx = document.getElementById('weightChart').getContext('2d');
  
    // Generate the labels for each day in the date range
    const startDate = new Date('2023-05-10');
    const endDate = new Date('2023-05-21');
    const labels = [];
    const currentDate = new Date(startDate);
    while (currentDate <= endDate) {
      const dateString = currentDate.toLocaleDateString('en-US', {
        month: 'numeric',
        day: 'numeric'
      });
      labels.push(dateString);
      currentDate.setDate(currentDate.getDate() + 1);
    }
  
    // Generate the weight data for each day in the date range
    const startWeight = 220;
    const decreaseRate = 2;
    const weights = [];
    let currentWeight = startWeight;
    for (let i = 0; i < labels.length; i++) {
      weights.push(currentWeight);
      currentWeight -= decreaseRate;
    }
  
    // Create the chart
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Weight',
          data: weights,
          borderColor: 'rgb(75, 192, 192)',
          fill: false
        }]
      },
      options: {
      }
    });
  }
  
  createChart();
  