/**
 * Created by yz on 9/15/17.
 */
$(document).ready(function () {
    $("input.slider").bootstrapSlider();

    $('#ex1').bootstrapSlider({
        formatter: function (value) {
            return value + '%';
        }
    });

    $("input.slider").on("slide", function (slideEvt) {
        $.post('/dobalance', {percentage: slideEvt.value, balancebylist: $(".balance_by").text()}, function (data) {
            edu_balance(slideEvt.value);
            gender_balance(slideEvt.value);
            region_balance(slideEvt.value);
            hispanic_balance(slideEvt.value);
            age_balance(slideEvt.value);
            race_balance(slideEvt.value);
            party_balance(slideEvt.value);
            income_balance(slideEvt.value);
            political_view_balance(slideEvt.value);
            result_balance(data);


        });
    });
});

function edu_balance(percentage) {
    //if in balance list
    if ($(".balance_by").text().indexOf("Last Grade in School") !== -1) {
        var edu_balance_data = [];
        for (i = 0; i < edu_survey_data.length; i++) {
            edu_balance_data.push(Math.round(edu_survey_data[i] + (edu_baseline_data[i] - edu_survey_data[i]) * percentage / 100));
        }
    }
    //if not in balance list
    else {
        var edu_balance_data = edu_survey_data;
    }
    //update array
    edu_data = edu_survey_data.concat(edu_balance_data.concat(edu_baseline_data));
    //update selection
    var edu_update = d3.select("#edu_level_chart").selectAll("g").data(edu_data);

    //get enter selection
    var edu_enter = edu_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - edu_survey_data.length * 2) + 2 * barHeight + gapBetweenGroups * (0.5 + (i - edu_survey_data.length * 2)) ) + ")";
        });
    //create rects for new data
    edu_enter.append("rect")
        .attr("class", "bar")
        .attr("height", barHeight - 1);
    //create number labels for new data
    edu_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
    ;
    //change attributes for all elements
    d3.select("#edu_level_chart").selectAll(".bar").data(edu_data)
        .attr("fill", function (d, i) {
            if (i < edu_survey_data.length) return "#1f77b4";
            else if (i < edu_survey_data.length * 2) return "#5AC2C6";
            else return "#aec7e8";
        })
        .attr("width", edu_x);
    d3.select("#edu_level_chart").selectAll(".numlabel").data(edu_data)
        .attr("x", function (d) {
            return edu_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function gender_balance(percentage) {
    //if in balance list
    if ($(".balance_by").text().indexOf("Gender") !== -1) {
        var gender_balance_data = [];
        for (i = 0; i < gender_survey_data.length; i++) {
            gender_balance_data.push(Math.round(gender_survey_data[i] + (gender_baseline_data[i] - gender_survey_data[i]) * percentage / 100));
        }
    }
    //if not in balance list
    else {
        var gender_balance_data = gender_survey_data;
    }
    //update array
    gender_data = gender_survey_data.concat(gender_balance_data.concat(gender_baseline_data));
    //update selection
    var gender_update = d3.select("#gender_chart").selectAll("g").data(gender_data);

    //get enter selection
    var gender_enter = gender_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - gender_survey_data.length * 2) + 2 * barHeight + gapBetweenGroups * (0.5 + (i - gender_survey_data.length * 2)) ) + ")";
        });
    //create rects for new data
    gender_enter.append("rect")
        .attr("class", "bar")
        .attr("height", barHeight - 1);
    //create number labels for new data
    gender_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
    ;
    //change attributes for all elements
    d3.select("#gender_chart").selectAll(".bar").data(gender_data)
        .attr("fill", function (d, i) {
            if (i < gender_survey_data.length) return "#1f77b4";
            else if (i < gender_survey_data.length * 2) return "#5AC2C6";
            else return "#aec7e8";
        })
        .attr("width", gender_x);
    d3.select("#gender_chart").selectAll(".numlabel").data(gender_data)
        .attr("x", function (d) {
            return gender_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function region_balance(percentage) {
    //if in balance list
    if ($(".balance_by").text().indexOf("Region") !== -1) {
        var region_balance_data = [];
        for (i = 0; i < region_survey_data.length; i++) {
            region_balance_data.push(Math.round(region_survey_data[i] + (region_baseline_data[i] - region_survey_data[i]) * percentage / 100));
        }
    }
    //if not in balance list
    else {
        var region_balance_data = region_survey_data;
    }
    //update array
    region_data = region_survey_data.concat(region_balance_data.concat(region_baseline_data));
    //update selection
    var region_update = d3.select("#region_chart").selectAll("g").data(region_data);

    //get enter selection
    var region_enter = region_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - region_survey_data.length * 2) + 2 * barHeight + gapBetweenGroups * (0.5 + (i - region_survey_data.length * 2)) ) + ")";
        });
    //create rects for new data
    region_enter.append("rect")
        .attr("class", "bar")
        .attr("height", barHeight - 1);
    //create number labels for new data
    region_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
    ;
    //change attributes for all elements
    d3.select("#region_chart").selectAll(".bar").data(region_data)
        .attr("fill", function (d, i) {
            if (i < region_survey_data.length) return "#1f77b4";
            else if (i < region_survey_data.length * 2) return "#5AC2C6";
            else return "#aec7e8";
        })
        .attr("width", region_x);
    d3.select("#region_chart").selectAll(".numlabel").data(region_data)
        .attr("x", function (d) {
            return region_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function hispanic_balance(percentage) {
    //if in balance list
    if ($(".balance_by").text().indexOf("Latino or Hispanic Oringin") !== -1) {
        var hispanic_balance_data = [];
        for (i = 0; i < hispanic_survey_data.length; i++) {
            hispanic_balance_data.push(Math.round(hispanic_survey_data[i] + (hispanic_baseline_data[i] - hispanic_survey_data[i]) * percentage / 100));
        }
    }
    //if not in balance list
    else {
        var hispanic_balance_data = hispanic_survey_data;
    }
    //update array
    hispanic_data = hispanic_survey_data.concat(hispanic_balance_data.concat(hispanic_baseline_data));
    //update selection
    var hispanic_update = d3.select("#hispanic_chart").selectAll("g").data(hispanic_data);

    //get enter selection
    var hispanic_enter = hispanic_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - hispanic_survey_data.length * 2) + 2 * barHeight + gapBetweenGroups * (0.5 + (i - hispanic_survey_data.length * 2)) ) + ")";
        });
    //create rects for new data
    hispanic_enter.append("rect")
        .attr("class", "bar")
        .attr("height", barHeight - 1);
    //create number labels for new data
    hispanic_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
    ;
    //change attributes for all elements
    d3.select("#hispanic_chart").selectAll(".bar").data(hispanic_data)
        .attr("fill", function (d, i) {
            if (i < hispanic_survey_data.length) return "#1f77b4";
            else if (i < hispanic_survey_data.length * 2) return "#5AC2C6";
            else return "#aec7e8";
        })
        .attr("width", hispanic_x);
    d3.select("#hispanic_chart").selectAll(".numlabel").data(hispanic_data)
        .attr("x", function (d) {
            return hispanic_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function age_balance(percentage) {
    //if in balance list
    if ($(".balance_by").text().indexOf("Age") !== -1) {
        var age_balance_data = [];
        for (i = 0; i < age_survey_data.length; i++) {
            age_balance_data.push(Math.round(age_survey_data[i] + (age_baseline_data[i] - age_survey_data[i]) * percentage / 100));
        }
    }
    //if not in balance list
    else {
        var age_balance_data = age_survey_data;
    }
    //update array
    age_data = age_survey_data.concat(age_balance_data.concat(age_baseline_data));
    //update selection
    var age_update = d3.select("#age_chart").selectAll("g").data(age_data);

    //get enter selection
    var age_enter = age_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - age_survey_data.length * 2) + 2 * barHeight + gapBetweenGroups * (0.5 + (i - age_survey_data.length * 2)) ) + ")";
        });
    //create rects for new data
    age_enter.append("rect")
        .attr("class", "bar")
        .attr("height", barHeight - 1);
    //create number labels for new data
    age_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
    ;
    //change attributes for all elements
    d3.select("#age_chart").selectAll(".bar").data(age_data)
        .attr("fill", function (d, i) {
            if (i < age_survey_data.length) return "#1f77b4";
            else if (i < age_survey_data.length * 2) return "#5AC2C6";
            else return "#aec7e8";
        })
        .attr("width", age_x);
    d3.select("#age_chart").selectAll(".numlabel").data(age_data)
        .attr("x", function (d) {
            return age_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function race_balance(percentage) {
    //if in balance list
    if ($(".balance_by").text().indexOf("Race") !== -1) {
        var race_balance_data = [];
        for (i = 0; i < race_survey_data.length; i++) {
            race_balance_data.push(Math.round(race_survey_data[i] + (race_baseline_data[i] - race_survey_data[i]) * percentage / 100));
        }
    }
    //if not in balance list
    else {
        var race_balance_data = race_survey_data;
    }
    //update array
    race_data = race_survey_data.concat(race_balance_data.concat(race_baseline_data));
    //update selection
    var race_update = d3.select("#race_chart").selectAll("g").data(race_data);

    //get enter selection
    var race_enter = race_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - race_survey_data.length * 2) + 2 * barHeight + gapBetweenGroups * (0.5 + (i - race_survey_data.length * 2)) ) + ")";
        });
    //create rects for new data
    race_enter.append("rect")
        .attr("class", "bar")
        .attr("height", barHeight - 1);
    //create number labels for new data
    race_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
    ;
    //change attributes for all elements
    d3.select("#race_chart").selectAll(".bar").data(race_data)
        .attr("fill", function (d, i) {
            if (i < race_survey_data.length) return "#1f77b4";
            else if (i < race_survey_data.length * 2) return "#5AC2C6";
            else return "#aec7e8";
        })
        .attr("width", race_x);
    d3.select("#race_chart").selectAll(".numlabel").data(race_data)
        .attr("x", function (d) {
            return race_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function party_balance(percentage) {
    //if in balance list
    if ($(".balance_by").text().indexOf("Party") !== -1) {
        var party_balance_data = [];
        for (i = 0; i < party_survey_data.length; i++) {
            party_balance_data.push(Math.round(party_survey_data[i] + (party_baseline_data[i] - party_survey_data[i]) * percentage / 100));
        }
    }
    //if not in balance list
    else {
        var party_balance_data = party_survey_data;
    }
    //update array
    party_data = party_survey_data.concat(party_balance_data.concat(party_baseline_data));
    //update selection
    var party_update = d3.select("#party_chart").selectAll("g").data(party_data);

    //get enter selection
    var party_enter = party_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - party_survey_data.length * 2) + 2 * barHeight + gapBetweenGroups * (0.5 + (i - party_survey_data.length * 2)) ) + ")";
        });
    //create rects for new data
    party_enter.append("rect")
        .attr("class", "bar")
        .attr("height", barHeight - 1);
    //create number labels for new data
    party_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
    ;
    //change attributes for all elements
    d3.select("#party_chart").selectAll(".bar").data(party_data)
        .attr("fill", function (d, i) {
            if (i < party_survey_data.length) return "#1f77b4";
            else if (i < party_survey_data.length * 2) return "#5AC2C6";
            else return "#aec7e8";
        })
        .attr("width", party_x);
    d3.select("#party_chart").selectAll(".numlabel").data(party_data)
        .attr("x", function (d) {
            return party_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function income_balance(percentage) {
    //if in balance list
    if ($(".balance_by").text().indexOf("Annual Family Income") !== -1) {
        var income_balance_data = [];
        for (i = 0; i < income_survey_data.length; i++) {
            income_balance_data.push(Math.round(income_survey_data[i] + (income_baseline_data[i] - income_survey_data[i]) * percentage / 100));
        }
    }
    //if not in balance list
    else {
        var income_balance_data = income_survey_data;
    }
    //update array
    income_data = income_survey_data.concat(income_balance_data.concat(income_baseline_data));
    //update selection
    var income_update = d3.select("#income_chart").selectAll("g").data(income_data);

    //get enter selection
    var income_enter = income_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - income_survey_data.length * 2) + 2 * barHeight + gapBetweenGroups * (0.5 + (i - income_survey_data.length * 2)) ) + ")";
        });
    //create rects for new data
    income_enter.append("rect")
        .attr("class", "bar")
        .attr("height", barHeight - 1);
    //create number labels for new data
    income_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
    ;
    //change attributes for all elements
    d3.select("#income_chart").selectAll(".bar").data(income_data)
        .attr("fill", function (d, i) {
            if (i < income_survey_data.length) return "#1f77b4";
            else if (i < income_survey_data.length * 2) return "#5AC2C6";
            else return "#aec7e8";
        })
        .attr("width", income_x);
    d3.select("#income_chart").selectAll(".numlabel").data(income_data)
        .attr("x", function (d) {
            return income_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function political_view_balance(percentage) {
    //if in balance list
    if ($(".balance_by").text().indexOf("Political View") !== -1) {
        var political_view_balance_data = [];
        for (i = 0; i < political_view_survey_data.length; i++) {
            political_view_balance_data.push(Math.round(political_view_survey_data[i] + (political_view_baseline_data[i] - political_view_survey_data[i]) * percentage / 100));
        }
    }
    //if not in balance list
    else {
        var political_view_balance_data = political_view_survey_data;
    }
    //update array
    political_view_data = political_view_survey_data.concat(political_view_balance_data.concat(political_view_baseline_data));
    //update selection
    var political_view_update = d3.select("#political_view_chart").selectAll("g").data(political_view_data);

    //get enter selection
    var political_view_enter = political_view_update.enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (groupHeight * (i - political_view_survey_data.length * 2) + 2 * barHeight + gapBetweenGroups * (0.5 + (i - political_view_survey_data.length * 2)) ) + ")";
        });
    //create rects for new data
    political_view_enter.append("rect")
        .attr("class", "bar")
        .attr("height", barHeight - 1);
    //create number labels for new data
    political_view_enter.append("text")
        .attr("class", "numlabel")
        .attr("y", barHeight / 2)
        .attr("fill", "grey")
        .attr("dy", ".35em")
        .style("font", "10px sans-serif")
    ;
    //change attributes for all elements
    d3.select("#political_view_chart").selectAll(".bar").data(political_view_data)
        .attr("fill", function (d, i) {
            if (i < political_view_survey_data.length) return "#1f77b4";
            else if (i < political_view_survey_data.length * 2) return "#5AC2C6";
            else return "#aec7e8";
        })
        .attr("width", political_view_x);
    d3.select("#political_view_chart").selectAll(".numlabel").data(political_view_data)
        .attr("x", function (d) {
            return political_view_x(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });
}
function result_balance(data) {
    //update result data
    result_data = data["values"];
    //update scale
    result_y = d3.scale.linear()
        .range([result_height, 0])
        .domain([0, d3.max(result_data)]);
    //bind elements with new data
    d3.select("#result_chart").selectAll("g")
        .data(result_data)
        .enter()
        .append("g")
        .attr("transform", function (d, i) {
            return "translate(" + i * result_barWidth * 2 + ",0)";
        })
        .attr("height", result_height);
    d3.select("#result_chart").selectAll(".bar").data(result_data)
        .attr("y",result_y)
        .attr("height", function (d) {
            return result_height - result_y(d);
        });
    d3.select("#result_chart").selectAll(".numlabel").data(result_data)
        .attr("y", function (d) {
            return result_y(d) + 3;
        })
        .text(function (d) {
            return d + "%";
        });

}

