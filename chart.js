// svg
var width = 1000,
    height = 500,
    margin = {left: 50, top: 30, right: 20, bottom: 20},
    g_width = width - margin.left - margin.right,
    g_height = height - margin.top -margin.bottom,
    high = 4000,
    low = 3000


var svg = d3.select('#container')
    .append('svg')
    .attr('width', width) // width
    .attr('height', height) // height

var trade_time = [
    '9:30',
    '10:00',
    '10:30',
    '11:00',
    '11:30|13:00',
    '13:30',
    '14:00',
    '14:30',
    ''
]

var scale_trade_time = d3.scale.linear()
    .domain([0, 8])
    .range([0, g_width])

var data = [1,3,5,7,8,5,4,3]
d3.select('svg')
    .append('g')
    .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')

var scale_x = d3.scale.linear()
    .domain([0, data.length - 1])
    .range([0, g_width])

var scale_y= d3.scale.linear()
    .domain([0, d3.max(data)])
    .range([g_height, 0])

var scale_index = d3.scale.linear()
    .domain([low, high])
    .range([g_height, 0])

var line_generator = d3.svg.line()
    .x(function(d,i) { return scale_x(i); })
    .y(function(d,i) { return scale_y(d); })


var g = d3.select('g')

g
    .append('path')
    .attr('d', line_generator(data))

var x_axis = d3.svg.axis().scale(scale_trade_time),
    y_axis = d3.svg.axis().scale(scale_y).orient('left'),
    index_axis = d3.svg.axis().scale(scale_index).orient('left');

g.append('g')
    .call(index_axis)
    .attr('transform', 'translate(' + g_width + ', 0)')

g.append('g')
    .call(x_axis)
    .attr('transform', 'translate(0, ' + g_height / 2 + ')')
    .attr('id', 'x-axis')

d3.select('#x-axis').selectAll('text')
    .data(trade_time)
    .text(function(d) { return d; })

svg.selectAll('circle')
    .data(data)
    .enter()
    .append('circle')
    .attr('cx', (d,i) => scale_x(i))
    .attr('cy', (d,i) => scale_y(d))
    .attr('r', 3)
    .attr('fill', 'red')
    .attr('transform', 'translate(50, 30)')
    .on('mouseover', mouse_over)
    .on('mouseout', mouse_out)


g.append('g')
    .call(y_axis)
    .append('text')
    //.text('单位：亿元')
    .attr('text-anchor', 'end')
    .attr('transform', 'translate(40, -10)')
    //.attr('dy', '1em')

function mouse_out(d, i) {
    d3.select(this).attr({
        fill: 'red',
        r: 3
    })
    d3.select('#t' + i + '-' + d + '-' + i).remove()
}

function mouse_over(d, i) {
    console.log(d, i)
    d3.select(this).attr({
        fill: 'orange',
        r: 6
    })
    svg.append('text').attr({
        id: 't' + i + '-' + d + '-' + i,
        x: scale_x(i),
        y: scale_y(d)
    })
    .text([scale_x(i), scale_y(d)])
}
