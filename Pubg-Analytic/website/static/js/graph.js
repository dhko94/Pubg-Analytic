google.charts.load('current', {'packages':['corechart', 'bar', 'timeline']});
google.charts.setOnLoadCallback(drawPie);
google.charts.setOnLoadCallback(drawBar);
google.charts.setOnLoadCallback(drawScatter);
google.charts.setOnLoadCallback(drawLine);
google.charts.setOnLoadCallback(drawGantt);




function drawPie() {
    var data = google.visualization.arrayToDataTable(pieData);

    var options = { 
      title: 'Number of each game mode played',
      is3D: true,
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));

    chart.draw(data, options);
};

function drawBar(){
    var data = google.visualization.arrayToDataTable(barData);

    var materialOptions = {
        chart: {
            title: 'Number of Game Played/Map'
        },
        hAxis: {
            title: 'Count',
            minValue: 0,
        },
        vAxis: {
            title: 'mapName'
        },
        legend: 'none',
        bars: 'horizontal'
    };

    var chart = new google.visualization.BarChart(document.getElementById("barchart"));
    chart.draw(data, materialOptions);
};

function drawScatter(){
    var data = google.visualization.arrayToDataTable(scatterData);
    var options = {
        title: "timeSurvived vs kills",
        hAxis: {title: 'timeSurvived'},
        vAxis: {title: 'kills'},
        legend: 'none',
        trendlines: { 0: 
            {
                color: 'green',
            } 
        }
    };

    var chart = new google.visualization.ScatterChart(document.getElementById('scatterchart'));
    chart.draw(data, options);
};

function drawLine(){
    var data = google.visualization.arrayToDataTable(lineData);

    var options = {
        title: 'kills + assists, damageDealt, and headshotKills Performance Correlation',
        legend: {
            position:'bottom'
        }
    };

    var chart = new google.visualization.LineChart(document.getElementById('linechart'));
    chart.draw(data, options);
};

function drawGantt() {

    var container = document.getElementById('ganttchart');
    var chart = new google.visualization.Timeline(container);
    var data = new google.visualization.DataTable();

    data.addColumn({type: 'string', id: 'Date'});
    data.addColumn({type: 'string', id: 'Name'});
    data.addColumn({type: 'date', id: 'Start'});
    data.addColumn({type: 'date', id: 'End'});

    for (var i = 0; i < ganttData.length; i++){
        var d = ganttData[i][0];
        var n = '';
        var sh = ganttData[i][1];
        var sm = ganttData[i][2];
        var eh = ganttData[i][3];
        var em = ganttData[i][4];

        data.addRows([[d, n, new Date(0, 0, 0, sh, sm, 0), new Date(0, 0, 0, eh, em, 0)]]);
    }

    var options = {
        timeline: { colorByRowLabel: false}
    };
    chart.draw(data, options);
};