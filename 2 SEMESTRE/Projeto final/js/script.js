function isChecked(id){
    return document.getElementById(id).checked;
}

for(i = 0; i < 100; i++){
    checked = isChecked("check_"+(i/10+1)+"_"+(i%10));

}
window.open("/list?type=samples", "self");
function getSamples(params) {
    
}

// função para os sliders do volume
var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    output.innerHTML = this.value;
}

// Used to toggle the menu on small screens when clicking on the menu button
function myFunction() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else { 
        x.className = x.className.replace(" w3-show", "");
    }
}