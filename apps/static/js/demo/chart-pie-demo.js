// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
console.log('hi')
// Pie Chart Example
var ctx = document.getElementById("myPieChart");
const data_pie = {
  labels: [
    'Game 1',
    'Game 2',
    'Game 3',
    'Game 4'
  ],
  datasets: [{
    label: 'My First Dataset',
    data: [300, 50, 100, 20],
    backgroundColor: [
      'rgb(57, 109, 212)',
      'rgb(0, 194, 131)',
      'rgb(251, 182, 74)',
      'rgb(0, 179, 195)'
    ],
    hoverOffset: 4
  }]
};
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: data_pie,
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
