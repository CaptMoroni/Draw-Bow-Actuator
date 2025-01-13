function makeCall(callData, url){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            machineData = JSON.parse(this.response)

            document.getElementById("r").value = machineData['r']
            document.getElementById("l").value = machineData['l']
            document.getElementById("p").value = machineData['x']
        }
    };
    //xhttp.open("GET", data.pyURL + "/command?var=4&c=54", true);
    xhttp.open("GET", "/" + url + "?data=" + JSON.stringify(callData), true)
    xhttp.send();
}
function SaveData(){
    console.log("Saving")
    let newData = {}
    
    let raw_1 = document.getElementById("raw_1").value
    let raw_2 = document.getElementById("raw_2").value
    let raw_3 = document.getElementById("raw_3").value
    let raw_4 = document.getElementById("raw_4").value

    let known_1 = document.getElementById("known_1").value
    let known_2 = document.getElementById("known_2").value
    let known_3 = document.getElementById("known_3").value
    let known_4 = document.getElementById("known_4").value

    newData = [
        [parseFloat(raw_1), parseFloat(known_1)],
        [parseFloat(raw_2), parseFloat(known_2)],
        [parseFloat(raw_3), parseFloat(known_3)],
        [parseFloat(raw_4), parseFloat(known_4)],
    ]

    console.log(newData)

    makeCall(newData,'saveCalibration')
}

function refreshData(){
    makeCall({},'mr')
}

//  Controll Logic
document.getElementById("refresh").onclick = refreshData
document.getElementById("save").onclick = SaveData

refreshData();