// from data.js
var tableData = data;
var tbody = d3.select("tbody");
// // YOUR CODE HERE!
// * Using the UFO dataset provided in the form of an array of JavaScript objects, write code that appends a table to your web page and then adds new rows of data for each UFO sighting.

//   * Make sure you have a column for `date/time`, `city`, `state`, `country`, `shape`, and `comment` at the very least.

// * Use a date form in your HTML document and write JavaScript code that will listen for events and search through the `date/time` column to find rows that match user input.

function update1(newData) {
    newData.forEach(function (UFO_Sighting) {
        var row = tbody.append("tr");
        Object.values(UFO_Sighting).forEach(function (value) {
            console.log(value);
            var cell = tbody.append("td");
            cell.text(value);
        });
    })
};

update1(data);


d3.select('#filter-btn').on("click", function () {
    var selectDate = d3.select('#datetime').property("value");
    var newData = data.filter(row => row.datetime == selectDate);
    update1(newData)
});





