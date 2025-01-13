function makeCall(callData, url){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            machineData = JSON.parse(this.response)

            document.getElementById("SSID").value = machineData['SSID']
            document.getElementById("PASSWORD").value = machineData['PASSWORD']
            document.getElementById("load_cell_value_1").value = machineData['load_cell_value_1']
            document.getElementById("load_cell_weight_1").value = machineData['load_cell_weight_1']
            document.getElementById("load_cell_value_2").value = machineData['load_cell_value_2']
            document.getElementById("load_cell_weight_2").value = machineData['load_cell_weight_2']
            document.getElementById("sampleRate").value = machineData['sampleRate']
        }
    };
    //xhttp.open("GET", data.pyURL + "/command?var=4&c=54", true);
    xhttp.open("GET", "/" + url + "?data=" + JSON.stringify(callData), true)
    xhttp.send();
}
function SaveData(){
    let newData = {}
    
    let SSID = document.getElementById("SSID").value
    let PASSWORD = document.getElementById("PASSWORD").value
    let load_cell_value_1 = document.getElementById("load_cell_value_1").value
    let load_cell_weight_1 = document.getElementById("load_cell_weight_1").value
    let load_cell_value_2 = document.getElementById("load_cell_value_2").value
    let load_cell_weight_2 = document.getElementById("load_cell_weight_2").value
    let sampleRate = document.getElementById("sampleRate").value

    newData['SSID'] = SSID
    newData['PASSWORD'] = PASSWORD
    newData['load_cell_value_1'] = parseFloat(load_cell_value_1)
    newData['load_cell_weight_1'] = parseFloat(load_cell_weight_1)
    newData['load_cell_value_2'] = parseFloat(load_cell_value_2)
    newData['load_cell_weight_2'] = parseFloat(load_cell_weight_2)
    newData['sampleRate'] = parseInt(sampleRate)

    makeCall(newData,'saveSettings')
}

function getSettings(){
    makeCall({},'getSettings')
}

//  Controll Logic
document.getElementById("save").onclick = SaveData

getSettings();