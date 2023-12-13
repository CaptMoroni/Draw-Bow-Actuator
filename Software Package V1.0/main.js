
pyData = '{"piURL":"192.1.1.1", "count":42}'
data = JSON.parse(pyData)
let x = 0
let l = 0
let maxX = 30
let clickIncrament = 0.10
let systemLock = false

function makeCall(callData, url){
    if (!systemLock){
        lock()
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                machineData = JSON.parse(this.response)
                x = machineData["x"]
                l = machineData["l"]
                loadText = document.getElementById("currentLoadText")
                loadText.innerHTML = l + " lbf"
                log("machine response: </br> position: " + x + ", load: " + l, 1)
                renderPos(x)
                toggleLock()
            }
        };
        //xhttp.open("GET", data.pyURL + "/command?var=4&c=54", true);
        xhttp.open("GET", "/" + url + "?data=" + JSON.stringify(callData), true)
        xhttp.send();
    }else{
        log("ERROR: System Locked")
    }
}
function log(text, c){
    console.log(text)
    oldHTML = document.getElementById("dataCommands").innerHTML
    if (c){
        document.getElementById("dataCommands").innerHTML = "<p style='background:#1d6f90;color:#fff;'>" + text + "</p>" + oldHTML
    }else{
        document.getElementById("dataCommands").innerHTML = "<p>" + text + "</p>" + oldHTML
    }
}
function renderPos( newPos ){
    posElement = document.getElementById("currentPosHeight")
    loadText = document.getElementById("currentLoadText")
    posText = document.getElementById("currentPosText")
    inputGoTo = document.getElementById("goToInput")
    positionFill = document.getElementById("positionFill")

    posText.innerHTML = Math.round(newPos*100)/100 + " in"
    inputGoTo.value = Math.round(newPos*10000)/10000
    
    newPos = Math.min(Math.max(newPos, 0),maxX)
    let percentage = (1-newPos/maxX)*100.0
    posElement.style.top = percentage + "%"
    positionFill.style = "height:" + percentage + "%"
}
function stepSizeLarge(){
    log("Set Step Size: Large")
    clickIncrament = 1
    document.getElementById("setStepLarge").classList.add('selected')
    document.getElementById("setStepMedium").classList.remove('selected')
    document.getElementById("setStepSmall").classList.remove('selected')
}
function stepSizeMedium(){
    log("Set Step Size: Medium");
    clickIncrament = 0.1
    document.getElementById("setStepMedium").classList.add('selected')
    document.getElementById("setStepLarge").classList.remove('selected')
    document.getElementById("setStepSmall").classList.remove('selected')
}
function stepSizeSmall(){
    log("Set Step Size: Small");
    clickIncrament = 0.01
    document.getElementById("setStepSmall").classList.add('selected')
    document.getElementById("setStepMedium").classList.remove('selected')
    document.getElementById("setStepLarge").classList.remove('selected')
}
function goUp(){
    log("Moving Up");
    x += clickIncrament
    makeCall({"c":"to","x":x},'c')
}
function goDown(){
    log("Moving Down")
    x -= clickIncrament
    makeCall({"c":"to","x":x},'c')
}
function setTare(){
    log("Taring Load Cell")
    makeCall({"c":"to","x":x},'setTare')
}
function setZero(){
    log("Setting Current Position to Zero")
    makeCall({"c":"to","x":x},'setZero')
}
function goTo(){
    log('go to')
    let newPos = document.getElementById("goToInput").value
    x = parseFloat(newPos)
    makeCall({"c":"to","x":x},'c')
}
function run(){
    log('Running: Please Wait')
    let runHeight = document.getElementById("runInput").value
    x = parseFloat(runHeight)
    makeCall({"c":"run","x":x},'c')
}
function getMachineStatus(){
    makeCall({"c":"run","x":x},'m')
}
function updateGraph(){
    var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                csvData = this.response.toString()
                csvData = csvData.split('\n')
                console.log(csvData)
                let xValues = [];
                let yValues = [];
                for (let i = 0; i < csvData.length-1; i++) {
                    lineData = csvData[i+1]
                    console.log(lineData)
                    lineData = lineData.split(",")
                    xValues.push(parseFloat(lineData[0]));
                    yValues.push(parseFloat(lineData[1]));
                }
                const data = [{x:xValues, y:yValues, mode:"lines"}];
                const layout = {title: "Test Data"};
                Plotly.newPlot("graph", data, layout);
            }
        };
        xhttp.open("GET", "/testData.csv", true)
        xhttp.send();
}
function lock(){
    systemLock = true
    document.getElementById("toggleLock").innerHTML = "Locked"
    document.getElementById("toggleLock").classList.add('red')
}
function toggleLock(){
    if (systemLock){
        console.log('unlocking')
        systemLock = false
        document.getElementById("toggleLock").innerHTML = "Lock"
        document.getElementById("toggleLock").classList.remove('red')
    }else{
        console.log('locking')
        systemLock = true
        document.getElementById("toggleLock").innerHTML = "Locked"
        document.getElementById("toggleLock").classList.add('red')
    }
}

//  Controll Logic
document.getElementById("buttonUP").onclick = goUp
document.getElementById("buttonDown").onclick = goDown
document.getElementById("buttonZero").onclick = setZero
document.getElementById("buttonTare").onclick = setTare
document.getElementById("setStepLarge").onclick = stepSizeLarge
document.getElementById("setStepMedium").onclick = stepSizeMedium
document.getElementById("setStepSmall").onclick = stepSizeSmall
document.getElementById("buttonGoTo").onclick = goTo
document.getElementById("buttonRun").onclick = run
document.getElementById("buttonUpdateGraph").onclick = updateGraph
document.getElementById("toggleLock").onclick = toggleLock

getMachineStatus();