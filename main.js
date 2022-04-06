// function initWS(websocket){
//     websocket.addEventListener("open", ()=>{

//     })
// }

const createOption = (data)=> {
    const select = document.querySelector(".form-select");
    for (const i in data) {
        const opt = document.createElement("option");
        opt.setAttribute("value", data[i]);
        opt.innerText = i == "" ? "World Wide" : i
        select.appendChild(opt);
    }
}

function receiveMessages(websocket){
    websocket.addEventListener("message", ({ data })=> {
        const parsedData = JSON.parse(data);
        switch(parsedData.type){
            case "places":
                createOption(parsedData.places)
                break;
            case "tweets":
                console.log(parsedData.tweets)
                break;
        }

    });
}

window.addEventListener("DOMContentLoaded", ()=> {

    // create ws
    const websocket = new WebSocket("ws://localhost:8001/");
    receiveMessages(websocket);
});

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