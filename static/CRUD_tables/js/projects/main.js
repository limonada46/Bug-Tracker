
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

const search_input = document.getElementById("search_input");


function searchProject(){
    var form = new FormData(document.getElementById('projects-list-form'));
    const request = new Request(
        this_site_url,
        {
            method: "POST",
            headers: 
            {'X-CSRFToken': csrftoken,
            "x-requested-with": "XMLHttpRequest"},
            body: form,
            mode: 'same-origin',
    
        }
    ); 
   

    fetch(request).then(function(response){
        if (response.status != 200){
            let table = document.getElementById("replaceable-table");
            let error = document.createElement("p");
            error.textContent = "The project does not exist"
            error.className= "search-error";

            //remove all the child nodes from the old table
            table.textContent="";
            table.appendChild(error);
            
            console.clear(); // WEEK 4 
        }else{
            return response.json();
        }
        
    }).then(function(data){
        if(data){
            let table = document.getElementById("replaceable-table");
            //convert string into dom html nodes
            let new_table = document.createRange().createContextualFragment(data['html_from_view']);
            //remove all the child nodes from the old table
            table.textContent="";
            //append the new table
            table.appendChild(new_table);
        }
        
    });
}

    

