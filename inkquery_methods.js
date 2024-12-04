
function fetchData(word, langType = 'English intermediate') {

    const dictCodes = {
        "English intermediate": "sd3", "English elementary": "sd2", "English collegiate": "collegiate", "Spanish": "spanish"
    };

    const dictKeys = {
        "English intermediate": "a19c9426-51cf-4c68-af55-de3b8229f559",
        "English elementary": "e59d86cd-4e68-4ffc-a389-9945b19a1f32",
        "English collegiate": "95da4924-31ba-4752-b070-f434ec41a1ba",
        "Spanish": "a29aabe7-82a8-4c85-8e27-3b0bb0d722d8"
    };


    /*
    const Languages = [
        "English intermediate",
        "English elementary",
        "English collegiate",
        "Spanish",
        "Japanese",
        "Russian",
        "German",
        "French",
        "Swedish",
        "Dutch",
        "Hungarian",
        "Slovenian",
    ];

    const dicTypes = {
        "MerriamW":`https://dictionaryapi.com/api/v3/references/${dictCodes[langType]}/json/${word}?key=${dictKeys[langType]}`,
        "Jotoba": `https://jotoba.de/api/search/words`
    };

    cost urlSelection = Object.fromEntries(Languages.map(field => [field, dicTypes[1]]));
    dicTypes["English intermediate"] = dicTypes["English elementary"] = dicTypes["English collegiate"] = dicTypes["Spanish"] = dicTypes[0];


    */

    const urlSelection = {
        //Spanish & English
        "Spanish": `https://dictionaryapi.com/api/v3/references/${dictCodes[langType]}/json/${word}?key=${dictKeys[langType]}`,
        "English elementary": `https://dictionaryapi.com/api/v3/references/${dictCodes[langType]}/json/${word}?key=${dictKeys[langType]}`,
        "English intermediate": `https://dictionaryapi.com/api/v3/references/${dictCodes[langType]}/json/${word}?key=${dictKeys[langType]}`,
        "English collegiate": `https://dictionaryapi.com/api/v3/references/${dictCodes[langType]}/json/${word}?key=${dictKeys[langType]}`,
        //Japanese/German/Russain/Swedish/French/Dutch/Hungarian/Slovenian
        //Note: Also includes Spanish
        "Japanese": `https://jotoba.de/api/search/words`,
        "Russian": `https://jotoba.de/api/search/words`,
        "German": `https://jotoba.de/api/search/words`,
        "French": `https://jotoba.de/api/search/words`,
        "Swedish": `https://jotoba.de/api/search/words`,
        "Dutch": `https://jotoba.de/api/search/words`,
        "Hungarian": `https://jotoba.de/api/search/words`,
        "Slovenian": `https://jotoba.de/api/search/words`
    };

    const url = `${urlSelection[langType]}`;
    const queryLoad = {
        query: `${word}`,
        language: `${langType}`,
        no_english: false //DO NOT CHANGE
    };
    
    
    
    if( langType == "Japanese" || 
        langType == "Russian" ||
        langType == "German" ||
        langType == "French" ||
        langType == "Swedish" ||
        langType == "Dutch" ||
        langType == "Hungarian" ||
        langType == "Slovenian"
    ) { 
        return fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(queryLoad)
        }).then(response => {
            if (!response.ok) {
                console.error("Response not ok");
                throw new Error(response.status);
            }
            return response.json()
        })
        .catch(error => {
            console.error("Error fetching")
            console.error(error);
            throw error;
        });
    } else {
        return fetch(url)
        .then(response => {
            if (!response.ok) {
                console.error("Response not ok");
                throw new Error(response.status);
            }
            return response.json()
        })
        .catch(error => {
            console.error("Error fetching")
            console.error(error);
            throw error;
        });
    }
   
}

export function wm_getDef(word, langType = 'English intermediate') {
    return fetchData(word, langType)
    .then(data => {
        if( langType == "Japanese" || 
            langType == "Russian" ||
            langType == "German" ||
            langType == "French" ||
            langType == "Swedish" ||
            langType == "Dutch" ||
            langType == "Hungarian" ||
            langType == "Slovenian"
        ) {
            const dta = data.words[0].senses;
            const keys = Object.keys(dta);
            const lastKey = keys[keys.length - 1];
            console.log(dta[lastKey].glosses[0]);
            return dta[lastKey].glosses[0];
        } else {
            console.log(data[0].shortdef[0]);
            return data[0].shortdef[0];
        }
        
        
    })
    .catch(error => console.error(error));
}

export function fetchPicture(word) {
    const url = `https://pixabay.com/api/?key=47380368-f08bf6fd37b056b31201b5932&q=${word}&image_type=photo`

    return fetch(url)
    .then(response => {
        if (!response.ok) {
            console.error("Response not ok");
            throw new Error(response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.hits && data.hits.length > 0) {
            const imageURL = data.hits[0].largeImageURL;
            return imageURL
            // return fetch(imageURL)
            //     .then(imageResponse => {
            //         if (!imageResponse.ok) {
            //             console.error("Failed to fetch image");
            //             throw new Error(imageResponse.status);
            //         }
            //         return imageResponse.blob();
            //     });
        }
        else {
            console.error("No image found for word");
            throw new Error("No image found for word")
        }
    })
    .catch(error => {
        console.error("Error fetching from Pixabay: ", error);
        throw error;
    });
}

// let test = await fetchPicture("car");
// console.log(test.hits[0].largeImageURL);

// fetch(url)
//     .then(response => {
//         if (!response.ok) {
//             throw new Error(response.statusText);
//         }
//         return response.json()
//     })
//     .then(data => console.log(data))
//     .catch(error => console.error(error))

// async function fetchData(){
//
//     try{
//         const response = await fetch(url);
//         if (!response.ok) {
//             throw new Error(response.statusText);
//         }
//
//         const data = await response.json();
//         console.log(data);
//     }
//     catch(error){
//         console.error(error);
//     }
//
// }
