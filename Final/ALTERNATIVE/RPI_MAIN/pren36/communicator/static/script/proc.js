var started = false;
var locationInterval = 0;
var reqAnimationInterval = 0;
var timerInterval = 0;
var canvas = null;
var ctx = null;
var cvWidth = null;
var cvHeight = null;
var realCubeX = null;
var realCubeZ = null;
var cubeX = null;
var cubeZ = null;
var startTime = null;
var stopped = false;

$(document).ready(function () {
    $('#btnStart').click(function () {
       start();
    });
    $('#btnStop').click(function () {
       stop();
    });
    initializeCanvas();
});

function start() {
    if(!started) {
        $('#btnStart').addClass("btnStartActive");
        $('#btnStop').removeClass("btnStopActive");
        startProcess();
    }
}

function stop() {
    if(started) {
        $('#btnStop').addClass("btnStopActive");
        $('#btnStart').removeClass("btnStartActive");
        stopProcess();
    }
}

function startProcess() {
    stopped = false;
    sendAjaxRequest("start", startCallback);
    started = true;
}

function stopProcess() {
    stopped = true;
    sendAjaxRequest("stop", stopCallback);
    started = false;
}

function updateCoordinates() {
    locationInterval = window.setInterval("sendAjaxRequest(\"location\", locationCallback)", 80);
    reqAnimationInterval = window.requestAnimationFrame(animateCube);
}

function sendAjaxRequest(action, callback) {
    $.ajax({
        url: "http://192.168.2.1:8080/" + action,
        type: "GET",
        success: callback
    });
}

function startCallback(response) {
    $('#state').text(response);
    started = true;
    showState();
    startTimer();
    updateCoordinates();
}

function stopCallback(response) {
    $('#state').text(response);
    stopTimer();
    window.clearInterval(locationInterval);
    window.cancelAnimationFrame(reqAnimationInterval);
    started = false;
}

function locationCallback(response) {
    if(!started) {
        return;
    }
    var coordinates = response.split(";");
    var x = parseFloat((coordinates[0] / 10).toString()).toFixed(2);
    var z = parseFloat((coordinates[1] / 10).toString()).toFixed(2);
    if(coordinates.length === 3) {
        var state = coordinates[2].toString();
        $('#state').text(state);
        if(!stopped) {
            if(state === "RESPONSE_PROCESS STOPPED") {
                stopped = true;
                $('#btnStop').addClass("btnStopActive");
                $('#btnStart').removeClass("btnStartActive");
                stopCallback("RESPONSE_PROCESS STOPPED")
            }
        }
    }
    if(x !== "None" && z !== "None") {
        $('#posX').text(x);
        $('#posZ').text(z);
        realCubeX = x;
        realCubeZ = z;
    }
}

function showState() {
    $('#stateContainer').show();
}

function startTimer() {
    startTime = Date.now();
    timerInterval = setInterval(function() {
        var elapsedTime = Date.now() - startTime;
        document.getElementById("timer").innerHTML = (elapsedTime / 1000).toFixed(3);
    }, 100);
    $('#seconds').text('s');
    $('#timerContainer').show()
}

function stopTimer() {
    window.clearInterval(timerInterval)
}

function initializeCanvas() {
    canvas = document.getElementById("cvsPos");
    ctx = canvas.getContext("2d");
    cvWidth = canvas.width;
    cvHeight = canvas.height;

    ctx.fillStyle = "rgba(0, 0, 0, 0.1)";
    ctx.fillRect(0, cvHeight - 50, cvWidth, 50);

    ctx.fillStyle = "rgba(233, 210, 171, 1.0)";
    ctx.fillRect(10, cvHeight - 170, 20, 120);

    ctx.fillStyle = "rgba(233, 210, 171, 1.0)";
    ctx.fillRect(710, cvHeight - 270, 20, 220);

    ctx.beginPath();
    ctx.fillStyle = "rgba(0, 0, 0, 1.0)";
    ctx.arc(10, cvHeight - 172, 2, 0, Math.PI * 2, true);
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();
    ctx.fillStyle = "rgba(0, 0, 0, 1.0)";
    ctx.moveTo(0, cvHeight - 150);
    ctx.lineTo(8, cvHeight - 171);
    ctx.moveTo(10, cvHeight - 174);
    ctx.lineTo(710, cvHeight - 270);
    ctx.moveTo(710, cvHeight - 270);
    ctx.lineTo(720, cvHeight - 270);
    ctx.stroke();
    ctx.closePath();

    window.requestAnimationFrame = window.requestAnimationFrame
                                        || window.webkitRequestAnimationFrame
                                        || window.msRequestAnimationFrame
                                        || window.mozRequestAnimationFrame;
}

function clearCube() {
    if(cubeX != null && cubeZ != null) {
        ctx.clearRect(cubeX - 1, cubeZ - 1, 32, 32);
    }
}

function clearArea() {
    ctx.clearRect(31, cvHeight - 169, 647, 118);
    ctx.clearRect((cvWidth / 2) + 50, cvHeight - 220, 270, 170)
}

function drawCube(x, z) {
    cubeX = transformX(x);
    cubeZ = transformZ(z);
    ctx.fillStyle = "rgba(255, 0, 0, 1.0)";
    ctx.fillRect(cubeX, cubeZ, 30, 30);
}

function animateCube() {
    if(realCubeX != null && realCubeZ != null) {
        clearArea();
        drawCube(realCubeX, realCubeZ);
    }
    window.requestAnimationFrame(animateCube);
}

function transformX(x) {
    return (x * 2) + 30;
}

function transformZ(z) {
    return (cvHeight - 80) - (z * 2);
}