
const createOption = (data)=> {
    const select = document.querySelector(".form-select");
    for (const i in data) {
        const opt = document.createElement("option");
        opt.setAttribute("value", data[i]);
        opt.innerText = i == "" ? "World Wide" : i
        select.appendChild(opt);
    }
}

const handleLiveTweets = (data)=> {

    const listContainer = document.querySelector('#live-tweets > ul');
    const content = document.createElement("li");
    content.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-start")
    content.innerHTML = `
        <div class="ms-2 me-auto"><div class="fw-bold">@${data.name}</div>${data.text}</div>
        <span class="badge bg-success">${data.time}</span>
    `
    listContainer.appendChild(content);
}

const place = document.querySelector(".place");
document.querySelector(".form-select").addEventListener("change", (e)=>{
    place.innerText = e.target.options[e.target.selectedIndex].text;
});

document.querySelector("#topic").addEventListener("keyup", (e)=> {
    let value = e.target.value;
    let values = [];
    const topics = document.querySelector("#topics");
    if (e.keyCode == 32) {
        values = value.split(" ").filter(v=> !v==" " && v)
        
        const tp = document.createElement('li')
        tp.classList.add("list-group-item")
        tp.innerText = values[values.length - 1];
        topics.append(tp);

    }
})


const initWS = (websocket) =>{
    websocket.addEventListener("open", ()=>{
        let data = {"type":"open"}
        websocket.send(JSON.stringify(data))
    })
}

const receiveMessages =  (websocket)=> {
    websocket.addEventListener("message", ({ data })=> {
        const parsedData = JSON.parse(data);
        switch(parsedData.type){
            case "places":
                localStorage.setItem("places",JSON.stringify(parsedData.places))
                createOption(parsedData.places)
                break;
            case "tweets":
                handleLiveTweets(parsedData)
                break;
        }

    });
}

window.addEventListener("DOMContentLoaded", ()=> {
    const body = document.querySelector("#body")
    // create ws
    const websocket = new WebSocket("ws://localhost:8001/");
    initWS(websocket);
    receiveMessages(websocket);
});