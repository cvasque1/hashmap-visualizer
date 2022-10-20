const operations = document.querySelectorAll(".operation")
const formDiv = document.querySelector(".form")
const button = document.querySelector("#formButton")
const keyField = document.querySelector(".key-field")
const valueField = document.querySelector(".value-field")
let currentOp = "insert"


function submit_entry() {
    let key = document.getElementById("key")
    let value = document.getElementById("value")
    console.log(currentOp)
    if (currentOp === "insert") {
        if (key.value === "" || value.value === "") {
            return;
        }
    } else if (currentOp === "delete") {
        if (key.value === "") {
            return;
        }
    }
    
    let entry = {
        key: key.value,
        value: value.value,
        op: currentOp
    }

    fetch(`${window.origin}/process`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
    .then(function(response) {
        if (response.status !== 200) {
            console.log(`Response status was not 200: ${response.status}`);
            return;
        }
        response.json().then(function(data) {
            console.log(data)
            if (data["op"] === "insert") {
                createBlock(data["hash"], data["key"], data["value"])
            } else if (data["op"] === "delete") {
                removeBlock(data["hash"], data["key"])
            } else {
                resetHashMap()
            }
            
        })
    })
}


operations.forEach((op) => {
    op.addEventListener('click', () => {
        createForm(op)
    })
})


function createForm(op) {
    currentOp = op.id   
    if (op.id === "insert") {
        keyField.style.display = ''
        valueField.style.display = ''
        button.style.display = ''
    } else if (op.id === "delete") {
        keyField.style.display = ''
        valueField.style.display = 'none'
        button.style.display = ''
    } else {
        keyField.style.display = 'none'
        valueField.style.display = 'none'
        button.style.display = 'none'
        submit_entry()
    }
    let key = document.getElementById("key")
    let value = document.getElementById("value")
    key.value = ""
    value.value = ""
}


function resetHashMap() {
    console.log("here")
    let blocks = document.querySelectorAll(".blocks .block")
    blocks.forEach((block) => {
        block.remove()
    })
}


function removeBlock(hash, key) {
    if (document.querySelector(`#b${hash+key}`) !== null) {
        let block = document.querySelector(`#b${hash+key}`)
        block.remove()
    }
}


function createBlock(hash, key, value) {
    // Check if entry doesn't exist
    if (document.querySelector(`#b${hash+key}`) !== null) {
        let entry = document.querySelector(`#b${hash+key} .value`)
        entry.textContent = value
        
    } else { // Entry does exist, so update value
        let blocks = document.querySelector(`#blocks${hash}`)

        let blockDiv = document.createElement("div")
        blockDiv.id = 'b'+hash+key
        blockDiv.classList.add("block")
        let arrowP = document.createElement("p")
        arrowP.classList.add("arrow")
        arrowP.textContent = " ===> "
        let keyValueDiv = document.createElement("div")
        keyValueDiv.classList.add("key-value")
        let keyP = document.createElement("p")
        keyP.textContent = `${key} |`
        keyP.classList.add("key")
        let valueP = document.createElement("p")
        valueP.textContent = value
        valueP.classList.add("value")

        keyValueDiv.appendChild(keyP)
        keyValueDiv.appendChild(valueP)
        blockDiv.appendChild(arrowP)
        blockDiv.appendChild(keyValueDiv)
        blocks.insertBefore(blockDiv, blocks.firstChild)
    }
    
}