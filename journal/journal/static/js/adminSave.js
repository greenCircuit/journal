// saving stuff when click save btn on admin page
const saveBtns = document.querySelector('.submit-row');

// creates fake ling and triggers file trigger
function saveTemplateAsFile(fileName) {
    const link = document.createElement("a");
    link.download = fileName;
    link.href='/api/journey/get_story?format=json'
    link.innerHTML ="test";
    console.log('here');
    console.log(link);
    link.click();
};

// saving everything
saveBtns.addEventListener("click", (event) => {
       const date = new Date().toISOString().slice(0, 10);
        let downloadName = "journey_"+ date + "";
        saveTemplateAsFile(downloadName)



})

saveBtns.appendChild(link);