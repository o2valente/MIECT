
function chamar_api() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (request.readyState == 4 && request.status == 200) {
            resposta = JSON.parse(request.responseText);
            preencher_lista(resposta);
        }
    }
    request.open("GET", "list?type=samples", true);
    request.send(null);
}

function preencher_lista(json_dados) {
    html = `<option value="" disabled selected>Escolhe o teu Som</option>`;
    for (var i = 0; i < json_dados.length; i++) {
        dados = json_dados[i];
        html = html + `<option value="`+dados.name+`">`+dados.name+`</option>`;
    }

    var arr = document.getElementsByClassName("mixJS");
    for (var i = 0; i < arr.length; i++) {
        arr[i].innerHTML = html;
    }
}


chamar_api();