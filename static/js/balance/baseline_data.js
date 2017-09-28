/**
 * Created by yz on 9/1/17.
 */
function edu_baseline(data) {
    //get new edu_data
    edu_baseline_data = data["edu"]["values"];
    edu_data = edu_survey_data.concat(edu_baseline_data);

    //re-compute edu scale
    edu_x = d3.scale.linear()
        .domain([0, d3.max(edu_data)])
        .range([0, chartWidth]);
    //get update selection
    var edu_update = d3.select("#edu_level_chart").selectAll("g").data(edu_data);

    //get enter selection
    var edu_enter = edu_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - edu_data.length / 2) + barHeight + gapBetweenGroups * (0.5 + (i - edu_data.length / 2)) ) + ")";
        });

    //create rects for new data
    edu_enter.append("rect")
        .attr("fill", function (d, i) {
            return "#aec7e8";
        })
        .attr("class", "bar")
        .attr("height", barHeight - 1);

    edu_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif");
    //update+enter
    d3.select("#edu_level_chart").selectAll(".bar").data(edu_data).attr("width", edu_x);
    d3.select("#edu_level_chart").selectAll(".numlabel").data(edu_data)
        .attr("x", function (d) {
            return edu_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });

}
function gender_baseline(data) {
    //get new gender_data
    gender_baseline_data = data["gender"]["values"];
    gender_data = gender_survey_data.concat(gender_baseline_data);

    //re-compute gender scale
    gender_x = d3.scale.linear()
        .domain([0, d3.max(gender_data)])
        .range([0, chartWidth]);
    //get update selection
    var gender_update = d3.select("#gender_chart").selectAll("g").data(gender_data);

    //get enter selection
    var gender_enter = gender_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - gender_data.length / 2) + barHeight + gapBetweenGroups * (0.5 + (i - gender_data.length / 2)) ) + ")";
        });

    //create rects for new data
    gender_enter.append("rect")
        .attr("fill", function (d, i) {
            return "#aec7e8";
        })
        .attr("class", "bar")
        .attr("height", barHeight - 1);

    gender_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif");
    //update+enter
    d3.select("#gender_chart").selectAll(".bar").data(gender_data).attr("width", gender_x);
    d3.select("#gender_chart").selectAll(".numlabel").data(gender_data)
        .attr("x", function (d) {
            return gender_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function age_baseline(data) {
    //get new age_data
    age_baseline_data = data["age"]["values"];
    age_data = age_survey_data.concat(age_baseline_data);

    //re-compute age scale
    age_x = d3.scale.linear()
        .domain([0, d3.max(age_data)])
        .range([0, chartWidth]);
    //get update selection
    var age_update = d3.select("#age_chart").selectAll("g").data(age_data);

    //get enter selection
    var age_enter = age_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - age_data.length / 2) + barHeight + gapBetweenGroups * (0.5 + (i - age_data.length / 2)) ) + ")";
        });

    //create rects for new data
    age_enter.append("rect")
        .attr("fill", function (d, i) {
            return "#aec7e8";
        })
        .attr("class", "bar")
        .attr("height", barHeight - 1);

    age_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif");
    //update+enter
    d3.select("#age_chart").selectAll(".bar").data(age_data).attr("width", age_x);
    d3.select("#age_chart").selectAll(".numlabel").data(age_data)
        .attr("x", function (d) {
            return age_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function region_baseline(data) {
    //get new region_data
    region_baseline_data = data["region"]["values"];
    region_data = region_survey_data.concat(region_baseline_data);

    //re-compute region scale
    region_x = d3.scale.linear()
        .domain([0, d3.max(region_data)])
        .range([0, chartWidth]);
    //get update selection
    var region_update = d3.select("#region_chart").selectAll("g").data(region_data);

    //get enter selection
    var region_enter = region_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - region_data.length / 2) + barHeight + gapBetweenGroups * (0.5 + (i - region_data.length / 2)) ) + ")";
        });

    //create rects for new data
    region_enter.append("rect")
        .attr("fill", function (d, i) {
            return "#aec7e8";
        })
        .attr("class", "bar")
        .attr("height", barHeight - 1);

    region_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif");
    //update+enter
    d3.select("#region_chart").selectAll(".bar").data(region_data).attr("width", region_x);
    d3.select("#region_chart").selectAll(".numlabel").data(region_data)
        .attr("x", function (d) {
            return region_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });

}
function hispanic_baseline(data) {

    //get new hispanic_data
    hispanic_baseline_data = data["hispanic"]["values"];
    hispanic_data = hispanic_survey_data.concat(hispanic_baseline_data);

    //re-compute hispanic scale
    hispanic_x = d3.scale.linear()
        .domain([0, d3.max(hispanic_data)])
        .range([0, chartWidth]);
    //get update selection
    var hispanic_update = d3.select("#hispanic_chart").selectAll("g").data(hispanic_data);

    //get enter selection
    var hispanic_enter = hispanic_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - hispanic_data.length / 2) + barHeight + gapBetweenGroups * (0.5 + (i - hispanic_data.length / 2)) ) + ")";
        });

    //create rects for new data
    hispanic_enter.append("rect")
        .attr("fill", function (d, i) {
            return "#aec7e8";
        })
        .attr("class", "bar")
        .attr("height", barHeight - 1);

    hispanic_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif");
    //update+enter
    d3.select("#hispanic_chart").selectAll(".bar").data(hispanic_data).attr("width", hispanic_x);
    d3.select("#hispanic_chart").selectAll(".numlabel").data(hispanic_data)
        .attr("x", function (d) {
            return hispanic_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });

}
function race_baseline(data) {

    //get new race_data
    race_baseline_data = data["race"]["values"];
    race_data = race_survey_data.concat(race_baseline_data);

    //re-compute race scale
    race_x = d3.scale.linear()
        .domain([0, d3.max(race_data)])
        .range([0, chartWidth]);
    //get update selection
    var race_update = d3.select("#race_chart").selectAll("g").data(race_data);

    //get enter selection
    var race_enter = race_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - race_data.length / 2) + barHeight + gapBetweenGroups * (0.5 + (i - race_data.length / 2)) ) + ")";
        });

    //create rects for new data
    race_enter.append("rect")
        .attr("fill", function (d, i) {
            return "#aec7e8";
        })
        .attr("class", "bar")
        .attr("height", barHeight - 1);

    race_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif");
    //update+enter
    d3.select("#race_chart").selectAll(".bar").data(race_data).attr("width", race_x);
    d3.select("#race_chart").selectAll(".numlabel").data(race_data)
        .attr("x", function (d) {
            return race_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function party_baseline(data) {
    //get new party_data
    party_baseline_data = data["party"]["values"];
    party_data = party_survey_data.concat(party_baseline_data);

    //re-compute party scale
    party_x = d3.scale.linear()
        .domain([0, d3.max(party_data)])
        .range([0, chartWidth]);
    //get update selection
    var party_update = d3.select("#party_chart").selectAll("g").data(party_data);

    //get enter selection
    var party_enter = party_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - party_data.length / 2) + barHeight + gapBetweenGroups * (0.5 + (i - party_data.length / 2)) ) + ")";
        });

    //create rects for new data
    party_enter.append("rect")
        .attr("fill", function (d, i) {
            return "#aec7e8";
        })
        .attr("class", "bar")
        .attr("height", barHeight - 1);

    party_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif");
    //update+enter
    d3.select("#party_chart").selectAll(".bar").data(party_data).attr("width", party_x);
    d3.select("#party_chart").selectAll(".numlabel").data(party_data)
        .attr("x", function (d) {
            return party_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function income_baseline(data) {
//get new income_data
    income_baseline_data = data["income"]["values"];
    income_data = income_survey_data.concat(income_baseline_data);

    //re-compute income scale
    income_x = d3.scale.linear()
        .domain([0, d3.max(income_data)])
        .range([0, chartWidth]);
    //get update selection
    var income_update = d3.select("#income_chart").selectAll("g").data(income_data);

    //get enter selection
    var income_enter = income_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - income_data.length / 2) + barHeight + gapBetweenGroups * (0.5 + (i - income_data.length / 2)) ) + ")";
        });

    //create rects for new data
    income_enter.append("rect")
        .attr("fill", function (d, i) {
            return "#aec7e8";
        })
        .attr("class", "bar")
        .attr("height", barHeight - 1);

    income_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif");
    //update+enter
    d3.select("#income_chart").selectAll(".bar").data(income_data).attr("width", income_x);
    d3.select("#income_chart").selectAll(".numlabel").data(income_data)
        .attr("x", function (d) {
            return income_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function political_view_baseline(data) {
    //get new political_view_data
    political_view_baseline_data = data["political_view"]["values"];
    political_view_data = political_view_survey_data.concat(political_view_baseline_data);

    //re-compute political_view scale
    political_view_x = d3.scale.linear()
        .domain([0, d3.max(political_view_data)])
        .range([0, chartWidth]);
    //get update selection
    var political_view_update = d3.select("#political_view_chart").selectAll("g").data(political_view_data);

    //get enter selection
    var political_view_enter = political_view_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - political_view_data.length / 2) + barHeight + gapBetweenGroups * (0.5 + (i - political_view_data.length / 2)) ) + ")";
        });

    //create rects for new data
    political_view_enter.append("rect")
        .attr("fill", function (d, i) {
            return "#aec7e8";
        })
        .attr("class", "bar")
        .attr("height", barHeight - 1);

    political_view_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif");
    //update+enter
    d3.select("#political_view_chart").selectAll(".bar").data(political_view_data).attr("width", political_view_x);
    d3.select("#political_view_chart").selectAll(".numlabel").data(political_view_data)
        .attr("x", function (d) {
            return political_view_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
$(document).ready(function () {
    $(".baseline_datasource").click(function () {
        $.post('/requestdata', {name: $(this).attr('value')}, function (data) {
            edu_baseline(data);
            gender_baseline(data);
            region_baseline(data);
            hispanic_baseline(data);
            age_baseline(data);
            race_baseline(data);
            party_baseline(data);
            income_baseline(data);
            political_view_baseline(data);

        });
    });
});