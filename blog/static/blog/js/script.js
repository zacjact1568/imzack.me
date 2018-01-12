var count = 10;
function redirect(){
    count--;
    document.getElementById("count").innerHTML = count.toString();
    if (count < 0) {
        document.getElementById("count").innerHTML = "0";
        location.href = document.getElementById("home").href;
    }
}
setInterval("redirect()", 1000);