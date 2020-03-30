
var selected_card = null


function start_game(game_id){
    console.log('game with id ' + game_id + 'started')
    var XHR = new XMLHttpRequest();
    var FD  = new FormData();
    
    FD.append('game_id', game_id);
    // Définissez ce qui se passe si la soumission s'est opérée avec succès
    XHR.addEventListener('load', function(event) {
        console.log(XHR.response)
        if (XHR.status == 403) {
            alert('Request forbidden ! ')
        }
        else if (XHR.status == 200) {
            console.log('return 200 OK');
            update_cells(JSON.parse(XHR.response))
        }
    });
  
    // Definissez ce qui se passe en cas d'erreur
    XHR.addEventListener('error', function(event) {
      alert('Oups! Quelque chose s\'est mal passé.');
      console.log(XHR.getResponseHeader)
    });
  
    // Configurez la requête
    XHR.open('POST', '/castlemaze/start_game');
    var csrftoken = getCookie('csrftoken');
    XHR.setRequestHeader("X-CSRFToken", csrftoken);
  
    // Expédiez l'objet FormData ; les en-têtes HTTP sont automatiquement définies
    console.log(XHR.send(FD));
}

function update_cells(jsonlist){
    jsonlist.forEach(e => {
        console.log(e)

        if(e.action == 'delete') {
            elem = document.getElementById('tile_'+ e.card_id);
            elem.remove();
        }
        if(e.action == 'update') {
            elem = document.getElementById('tile_'+ e.card_id);
            cell = document.getElementById('cell_'+ e.cell_id);
           
            elem.style.left = cell.style.left
            elem.style.top = cell.style.top
            if(e.clickable == true) {
                cell.className = "castlemaze-cell clickable";
            } else {
                cell.className = "castlemaze-cell";
            }
        }
        if(e.action == 'create') {

            old_card = document.getElementById('card_'+ e.card_id);
            old_card.remove()
            
            cell = document.getElementById('cell_'+ e.cell_id);
            var div = document.createElement('div');
          
            div.className = 'castlemaze-tile';
            div.id = 'tile_'+ e.card_id;
            cell.parentNode.appendChild(div);
            div.style.top = cell.style.top;
            div.style.left = cell.style.left;

            var img = document.createElement('img');
            img.style.width = "70px";
            img.src = "/static/" + e.src;
            div.appendChild(img)
        }
    });

}
function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
  }

function select_card(id){
    console.log(id);
    if (document.getElementById(id).style.width == '200px'){
        document.getElementById(id).style.width= "100px";
        selected_card = null

    }
    else {
        document.getElementById(id).style.width= "200px";
        selected_card = id
    }
}


function action_request(cell_id){

    var card_elem = document.getElementById(selected_card)
    var cell_elem = document.getElementById(cell_id)

    if(selected_card == null) {
        console.log('No card selected')
        alert('No card selected')
        return
    }
    
    var XHR = new XMLHttpRequest();
    var FD  = new FormData();


    // Mettez les données dans l'objet FormData
    FD.append('cell_id', cell_elem.getAttribute('value'));
    FD.append('card_id', card_elem.getAttribute('value'));

  
    // Définissez ce qui se passe si la soumission s'est opérée avec succès
    XHR.addEventListener('load', function(event) {
        console.log(XHR.response)
        console.log(typeof(JSON.parse(XHR.response)))
        if (XHR.status == 403) {
            alert('Move forbidden ! ')
        }
        else if (XHR.status == 200) {
            console.log('return 200 OK');
            update_cells(JSON.parse(XHR.response))
        }
    });
  
    // Definissez ce qui se passe en cas d'erreur
    XHR.addEventListener('error', function(event) {
      alert('Oups! Quelque chose s\'est mal passé.');
      console.log(XHR.getResponseHeader)
    });
  
    // Configurez la requête
    XHR.open('POST', '/castlemaze/action_request/');
    var csrftoken = getCookie('csrftoken');
    XHR.setRequestHeader("X-CSRFToken", csrftoken);
  
    // Expédiez l'objet FormData ; les en-têtes HTTP sont automatiquement définies
    console.log(XHR.send(FD));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

