// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
console.log('hi')
// Pie Chart Example
var ctx = document.getElementById("myPieChart");

var game_data = score_data["games"]
console.log(game_data)


var game_names = []
var game_plays = []

for (key in game_data) {
  game_names.push(key)
  game_plays.push(game_data[key]["plays"])
}



for (let i = 0; i < game_names.length; i++) {
  document.getElementById("game-title-" + (i+1)).innerHTML = game_names[i]
}

const data_pie = {
  labels: game_names,
  datasets: [{
    label: 'Game Stats',
    data: game_plays,
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
