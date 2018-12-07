function chamar_api() {
  var request = new XMLHttpRequest();
  request.onreadystatechange = function () {
    if (request.readyState == 4 && request.status == 200) {
      resposta = JSON.parse(request.responseText);
      preencher_lista(resposta);
    }
  }
  request.open("GET", "list?type=songs", true);
  request.send(null);
}

function preencher_lista(json_dados) {
  html = `<tr class="w3-dark-grey">
        <th class="w3-center">Músicas</th><th class="w3-center">Reprodução</th><th class="w3-center">Votos</th>
    </tr>`;
  for (var i = 0; i < json_dados.length; i++) {
    dados = json_dados[i];
    html = html + `<tr class="w3-center">
        <td class="w3-center">` + dados.name + `</td>
        <td class="w3-center"><audio controls>
          <source src="audio/samples/` + dados.name + `.wav" type="audio/wav">
          Your browser does not support the audio tag.
        </audio></td>
        <td class="w3-center">
          <button class="w3-button w3-blue-grey" id="up_` + dados.id + `" onclick="upvote('` + dados.id + `')"><i class="fa fa-arrow-up"></i></button>
          <a id="refresh_`+ dados.id + `">     ` + dados.votes + `</a>
          <button class="w3-button w3-blue-grey" id="down_` + dados.id + `" onclick="downvote('` + dados.id + `')"><i class="fa fa-arrow-down"> </i> </button> 
        </td>
      </tr>`;
  }
  document.getElementById("songsJS").innerHTML = html;
}


function upvote(id) {
  var request = new XMLHttpRequest();
  request.open("GET", "vote?id=" + id + "&points=1", true);
  request.onreadystatechange = function () { if (request.readyState == 4 && request.status == 200) refresh(); }
  request.send(null);
}

function downvote(id) {
  var request = new XMLHttpRequest();
  request.open("GET", "vote?id=" + id + "&points=-1", true);
  request.onreadystatechange = function () { if (request.readyState == 4 && request.status == 200) refresh(); }
  request.send(null);
}

function refresh(id) {
  var request = new XMLHttpRequest();
  request.onreadystatechange = function () {
    if (request.readyState == 4 && request.status == 200) {
      resposta = JSON.parse(request.responseText);
      for (i = 0; i < resposta.length; i++) {
        console.log("refresh_" + resposta[i].id);
        document.getElementById("refresh_" + resposta[i].id).innerHTML = resposta[i].votes;
      }
    }
  }
  request.open("GET", "list?type=songs", true);
  request.send(null);
}

chamar_api();