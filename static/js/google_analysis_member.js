


//---------------
//member summary
//---------------

    function HideTotShowAvg() {
    document.getElementById('average').style.display = "block";
    document.getElementById('total').style.display = "none";
}

function HideAvgShowTot() {
    document.getElementById('average').style.display = "none";
    document.getElementById('total').style.display = "block";
}

// Google
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Name');    
    data.addColumn('number', 'Points');
    data.addRows([
      ['DataHoops_1', 9.0],
      ['Others', 31.0]
    ]);
    // Create the data table.
    var data2 = new google.visualization.DataTable();
    data2.addColumn('string', 'Name');
    data2.addColumn('number', 'Assists');
    data2.addRows([
      ['DataHoops_1', 4.0],
      ['Others', 2.0]
    ]);
    // Create the data table.
    var data3 = new google.visualization.DataTable();
    data3.addColumn('string', 'Name');
    data3.addColumn('number', 'Rebonds');
    data3.addRows([
      ['DataHoops_1', 2.0],
      ['Others', 25.0]
    ]);

    // Set chart options
    var options = {'title':'Pts. / Game'};
    // Set chart options
    var options2 = {'title':'Ast. / Game'};
    // Set chart options
    var options3 = {'title':'Reb. / Game'};

    var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
    chart.draw(data, options);
    var chart2 = new google.visualization.PieChart(document.getElementById('chart_div2'));
    chart2.draw(data2, options2);
    var chart3 = new google.visualization.PieChart(document.getElementById('chart_div3'));
    chart3.draw(data3, options3);
}