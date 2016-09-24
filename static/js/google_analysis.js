var SIZE = 5;
var WIDTH = window.innerWidth 
            || document.documentElement.clientWidth
            || document.body.clientWidth;

// Google chart - Line chart.
google.charts.load('current', {packages: ['corechart']});
google.charts.setOnLoadCallback(drawBasic);


function drawBasic() {

      var data = new google.visualization.DataTable();
      data.addColumn('date', 'Date');
      data.addColumn('number', '得分');

      data.addRows([
        
        [new Date('2016-06-30'), 40],
        
      ]);

      var options = {
        hAxis: {
          title: '日期'
        },
        vAxis: {
          title: '得分'
        },
        pointSize: SIZE,
        width: WIDTH * 0.8
      };

      var chart = new google.visualization.LineChart(document.getElementById('divPTS'));

      chart.draw(data, options);

      // FGA
      var data_FGA = new google.visualization.DataTable();
      data_FGA.addColumn('date', 'Date');
      data_FGA.addColumn('number', '投籃出手');

      data_FGA.addRows([
        
        [new Date('2016-06-30'), 38],
        
      ]);

      var options_FGA = {
        hAxis: {
          title: '日期'
        },
        vAxis: {
          title: '投籃出手'
        },
        pointSize: SIZE,
        width: WIDTH * 0.8
      };

      var chart_FGA = new google.visualization.LineChart(document.getElementById('divFGA'));

      chart_FGA.draw(data_FGA, options_FGA);

      // 3PTSA
      var data_3PTSA = new google.visualization.DataTable();
      data_3PTSA.addColumn('date', 'Date');
      data_3PTSA.addColumn('number', '三分球出手');

      data_3PTSA.addRows([
        
        [new Date('2016-06-30'), 8],
        
      ]);

      var options_3PTSA = {
        hAxis: {
          title: '日期'
        },
        vAxis: {
          title: '三分球出手'
        },
        pointSize: SIZE,
        width: WIDTH * 0.8
      };

      var chart_3PTSA = new google.visualization.LineChart(document.getElementById('div3PTSA'));

      chart_3PTSA.draw(data_3PTSA, options_3PTSA);

      // FTA
      var data_FTA = new google.visualization.DataTable();
      data_FTA.addColumn('date', 'Date');
      data_FTA.addColumn('number', '罰球出手');

      data_FTA.addRows([
        
        [new Date('2016-06-30'), 8],
        
      ]);

      var options_FTA = {
        hAxis: {
          title: '日期'
        },
        vAxis: {
          title: '罰球出手'
        },
        pointSize: SIZE,
        width: WIDTH * 0.8
      };

      var chart_FTA = new google.visualization.LineChart(document.getElementById('divFTA'));

      chart_FTA.draw(data_FTA, options_FTA);

      // REB
      var data_REB = new google.visualization.DataTable();
      data_REB.addColumn('date', 'Date');
      data_REB.addColumn('number', '籃板');

      data_REB.addRows([
        
        [new Date('2016-06-30'), 27],
        
      ]);

      var options_REB = {
        hAxis: {
          title: '日期'
        },
        vAxis: {
          title: '籃板'
        },
        pointSize: SIZE,
        width: WIDTH * 0.8
      };

      var chart_REB = new google.visualization.LineChart(document.getElementById('divREB'));

      chart_REB.draw(data_REB, options_REB);

      // OREB
      var data_OREB = new google.visualization.DataTable();
      data_OREB.addColumn('date', 'Date');
      data_OREB.addColumn('number', '進攻籃板');

      data_OREB.addRows([
        
        [new Date('2016-06-30'), 9],
        
      ]);

      var options_OREB = {
        hAxis: {
          title: '日期'
        },
        vAxis: {
          title: '進攻籃板'
        },
        pointSize: SIZE,
        width: WIDTH * 0.8
      };

      var chart_OREB = new google.visualization.LineChart(document.getElementById('divOREB'));

      chart_OREB.draw(data_OREB, options_OREB);

      // DREB
      var data_DREB = new google.visualization.DataTable();
      data_DREB.addColumn('date', 'Date');
      data_DREB.addColumn('number', '防守籃板');

      data_DREB.addRows([
        
        [new Date('2016-06-30'), 18],
        
      ]);

      var options_DREB = {
        hAxis: {
          title: '日期'
        },
        vAxis: {
          title: '防守籃板'
        },
        pointSize: SIZE,
        width: WIDTH * 0.8
      };

      var chart_DREB = new google.visualization.LineChart(document.getElementById('divDREB'));

      chart_DREB.draw(data_DREB, options_DREB);

      // AST
      var data_AST = new google.visualization.DataTable();
      data_AST.addColumn('date', 'Date');
      data_AST.addColumn('number', '助攻');

      data_AST.addRows([
        
        [new Date('2016-06-30'), 6],
        
      ]);

      var options_AST = {
        hAxis: {
          title: '日期'
        },
        vAxis: {
          title: '助攻'
        },
        pointSize: SIZE,
        width: WIDTH * 0.8
      };

      var chart_AST = new google.visualization.LineChart(document.getElementById('divAST'));

      chart_AST.draw(data_AST, options_AST);

      // STL
      var data_STL = new google.visualization.DataTable();
      data_STL.addColumn('date', 'Date');
      data_STL.addColumn('number', '抄截');

      data_STL.addRows([
        
        [new Date('2016-06-30'), 2],
        
      ]);

      var options_STL = {
        hAxis: {
          title: '日期'
        },
        vAxis: {
          title: '抄截'
        },
        pointSize: SIZE,
        width: WIDTH * 0.8
      };

      var chart_STL = new google.visualization.LineChart(document.getElementById('divSTL'));

      chart_STL.draw(data_STL, options_STL);

      // BLK
      var data_BLK = new google.visualization.DataTable();
      data_BLK.addColumn('date', 'Date');
      data_BLK.addColumn('number', '阻攻');

      data_BLK.addRows([
        
        [new Date('2016-06-30'), 3],
        
      ]);

      var options_BLK = {
        hAxis: {
          title: '日期'
        },
        vAxis: {
          title: '阻攻'
        },
        pointSize: SIZE,
        width: WIDTH * 0.8
      };

      var chart_BLK = new google.visualization.LineChart(document.getElementById('divBLK'));

      chart_BLK.draw(data_BLK, options_BLK);

      // TO
      var data_TO = new google.visualization.DataTable();
      data_TO.addColumn('date', 'Date');
      data_TO.addColumn('number', '失誤');

      data_TO.addRows([
        
        [new Date('2016-06-30'), 5],
        
      ]);

      var options_TO = {
        hAxis: {
          title: '日期'
        },
        vAxis: {
          title: '失誤'
        },
        pointSize: SIZE,
        width: WIDTH * 0.8
      };

      var chart_TO = new google.visualization.LineChart(document.getElementById('divTO'));

      chart_TO.draw(data_TO, options_TO);

      // PF
      var data_PF = new google.visualization.DataTable();
      data_PF.addColumn('date', 'Date');
      data_PF.addColumn('number', '犯規');

      data_PF.addRows([
        
        [new Date('2016-06-30'), 12],
        
      ]);

      var options_PF = {
        hAxis: {
          title: '日期'
        },
        vAxis: {
          title: '犯規'
        },
        pointSize: SIZE,
        width: WIDTH * 0.8
      };

      var chart_PF = new google.visualization.LineChart(document.getElementById('divPF'));

      chart_PF.draw(data_PF, options_PF);

      // Percentage of points (Pie chart)
      var two_points = 10 * 2,
          three_points = 2 * 3

      var data_pointsPercent = google.visualization.arrayToDataTable([
          ['Type', 'Points'],
          ['罰球',     4],
          ['二分球',      two_points],
          ['三分球',  three_points]
        ]);

      var options_pointsPercent = {
          title: '得分比例',
          width: WIDTH * 0.4
        };

      var chart_pointsPercent = new google.visualization.PieChart(document.getElementById('piePointsPercent'));

      chart_pointsPercent.draw(data_pointsPercent, options_pointsPercent);

      var data_attemptssPercent = google.visualization.arrayToDataTable([
          ['Type', 'Attempts'],
          ['罰球',     8],
          ['二分球',      30],
          ['三分球',  8]
        ]);

      var options_attemptssPercent = {
          title: '出手比例',
          width: WIDTH * 0.4
        };

      var chart_attemptssPercent = new google.visualization.PieChart(document.getElementById('pieAttemptsPercent'));

      chart_attemptssPercent.draw(data_attemptssPercent, options_attemptssPercent);
    }


