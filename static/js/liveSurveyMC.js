      google.charts.load('current', {
        'packages': ['corechart']
      });
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Answers', 'Count'],
          ['A', 18],
          ['B', 2],
          ['C', 5],
          ['D', 2],
        ]);

        var options = {
          title: 'Answers'
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }
