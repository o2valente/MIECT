
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
  html = `<tr class="w3-dark-grey">
      <th class="w3-center">Som</th><th class="w3-center">Reprodução</th>
  </tr>`;
  for (var i = 0; i < json_dados.length; i++) {
    dados = json_dados[i];
    html = html + `<tr class="w3-center w3-hover-blue-gray">
      <td class="w3-center">` + dados.name + `</td>
      <td class="w3-center"><audio controls>
        <source src="audio/samples/` + dados.name + `.wav" type="audio/wav">
        Your browser does not support the audio tag.
      </audio></td>
    </tr>`;
  }
  document.getElementById("sampleJS").innerHTML = html;
}


chamar_api();