
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
    jsonlist.cards.forEach(e => {
        console.log(e)
        card = document.getElementById('tile_'+ e.card_id);
        card.style.left = e.left + 'px'
        card.style.top = e.top + 'px'
    });
    jsonlist.players.forEach(e => {
        console.log(e)
        card = document.getElementById('player_'+ e.player_id);
        card.style.left = e.left + 'px'
        card.style.top = e.top + 'px'
    });
    jsonlist.cells.forEach(e => {
        console.log(e)
        cell = document.getElementById('cell_'+ e.cell_id);
        cell.className = e.class
        if(e.clickable == true) {
            cell.dataset.clickable = 'True'
        } else {
            cell.dataset.clickable = 'False'
        }
    });

}


function action_request(cell_id){
    var cell_elem = document.getElementById(cell_id)
    if(cell_elem.dataset.clickable == 'False') {
        console.log('action not permitted')
        return
    }

    var XHR = new XMLHttpRequest();
    var FD  = new FormData();


    // Mettez les données dans l'objet FormData
    FD.append('cell_id', cell_elem.getAttribute('value'));

  
    // Définissez ce qui se passe si la soumission s'est opérée avec succès
    XHR.addEventListener('load', function(event) {
        console.log(XHR.response)
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

