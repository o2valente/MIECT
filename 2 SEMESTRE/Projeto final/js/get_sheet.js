function get_array(){
    var arr = [];
    for(var i = 0; i < 10; i++){
        arr[i] = [];
    }
    var temp = [];
    for(var i = 1; i <= 10; i++){
        for(var j = 1; j <= 10; j++){
            arr[i-1][j-1] = document.getElementById("check_" + i.toString() + "_" + j.toString()).checked;
        }
    }
    return arr;
}

function get_samples(){
    var arr = [];
    var selects = [];
    var values = [];
    selects = document.getElementsByClassName("mixJS");
    for(var i = 0; i < selects.length; i++){
        var elem = selects[i];
        values[i] = elem.options[elem.selectedIndex].value;
    }
    for(var i = 0; i < values.length; i++){    
        if(values[i].length != 0){
            arr.push(values[i]);
        }
    }
    return arr;
    
}

function get_effects(){
    var arr = [];
    var selects = [];
    var values = [];
    selects = document.getElementsByClassName("effectsJS");
    for(var i = 0; i < selects.length; i++){
        var elem = selects[i];
        values[i] = elem.options[elem.selectedIndex].value;
    }
    for(var i = 0; i < values.length; i++){    
        if(values[i].length != 0){
            arr.push(values[i]);
        }
    }
    return arr;
    
}

function get_vol(){
    var arr = [];
    var selects = [];
    var values = [];
    selects = document.getElementsByClassName("volJS");
    for(var i = 0; i < selects.length; i++){
        var elem = selects[i];
        values[i] = elem.value;
    }
    for(var i = 0; i < values.length; i++){    
        if(values[i].length != 0){
            arr.push(values[i]);
        }
    }
    return arr;
    
}


function get_BPM() {
    var select = document.getElementsByClassName("bpmJS")
    var elem = select.value;
    return select;
}


function generate_json(){
    var json = {
        "bpm": 0,
        "samples": [],
        "effects": [],
        "vol" : [],
        "music" : []
    };

    json.bpm = get_BPM();
    json.samples = get_samples();
    json.effects = get_effects().slice(0,json.samples.length);
    json.vol = get_vol().slice(0,json.samples.length);
    var arr = get_array();
    for(var i = 0; i < 10; i++){
        json.music[i] = [];
    }
    for(var i = 0; i < arr[0].length; i++){
        for(var j = 0; j < arr.length; j++){
             if(arr[j][i] && j<json.samples.length){
               
                json.music[i].push(j);
            }
        }
    }
    return json;
}

function test(){
    var json = generate_json();
    var request = new XMLHttpRequest();

    request.open("POST", "sheet?sheet=" + JSON.stringify(json), true);
    request.send(null);
      
}
