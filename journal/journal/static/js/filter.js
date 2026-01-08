// GLOBAL VARS
let startDate = "2020-01-01"
let endDate = "2040-01-01"
let stringSearch = "";

// GLOBAL NODES
const startDateFilter = document.getElementById("start-date-filter");
const endDateFilter = document.getElementById("end-date-filter");
const stringFilter = document.getElementById("word-filter");
const storyDiv = document.getElementById("story");


startDate = startDateFilter.addEventListener("change", (event) => {
    startDate = event.target.value;
    filterStart(startDate, endDate, stringSearch);
});

endDate = endDateFilter.addEventListener("change", (event) => {
    endDate = event.target.value;
    filterStart(startDate, endDate, stringSearch);
});

stringSearch = stringFilter.addEventListener("input", (event) => {
    stringSearch = event.target.value;
    filterStart(startDate, endDate, stringSearch);

});


function filterStart(start_date = "2020-01-01", end_date = "2060-01-01", stringSearch="") {
    let allStories = document.querySelectorAll(".entry");
    allStories.forEach(element => {
        let titleDate = element.querySelector(".title-date").innerHTML;
        let rawEntry = element.innerHTML.toLowerCase();
        let formaterDate = Date.parse(titleDate);

        if (formaterDate > Date.parse(start_date) && formaterDate< Date.parse(end_date) && rawEntry.includes(stringSearch)) {
            element.classList.remove("d-none");      
        } else {
            element.classList.add("d-none");
        }
    })
};


function getEntities(){
    let downloadBtn = document.getElementById('download-json');
    downloadBtn.addEventListener("click", (event) => {        
        const date = new Date().toDateString();
        downloadBtn.download = "journey "+date;
     })
}

getEntities();
filterStart("2020-01-01", "2040-01-01");