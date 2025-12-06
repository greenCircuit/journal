// fs: manipulate files
// const fs = require('fs');
// Or this way, like in jest...
// import fs from 'fs';

// // path: manipulate paths
// // const path = require('path');
// import path from 'path';

// const alerts = fs.readFileSync(
//   path.resolve('./data.json'),
//   {'encoding': 'utf-8'}
// );

const response = await fetch("data.json");
const data = await response.json();
// console.log(data);

// GLOBAL VARS
let startDate = "2020-01-01"
let endDate = "2040-01-01"
let stringSearch = "";

// GLOBAL NODES

const startDateFilter = document.getElementById("start-date");
const endDateFilter = document.getElementById("end-date");
const storyDiv = document.getElementById("story");


startDate = startDateFilter.addEventListener("change", (event) => {
    startDate = event.target.value;
    
    filterStart(startDate, endDate);
});

endDate = endDateFilter.addEventListener("change", (event) => {
    endDate = event.target.value;
    console.log(endDate)
    filterStart(startDate, endDate);
});

function filterStart(start_date="2020-01-01", end_date="2060-01-01") {
    storyDiv.innerHTML = '';
    console.log("Start date: " + start_date);
    console.log("End date: " + end_date);
    data.forEach(element => {
        console.log(startDate);
        let newStory = document.createElement('div');
        if (element.date_start > start_date && element.date_start < end_date) {
            newStory.innerHTML = element.date_start;
            storyDiv.appendChild(newStory);
        }
    })
};


filterStart("2020-01-01", "2060-01-01");
