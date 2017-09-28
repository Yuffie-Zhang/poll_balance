/**
 * Created by yz on 9/1/17.
 */
var chartWidth = 200,
    barHeight = 15,
    groupHeight = barHeight*3,
    gapBetweenGroups = 8,
    spaceForLabels = 180,
    spaceForLegend = 200;
var result_width = 360,
    result_height = 300,
    result_barWidth = 100;
var legendRectSize = 18,
    legendTotalSize=40,
    legendSpacing = 4;
var edu_survey_data, edu_baseline_data, edu_data, edu_x, gender_survey_data,gender_baseline_data, gender_data, gender_x,
    hispanic_survey_data,hispanic_baseline_data,hispanic_data, hispanic_x, race_survey_data,race_baseline_data,race_data,
    race_x, income_survey_data,income_baseline_data,income_data, income_x, political_view_survey_data,
    political_view_baseline_data,political_view_data, political_view_x, party_survey_data,party_baseline_data,
    party_data, party_x, region_survey_data,region_baseline_data,region_data, region_x, age_survey_data,age_baseline_data,
    age_data, age_x,result_data,result_y,legend_data;
//emptyarray to remove exit()
var emptyarray = {};

$(document).ready(function () {
    // //draw survey data
    $(".survey_datasource").click(function () {
        $.post('/requestdata', {name: $(this).attr('value')}, function (data) {
            edu_survey(data);
            gender_survey(data);
            region_survey(data);
            hispanic_survey(data);
            age_survey(data);
            race_survey(data);
            party_survey(data);
            income_survey(data);
            political_view_survey(data);
            result(data);

        });
    });
});


function edu_survey(data) {
//edu chart
    var edu_labels = data["edu"]["labels"];
    edu_survey_data = data["edu"]["values"];
    edu_data=edu_survey_data;
    var educhartHeight = barHeight * edu_data.length * 3 + gapBetweenGroups * edu_labels.length;
    edu_x = d3.scale.linear()
        .domain([0, d3.max(edu_data)])
        .range([0, chartWidth]);

// Specify the chart area and dimensions
    var educhart = d3.select("#edu_level_chart")
        .attr("width", spaceForLabels + chartWidth + spaceForLegend)
        .attr("height", educhartHeight);

//bind elements to an empty array to get exit() part
    var edu_update = educhart.selectAll("g")
        .data(emptyarray);
    edu_update.exit().remove();
// Create bars, bars contains text label on the left, rect in the middle and number labels on the right
    var edu_bar = educhart.selectAll("g").data(edu_data).enter().append("g")
        .attr("transform", function (d, i) {
            //left offset and upper offset
            return "translate(" + spaceForLabels + "," + (i * groupHeight + gapBetweenGroups * (0.5 + i)  ) + ")";
        });

// Create rectangles of the correct width
    edu_bar.append("rect")
        .attr("fill", "#1f77b4")
        .attr("class", "bar")
        .attr("width", edu_x)
        .attr("height", barHeight - 1);

// Add number label on the right
    edu_bar.append("text")
        .attr("class", "numlabel")
        .attr("x", function (d) {
            return edu_x(d) + 3;
        })
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
        .text(function (d) {
            return d + "%";
        });

// Draw labels on the left
    edu_bar.append("text")
        .attr("class", "label")
        .attr("x", function (d) {
            return -10;
        })
        .attr("y", groupHeight / 2)
        .attr("dy", "-.15em")
        .style("text-anchor", "end")
        .style("font", "14px sans-serif")
        .text(function (d, i) {
            return edu_labels[i];
        });
}
function gender_survey(data) {
    //gender chart
    var gender_labels = data["gender"]["labels"];
    gender_survey_data = data["gender"]["values"];
    gender_data=gender_survey_data;
    var genderchartHeight = barHeight * gender_data.length * 3 + gapBetweenGroups * gender_labels.length;
    gender_x = d3.scale.linear()
        .domain([0, d3.max(gender_data)])
        .range([0, chartWidth]);

// Specify the chart area and dimensions
    var genderchart = d3.select("#gender_chart")
        .attr("width", spaceForLabels + chartWidth + spaceForLegend)
        .attr("height", genderchartHeight);

//bind elements to an empty array to get exit() part
    var gender_update = genderchart.selectAll("g")
        .data(emptyarray);
    gender_update.exit().remove();

// Create bars, bars contains text label on the left, rect in the middle and number labels on the right
    var bar = genderchart.selectAll("g")
        .data(gender_data)
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (i * groupHeight + gapBetweenGroups * (0.5 + i)  ) + ")";
        });

// Create rectangles of the correct width
    bar.append("rect")
        .attr("fill", "#1f77b4")
        .attr("class", "bar")
        .attr("width", gender_x)
        .attr("height", barHeight - 1);

// Add number label on the right
    bar.append("text")
        .attr("class", "numlabel")
        .attr("x", function (d) {
            return gender_x(d) + 3;
        })
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
        .text(function (d) {
            return d + "%";
        });

// Draw labels
    bar.append("text")
        .attr("class", "label")
        .attr("x", function (d) {
            return -10;
        })
        .attr("y", groupHeight / 2)
        .attr("dy", "-.15em")
        .style("text-anchor", "end")
        .style("font", "14px sans-serif")
        .text(function (d, i) {
            return gender_labels[i];
        });
}
function age_survey(data) {
    //age chart
    var age_labels = data["age"]["labels"];
    age_survey_data = data["age"]["values"];
    age_data=age_survey_data;
    var agechartHeight = barHeight * age_data.length * 3 + gapBetweenGroups * age_labels.length;
    age_x = d3.scale.linear()
        .domain([0, d3.max(age_data)])
        .range([0, chartWidth]);

    // Specify the chart area and dimensions
    var agechart = d3.select("#age_chart")
        .attr("width", spaceForLabels + chartWidth + spaceForLegend)
        .attr("height", agechartHeight);

    //bind elements to an empty array to get exit() part
    var age_update = agechart.selectAll("g")
        .data(emptyarray);
    age_update.exit().remove();

    // Create bars, bars contains text label on the left, rect in the middle and number labels on the right
    var bar = agechart.selectAll("g")
        .data(age_data)
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (i * groupHeight + gapBetweenGroups * (0.5 + i)  ) + ")";
        });

    // Create rectangles of the correct width
    bar.append("rect")
        .attr("fill", "#1f77b4")
        .attr("class", "bar")
        .attr("width", age_x)
        .attr("height", barHeight - 1);

    // Add number label on the right
    bar.append("text")
        .attr("class", "numlabel")
        .attr("x", function (d) {
            return age_x(d) + 3;
        })
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
        .text(function (d) {
            return d + "%";
        });

    // Draw labels
    bar.append("text")
        .attr("class", "label")
        .attr("x", function (d) {
            return -10;
        })
        .attr("y", groupHeight / 2)
        .attr("dy", "-.15em")
        .style("text-anchor", "end")
        .style("font", "14px sans-serif")
        .text(function (d, i) {
            return age_labels[i];
        });
}
function hispanic_survey(data) {
    //hispanic chart
    var hispanic_labels = data["hispanic"]["labels"];
    hispanic_survey_data = data["hispanic"]["values"];
    hispanic_data=hispanic_survey_data;
    var hispanicchartHeight = barHeight * hispanic_data.length * 3 + gapBetweenGroups * hispanic_labels.length;
    hispanic_x = d3.scale.linear()
        .domain([0, d3.max(hispanic_data)])
        .range([0, chartWidth]);

    // Specify the chart area and dimensions
    var hispanicchart = d3.select("#hispanic_chart")
        .attr("width", spaceForLabels + chartWidth + spaceForLegend)
        .attr("height", hispanicchartHeight);
    //bind elements to an empty array to get exit() part
    var hispanic_update = hispanicchart.selectAll("g")
        .data(emptyarray);
    hispanic_update.exit().remove();
    // Create bars, bars contains text label on the left, rect in the middle and number labels on the right
    var bar = hispanicchart.selectAll("g")
        .data(hispanic_data)
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (i * groupHeight + gapBetweenGroups * (0.5 + i)  ) + ")";
        });

    // Create rectangles of the correct width
    bar.append("rect")
        .attr("fill", "#1f77b4")
        .attr("class", "bar")
        .attr("width", hispanic_x)
        .attr("height", barHeight - 1);

    // Add number label on the right
    bar.append("text")
        .attr("class", "numlabel")
        .attr("x", function (d) {
            return hispanic_x(d) + 3;
        })
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
        .text(function (d) {
            return d + "%";
        });

    // Draw labels
    bar.append("text")
        .attr("class", "label")
        .attr("x", function (d) {
            return -10;
        })
        .attr("y", groupHeight / 2)
        .attr("dy", "-.15em")
        .style("text-anchor", "end")
        .style("font", "14px sans-serif")
        .text(function (d, i) {
            return hispanic_labels[i];
        });
}
function income_survey(data) {
    //income chart
    var income_labels = data["income"]["labels"];
    income_survey_data = data["income"]["values"];
    income_data=income_survey_data;
    var incomechartHeight = barHeight * income_data.length * 3 + gapBetweenGroups * income_labels.length;
    income_x = d3.scale.linear()
        .domain([0, d3.max(income_data)])
        .range([0, chartWidth]);

    // Specify the chart area and dimensions
    var incomechart = d3.select("#income_chart")
        .attr("width", spaceForLabels + chartWidth + spaceForLegend)
        .attr("height", incomechartHeight);
    //bind elements to an empty array to get exit() part
    var income_update = incomechart.selectAll("g")
        .data(emptyarray);
    income_update.exit().remove();

    // Create bars, bars contains text label on the left, rect in the middle and number labels on the right
    var bar = incomechart.selectAll("g")
        .data(income_data)
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (i * groupHeight + gapBetweenGroups * (0.5 + i)  ) + ")";
        });

    // Create rectangles of the correct width
    bar.append("rect")
        .attr("fill", "#1f77b4")
        .attr("class", "bar")
        .attr("width", income_x)
        .attr("height", barHeight - 1);

    // Add number label on the right
    bar.append("text")
        .attr("class", "numlabel")
        .attr("x", function (d) {
            return income_x(d) + 3;
        })
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
        .text(function (d) {
            return d + "%";
        });

    // Draw labels
    bar.append("text")
        .attr("class", "label")
        .attr("x", function (d) {
            return -10;
        })
        .attr("y", groupHeight / 2)
        .attr("dy", "-.15em")
        .style("text-anchor", "end")
        .style("font", "14px sans-serif")
        .text(function (d, i) {
            return income_labels[i];
        });
}
function political_view_survey(data) {
    //political_view chart
    var political_view_labels = data["political_view"]["labels"];
    political_view_survey_data = data["political_view"]["values"];
    political_view_data=political_view_survey_data;
    var political_viewchartHeight = barHeight * political_view_data.length * 3 + gapBetweenGroups * political_view_labels.length;
    political_view_x = d3.scale.linear()
        .domain([0, d3.max(political_view_data)])
        .range([0, chartWidth]);

    // Specify the chart area and dimensions
    var political_viewchart = d3.select("#political_view_chart")
        .attr("width", spaceForLabels + chartWidth + spaceForLegend)
        .attr("height", political_viewchartHeight);
    //bind elements to an empty array to get exit() part
    var political_view_update = political_viewchart.selectAll("g")
        .data(emptyarray);
    political_view_update.exit().remove();

    // Create bars, bars contains text label on the left, rect in the middle and number labels on the right
    var bar = political_viewchart.selectAll("g")
        .data(political_view_data)
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (i * groupHeight + gapBetweenGroups * (0.5 + i)  ) + ")";
        });

    // Create rectangles of the correct width
    bar.append("rect")
        .attr("fill", "#1f77b4")
        .attr("class", "bar")
        .attr("width", political_view_x)
        .attr("height", barHeight - 1);

    // Add number label on the right
    bar.append("text")
        .attr("class", "numlabel")
        .attr("x", function (d) {
            return political_view_x(d) + 3;
        })
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
        .text(function (d) {
            return d + "%";
        });

    // Draw labels
    bar.append("text")
        .attr("class", "label")
        .attr("x", function (d) {
            return -10;
        })
        .attr("y", groupHeight / 2)
        .attr("dy", "-.15em")
        .style("text-anchor", "end")
        .style("font", "14px sans-serif")
        .text(function (d, i) {
            return political_view_labels[i];
        });
}
function party_survey(data) {
    //party chart
    var party_labels = data["party"]["labels"];
    party_survey_data = data["party"]["values"];
    party_data=party_survey_data;
    var partychartHeight = barHeight * party_data.length * 3 + gapBetweenGroups * party_labels.length;
    party_x = d3.scale.linear()
        .domain([0, d3.max(party_data)])
        .range([0, chartWidth]);

    // Specify the chart area and dimensions
    var partychart = d3.select("#party_chart")
        .attr("width", spaceForLabels + chartWidth + spaceForLegend)
        .attr("height", partychartHeight);
    //bind elements to an empty array to get exit() part
    var party_update = partychart.selectAll("g")
        .data(emptyarray);
    party_update.exit().remove();

    // Create bars, bars contains text label on the left, rect in the middle and number labels on the right
    var bar = partychart.selectAll("g")
        .data(party_data)
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (i * groupHeight + gapBetweenGroups * (0.5 + i)  ) + ")";
        });

    // Create rectangles of the correct width
    bar.append("rect")
        .attr("fill", "#1f77b4")
        .attr("class", "bar")
        .attr("width", party_x)
        .attr("height", barHeight - 1);

    // Add number label on the right
    bar.append("text")
        .attr("class", "numlabel")
        .attr("x", function (d) {
            return party_x(d) + 3;
        })
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
        .text(function (d) {
            return d + "%";
        });

    // Draw labels
    bar.append("text")
        .attr("class", "label")
        .attr("x", function (d) {
            return -10;
        })
        .attr("y", groupHeight / 2)
        .attr("dy", "-.15em")
        .style("text-anchor", "end")
        .style("font", "14px sans-serif")
        .text(function (d, i) {
            return party_labels[i];
        });
}
function race_survey(data) {
    //race chart
    var race_labels = data["race"]["labels"];
    race_survey_data = data["race"]["values"];
    race_data=race_survey_data;
    var racechartHeight = barHeight * race_data.length * 3 + gapBetweenGroups * race_labels.length;
    race_x = d3.scale.linear()
        .domain([0, d3.max(race_data)])
        .range([0, chartWidth]);

    // Specify the chart area and dimensions
    var racechart = d3.select("#race_chart")
        .attr("width", spaceForLabels + chartWidth + spaceForLegend)
        .attr("height", racechartHeight);
    //bind elements to an empty array to get exit() part
    var race_update = racechart.selectAll("g")
        .data(emptyarray);
    race_update.exit().remove();
    // Create bars, bars contains text label on the left, rect in the middle and number labels on the right
    var bar = racechart.selectAll("g")
        .data(race_data)
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (i * groupHeight + gapBetweenGroups * (0.5 + i)  ) + ")";
        });

    // Create rectangles of the correct width
    bar.append("rect")
        .attr("fill", "#1f77b4")
        .attr("class", "bar")
        .attr("width", race_x)
        .attr("height", barHeight - 1);

    // Add number label on the right
    bar.append("text")
        .attr("class", "numlabel")
        .attr("x", function (d) {
            return race_x(d) + 3;
        })
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
        .text(function (d) {
            return d + "%";
        });

    // Draw labels
    bar.append("text")
        .attr("class", "label")
        .attr("x", function (d) {
            return -10;
        })
        .attr("y", groupHeight / 2)
        .attr("dy", "-.15em")
        .style("text-anchor", "end")
        .style("font", "14px sans-serif")
        .text(function (d, i) {
            return race_labels[i];
        });
}
function region_survey(data) {
//region chart

    var region_labels = data["region"]["labels"];
    region_survey_data = data["region"]["values"];
    region_data=region_survey_data;
    var regionchartHeight = barHeight * region_data.length * 3 + gapBetweenGroups * region_labels.length;
    region_x = d3.scale.linear()
        .domain([0, d3.max(region_data)])
        .range([0, chartWidth]);

    // Specify the chart area and dimensions
    var regionchart = d3.select("#region_chart")
        .attr("width", spaceForLabels + chartWidth + spaceForLegend)
        .attr("height", regionchartHeight);

    //bind elements to an empty array to get exit() part
    var region_update = regionchart.selectAll("g")
        .data(emptyarray);
    region_update.exit().remove();

    // Create bars, bars contains text label on the left, rect in the middle and number labels on the right
    var bar = regionchart.selectAll("g")
        .data(region_data)
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (i * groupHeight + gapBetweenGroups * (0.5 + i)  ) + ")";
        });

    // Create rectangles of the correct width
    bar.append("rect")
        .attr("fill", "#1f77b4")
        .attr("class", "bar")
        .attr("width", region_x)
        .attr("height", barHeight - 1);

    // Add number label on the right
    bar.append("text")
        .attr("class", "numlabel")
        .attr("x", function (d) {
            return region_x(d) + 3;
        })
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
        .text(function (d) {
            return d + "%";
        });

    // Draw labels
    bar.append("text")
        .attr("class", "label")
        .attr("x", function (d) {
            return -10;
        })
        .attr("y", groupHeight / 2)
        .attr("dy", "-.15em")
        .style("text-anchor", "end")
        .style("font", "14px sans-serif")
        .text(function (d, i) {
            return region_labels[i];
        });
}
function result(data) {
    //result chart
    var result_labels = data["result"]["labels"];
    result_data = data["result"]["values"];


    result_y = d3.scale.linear()
        .range([result_height, 0])
        .domain([0, d3.max(result_data)]);

    var result_chart = d3.select("#result_chart")
        .attr("width", result_width)
        .attr("height", result_height + 30)
        .attr("transform", function (d, i) {
            return "translate(60,0)";
        });

    var result_update = result_chart.selectAll("g").data(emptyarray);
    result_update.exit().remove();

    var result_bar = result_chart
        .selectAll("g")
        .data(result_data)
        .enter()
        .append("g")
        .attr("transform", function (d, i) {
            return "translate(" + i * result_barWidth * 2 + ",0)";
        })
        .attr("height", result_height);

    result_bar.append("rect")
        .attr("class","bar")
        .attr("y", function (d) {
            return result_y(d);
        })
        .attr("height", function (d) {
            return result_height - result_y(d);
        })
        .attr("width", result_barWidth - 5)
        .attr("fill", function (d, i) {
            if (i == 1) return "#3989cb"; else return "#d75c5c";
        });
    //draw percentage
    result_bar.append("text")
        .attr("class","numlabel")
        .attr("x", result_barWidth / 2)
        .attr("y", function (d) {
            return result_y(d) + 3;
        })
        .attr("dy", "1.5em")
        .attr("dx", "-1.1em")
        .text(function (d) {
            return d + "%";
        });
    //draw labels
    result_bar.append("text")
        .attr("x", result_barWidth / 2)
        .attr("y", result_height)
        .attr("dy", "1.5em").attr("dx", "-1.95em")
        .text(function (d, i) {
            return result_labels[i];
        });
}