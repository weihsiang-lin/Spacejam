var chart = c3.generate({
    bindto: '#chart1',
    data: {
        columns: [
            ['data1', 60],
            ['data2', 40],
        ],
        type : 'donut',
        onclick: function (d, i) { console.log("onclick", d, i); },
        /*onmouseover: function (d, i) { console.log("onmouseover", d, i); },
        onmouseout: function (d, i) { console.log("onmouseout", d, i); }*/
    },
    color: {
        pattern: ['#E6E6E6', '#e1271d']
    },
    donut: {
        width: 4,
        label: {
            show: false
        },
    },
    legend: {
        show: false
    },
    tooltip: {
        show: false
        // contents: function (d, defaultTitleFormat, defaultValueFormat, color) {
        //     return '<div style="background-color:rgba(0,0,0,.9); font-size:1.4em; line-height:1.6; min-width:200px; text-align:left; padding:10px;"><span style="color:#00fcff;">慷慨的藥</span><br/>能夠開源節流是件好事，但也不要過了頭；大家在各自的崗位上努力，也該享有相對應的收穫。有時候小小的不計較，會換來大大的驚喜回報！</div>';
        // }
    }
});
// add name
d3.select("#chart1 .c3-chart-arcs")
    .append("text")
    .text("40.0")
    .attr("dy", "0.4em")
    .attr("dx", "-0.9em")
    .attr("font-size", "1.5rem")
    .attr("font-family", "Ubuntu")
// add percentage
d3.select("#chart1 .c3-chart-arcs")
    .append("text")
    .text("平均得分")
    .attr("dy", "5em")
    .attr("dx", "-2em")
    .attr("font-size", "1rem")
    .attr("font-family", "cwTeXHei")

var chart = c3.generate({
    bindto: '#chart2',
    data: {
        columns: [
            ['data1', 68.4],
            ['data2', 31.6],
        ],
        type : 'donut',
        /*onclick: function (d, i) { console.log("onclick", d, i); },
        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
        onmouseout: function (d, i) { console.log("onmouseout", d, i); }*/
    },
    color: {
        pattern: ['#E6E6E6', '#e1271d']
    },
    donut: {
        width: 4,
        label: {
            show: false
        },
    },
    legend: {
        show: false
    },
    tooltip: {
        show: false
        // contents: function (d, defaultTitleFormat, defaultValueFormat, color) {
        //     return '<div style="background-color:rgba(0,0,0,.9); font-size:1.4em; line-height:1.6; min-width:200px; text-align:left; padding:10px;"><span style="color:#00fcff;">記憶麵包</span><br/>看大不看小在某些地方可能是個好習慣；但千萬別忘了「萬丈高樓平地起」和「積沙成塔」這兩句話，有時候，適度的在乎一下是需要的。</div>';
        // }
    }
});
// add name
d3.select("#chart2 .c3-chart-arcs")
    .append("text")
    .text("31.6%")
    .attr("width", "65px")
    .attr("dy", "0.4em")
    .attr("dx", "-1.3em")
    .attr("font-size", "1.5rem")
    .attr("font-family", "Ubuntu")
// add percentage
d3.select("#chart2 .c3-chart-arcs")
    .append("text")
    .text("命中率")
    .attr("dy", "5em")
    .attr("dx", "-1.5em")
    .attr("font-size", "1rem")
    .attr("font-family", "cwTeXHei")

var chart = c3.generate({
    bindto: '#chart3',
    data: {
        columns: [
            ['data1', 40],
            ['data2', 60],
        ],
        type : 'donut',
        /*onclick: function (d, i) { console.log("onclick", d, i); },
        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
        onmouseout: function (d, i) { console.log("onmouseout", d, i); }*/
    },
    color: {
        pattern: ['#E6E6E6', '#e1271d']
    },
    donut: {
        //title: "Annabelle's hohoho",
        width: 4,
        label: {
            show: false
        },
    },
    legend: {
        show: false
    },
    tooltip: {
        show: false
        // contents: function (d, defaultTitleFormat, defaultValueFormat, color) {
        //     return '<div style="background-color:rgba(0,0,0,.9); font-size:1.4em; line-height:1.6; min-width:200px; text-align:left; padding:10px;"><span style="color:#00fcff;">指引天使</span><br/>相信專業是個不錯的選擇！不過，在完全託付之前，還是該花心思選出最適合的專業團隊，避免發生「所託非人」的遺憾。</div>';
        // }
    }
});
// add name
d3.select("#chart3 .c3-chart-arcs")
    .append("text")
    .text("6.0")
    .attr("dy", "0.4em")
    .attr("dx", "-0.7em")
    .attr("font-size", "1.5rem")
    .attr("font-family", "Ubuntu")
// add percentage
d3.select("#chart3 .c3-chart-arcs")
    .append("text")
    .text("平均助攻")
    .attr("dy", "5em")
    .attr("dx", "-2em")
    .attr("font-size", "1rem")
    .attr("font-family", "cwTeXHei")

var chart = c3.generate({
    bindto: '#chart4',
    data: {
        columns: [
            ['data1', 73],
            ['data2', 27],
        ],
        type : 'donut',
        /*onclick: function (d, i) { console.log("onclick", d, i); },
        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
        onmouseout: function (d, i) { console.log("onmouseout", d, i); }*/
    },
    color: {
        pattern: ['#E6E6E6', '#e1271d']
    },
    donut: {
        width: 4,
        label: {
            show: false
        },
    },
    legend: {
        show: false
    },
    tooltip: {
        show: false
        // contents: function (d, defaultTitleFormat, defaultValueFormat, color) {
        //     return '<div style="background-color:rgba(0,0,0,.9); font-size:1.4em; line-height:1.6; min-width:200px; text-align:left; padding:10px;"><span style="color:#00fcff;">算了算了棒</span><br/>事必躬親絕對可以做出最適合自己的安排；但是，要達到目的，通常需要花很多時間、力氣和金錢…所以，同樣可以達到目的，有時候相信專業的建議安排，也是一個不錯的選擇！</div>';
        // }
    }
});
// add name
d3.select("#chart4 .c3-chart-arcs")
    .append("text")
    .text("27.0")
    .attr("dy", "0.4em")
    .attr("dx", "-0.9em")
    .attr("font-size", "1.5rem")
    .attr("font-family", "Ubuntu")
// add percentage
d3.select("#chart4 .c3-chart-arcs")
    .append("text")
    .text("平均籃板")
    .attr("dy", "5em")
    .attr("dx", "-2em")
    .attr("font-size", "1rem")
    .attr("font-family", "cwTeXHei")
// add image
// d3.select("#chart4 .c3-chart-arcs")
//     .append('image')
//     .attr('xlink:href','images/prop/prop_b2.png')
//     .attr('height', '70')
//     .attr('width', '70')
//     .style('transform', 'translate(-35px,-35px)')
//     .style('-webkit-transform', 'translate(-35px,-35px)')
//     .style('-moz-transform', 'translate(-35px,-35px)')
//     .style('-ms-transform', 'translate(-35px,-35px)')
//     .attr('transform', 'matrix(1 0 0 1 -35 -35)')


/*setTimeout(function () {
    chart.load({
        columns: [
            ["setosa", 60],
            ["versicolor", 40],
        ]
    });
}, 1500);*/

/*setTimeout(function () {
    chart.unload({
        ids: 'data1'
    });
    chart.unload({
        ids: 'data2'
    });
}, 2500);*/

// var g= document.querySelector('g image'),
//     transform= getComputedStyle(g).getPropertyValue('transform');
// g.setAttribute('transform', transform);