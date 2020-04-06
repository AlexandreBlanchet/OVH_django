const game_id = JSON.parse(document.getElementById('game_id').textContent);

const chatSocket = new WebSocket(
    'wss://'
    + window.location.host
    + '/ws/castlemaze/game/'
    + game_id
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(e.data)
    update_cells(data.message)
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
    chatSocket = new WebSocket(
        'wss://'
        + window.location.host
        + '/ws/castlemaze/game/'
        + game_id
        + '/'
    );
    console.log(e)
};

function update_cells(jsonlist){
    if(jsonlist.cards != null){
        jsonlist.cards.forEach(e => {
            card = document.getElementById('card_'+ e.card_id);
            img = document.getElementById('img_'+ e.card_id);
            if(card == null || img == null) {
                board = document.getElementById('board');
                card = document.createElement('div')
                card.setAttribute("id", 'card_' + e.card_id);
                board.appendChild(card)
                img = document.createElement('img')
                img.setAttribute('id', 'img_'+ e.card_id)
                card.appendChild(img)
            }
            card.style.left = e.left + 'px';
            card.style.top = e.top + 'px';
            card.className = e.class;
            img.src = '/static/'  + e.display
        });
    }
    if(jsonlist.pawns != null){
        jsonlist.pawns.forEach(e => {
            pawn = document.getElementById('pawn_'+ e.pawn_id);
            img = document.getElementById('pawn_img_'+ e.pawn_id);
            if(pawn == null || img == null) {
                board = document.getElementById('board');
                pawn = document.createElement('div')
                pawn.setAttribute("id", 'pawn_' + e.pawn_id);
                board.appendChild(pawn)
                img = document.createElement('img')
                img.setAttribute('id', 'pawn_img_'+ e.pawn_id)
                pawn.appendChild(img)
            }
            pawn.style.left = e.left + 'px'
            pawn.style.top = e.top + 'px'
            pawn.className = e.class;
            img.src = '/static/'  + e.display
        });
    }
    if(jsonlist.game_status != null){
        board = document.getElementById('board');
        jsonlist.game_status.forEach(e => {
            
            elem = document.getElementById('elem_'+ e.elem_id);
            img = document.getElementById('elem_img_'+ e.elem_id);
            text = document.getElementById('elem_text_'+ e.elem_id);
            if(elem == null) {
                elem = document.createElement('div')
                elem.setAttribute("id", 'elem_' + e.elem_id);
                board.appendChild(elem)
            }
            if(img == null) {
                img = document.createElement('img')
                img.setAttribute('id', 'elem_img_'+ e.elem_id)
                elem.appendChild(img)
            }
            if(text == null) {
                text = document.createElement('h4')
                text.setAttribute('id', 'elem_text_' + e.elem_id)
                elem.appendChild(text)
            }
                
            text.textContent = e.elem_text
            elem.className = e.class
            img.className = e.class
            elem.style.left = e.left + 'px'
            elem.style.top = e.top + 'px'
            if(typeof(e.display) != null && e.display != ''){
                img.src = '/static/'  + e.display;
            } 
            else {
                elem.removeChild(img);
            }
            if(e.elem_text == '') {
                board.removeChild(elem)
            }
        });
    }
    if(jsonlist.cells != null){
        jsonlist.cells.forEach(e => {
            cell = document.getElementById('cell_'+ e.cell_id);
            if(cell == null) {
                return;
            }
            cell.className = e.class
            if(e.clickable == true) {
                cell.dataset.clickable = 'True'
            } else {
                cell.dataset.clickable = 'False'
            }
        });
    }

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
            
            //update_cells(JSON.parse(XHR.response))
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

