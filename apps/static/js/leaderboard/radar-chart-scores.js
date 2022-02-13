// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var ctx = document.getElementById("myRadarChart");

var team_data = score_data['teams']
var game_data = score_data['games']

var game_names = []
var team_scores = {}



for (key in game_data) {
  game_names.push(key)
}
game_names.sort()

for (key in team_data) {
  team_scores = []
}

const data = {
  datasets: []
}

data['labels'] = game_names

console.log(team_data)


for (team in team_data) {
  console.log(Object.values(team_data[team]))
  data['datasets'].push({
    label: team,
    data: Object.values(team_data[team]),
    fill: true,
    
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
    borderColor: 'rgb(255, 99, 132)',
    pointBackgroundColor: 'rgb(255, 99, 132)',
    pointBorderColor: '#fff',
    pointHoverBackgroundColor: '#fff',
    pointHoverBorderColor: 'rgb(255, 99, 132)'
  })
}

// const data = {

//   labels: game_names,
//   datasets: [{
//     label: 'Team 1',
//     data: [65, 59, 90, 81],
//     fill: true,
//     backgroundColor: 'rgba(255, 99, 132, 0.2)',
//     borderColor: 'rgb(255, 99, 132)',
//     pointBackgroundColor: 'rgb(255, 99, 132)',
//     pointBorderColor: '#fff',
//     pointHoverBackgroundColor: '#fff',
//     pointHoverBorderColor: 'rgb(255, 99, 132)'
//   },{
//     label: 'Team 2',
//     data: [28, 48, 40, 19],
//     fill: true,
//     backgroundColor: 'rgba(54, 162, 235, 0.2)',
//     borderColor: 'rgb(54, 162, 235)',
//     pointBackgroundColor: 'rgb(54, 162, 235)',
//     pointBorderColor: '#fff',
//     pointHoverBackgroundColor: '#fff',
//     pointHoverBorderColor: 'rgb(54, 162, 235)'
//   }]
// }

var myRadarChart = new Chart(ctx, {
  type: 'radar',
  data: data,
    options: {
    elements: {
      line: {
        borderWidth: 3
      }
    }
  },
});
