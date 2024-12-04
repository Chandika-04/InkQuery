import {wm_getDef, fetchPicture} from "./inkquery_methods.js"


document.getElementById("wordButton").onclick = async function() {

    const intermediateBtn = document.getElementById("intermediateBtn");
    const elementaryBtn = document.getElementById("elementaryBtn");
    const collegiateBtn = document.getElementById("collegiateBtn");
    const spanishBtn = document.getElementById("spanishBtn");

    let checkedBtnInput = "English intermediate";

    if (intermediateBtn.checked){
        checkedBtnInput = "English intermediate";
    } else if (elementaryBtn.checked){
        checkedBtnInput = "English elementary";
    } else if (collegiateBtn.checked){
        checkedBtnInput = "English collegiate";
    } else if (spanishBtn.checked){
        checkedBtnInput = "Spanish";
    } else if (japaneseBtn.checked){
        checkedBtnInput = "Japanese";
    } else if (russianBtn.checked){
        checkedBtnInput = "Russian";
    }else if (germanBtn.checked){
        checkedBtnInput = "German";
    } else if (frenchBtn.checked){
        checkedBtnInput = "French";
    } else if (swedishBtn.checked){
        checkedBtnInput = "Swedish";
    } else if (dutchBtn.checked){
        checkedBtnInput = "Dutch";
    } else if (hungarianBtn.checked){
        checkedBtnInput = "Hungarian";
    } else if (slovenianBtn.checked){
        checkedBtnInput = "Slovenian";
    }

    console.log(checkedBtnInput);

    const wordLabel = document.getElementById("wordIn").value;
    document.getElementById("yourWordLabel").textContent = wordLabel;

    try {
        const wordDef = await wm_getDef(wordLabel, checkedBtnInput);
        const outputImg = await fetchPicture(wordLabel);
        document.getElementById("defLabel").textContent = wordDef;
        document.getElementById("outputImg").src = outputImg;
    }
    catch(error) {
        console.error("Error fetching definition", error);
        document.getElementById("defLabel").textContent = "Error displaying definition.";
    }

    // window.location.href = "Drawing_App.html";
}



