let commentForm = document.getElementById("commentForm")
let message = document.getElementById("message")
let botonComentario = document.getElementById("botonComentario")
let userID = document.getElementById("userID")
let postID = document.getElementById("postID")
let borrarBoton = document.getElementById("borrarBoton")
let editarBoton = document.getElementById("editarBoton")

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

borrarBoton.addEventListener("click", () => 
{
    let postID_value = postID.value;
    Swal.fire({
        title: "¿Estás seguro que deseas borrar el espacio?",
        text: "",
        icon: "question",
        confirmButtonText: "Borrar Post"
    })
    .then((result) => {
        if(result.isConfirmed)
        {
            fetch(`/borrarEspacio/`, {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(postID_value)
            })
            .then(data => data.json())
            .then((resultados) => {
                window.location.href = "/"
            })
        }
    })
})