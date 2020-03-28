
var selected_card = null

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
        var xT = cell_elem.offsetLeft;
        var yT = cell_elem.offsetTop;
        var xE = card_elem.offsetLeft;
        var yE = card_elem.offsetTop;
        // set elements position to their position for smooth animation
        card_elem.style.left = xE + 'px';
        card_elem.style.top = yE + 'px';
        // set their position to the target position
        // the animation is a simple css transition
        card_elem.style.left = xT + 'px';
        card_elem.style.top = yT + 'px';
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
            JSON.parse(XHR.response).forEach(e => {
                console.log(e.cell_id)
                elem = document.getElementById('cell_'+ e.cell_id)
                if (elem != null) {
                    elem.style.top = e.top + 'px';
                    elem.style.left = e.left + 'px';
                }
            });
          var xT = cell_elem.offsetLeft;
          var yT = cell_elem.offsetTop;
          var xE = card_elem.offsetLeft;
          var yE = card_elem.offsetTop;
          // set elements position to their position for smooth animation
          card_elem.style.left = xE + 'px';
          card_elem.style.top = yE + 'px';
          // set their position to the target position
          // the animation is a simple css transition
          card_elem.style.left = xT + 'px';
          card_elem.style.top = yT + 'px';

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

