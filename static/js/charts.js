function randomScalingFactor() {
    return Math.floor(Math.random() * 10);
}



/*
var ctx2 = document.getElementById('myChart2').getContext('2d');
var myLineChart2 = new Chart(ctx2, {
			type: 'line',
			data: {
				labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
				datasets: [{
					label: 'Unfilled',
					fill: false,
					backgroundColor: 'rgba(56, 120, 199, 0.2)',
					borderColor: 'rgba(56, 120, 199, 1)',
					data: [
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor()
					],
				}, {
					label: 'Dashed',
					fill: false,
					backgroundColor: 'rgba(2, 62, 88, 0.2)',
					borderColor: 'rgba(2, 62, 88, 1)',
					borderDash: [5, 5],
					data: [
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor()
					],
				}, {
					label: 'Filled',
					backgroundColor: 'rgba(29, 44, 77, 0.2)',
					borderColor: 'rgba(29, 44, 77, 1)',
					data: [
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor()
					],
					fill: true,
				}]
			},
			options: {
				responsive: true,
				title: {
					display: true,
					text: 'Chart.js Line Chart'
				},
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					x: {
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Month'
						}
					},
					y: {
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Value'
						}
					}
				}
			}
		});

 */