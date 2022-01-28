
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
const this_site_url = window.location.href;


function createNewComment(){
    var form = new FormData(document.getElementById('comment_form'));
    const request = new Request(
        this_site_url,
        {
            method: "POST",
            headers: 
            {'X-CSRFToken': csrftoken,
            "x-requested-with": "XMLHttpRequest",
            "if-value": "1"},
            body: form,
            mode: 'same-origin',
    
        }
    ); 
   

    fetch(request).then(function(response){

        return response.json();
        
    }).then(function(data){
        if(data){
            console.log(data)

            let table = document.getElementById("replaceable-comment-table");

            let new_table = document.createRange().createContextualFragment(data['comment_html_from_view']);

            table.textContent="";

            table.appendChild(new_table);
        }
        
    });
}

function createNewFile(){
    var form = new FormData(document.getElementById('file_form'));
    const request = new Request(
        this_site_url,
        {
            method: "POST",
            headers: 
            {'X-CSRFToken': csrftoken,
            "x-requested-with": "XMLHttpRequest",
            "if-value": "2"},
            body: form,
            mode: 'same-origin',
    
        }
    ); 
   

    fetch(request).then(function(response){

        return response.json();
        
    }).then(function(data){
        if(data){
            console.log(data)

            let table = document.getElementById("replaceable-file-table");

            let new_table = document.createRange().createContextualFragment(data['file_html_from_view']);

            table.textContent="";

            table.appendChild(new_table);
        }
        
    });
}
