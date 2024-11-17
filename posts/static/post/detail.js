let commentForm = document.getElementById("commentForm")
let message = document.getElementById("message")
let botonComentario = document.getElementById("botonComentario")
let userID = document.getElementById("userID")
let postID = document.getElementById("postID")

commentForm.addEventListener('submit', (e) => {
    e.preventDefault()
})
message.addEventListener("input", () => {
    if(message.value.length > 0)
    {
        botonComentario.disabled = false;
    }
    else 
    {
        botonComentario.disabled = true;
    }
    
})
botonComentario.addEventListener("click", () => {
    let informacion = {
        "postID": postID.value, 
        "userID": userID.value, 
        "message": message.value
    }
    fetch('', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(informacion)
    })
    .then(data => data.json())
    .then(results => {
        if('success in results')
        {
            window.location.href = ""
        }
        
    })
})