let save = document.querySelectorAll(".save")

save.forEach((guardado) => {
    guardado.addEventListener('click', (e) => {
        let post = ''
        if(guardado.src.includes('not_save.png'))
        {
            guardado.src = '/static/post/save.png'
            post = true
            
        }
        else 
        {
            guardado.src = '/static/post/not_save.png'
            post = false
        }
        guardarPost(e, post, window.location.pathname)
        
    })
}) 


function guardarPost(e, guardado, path)
{
    let postID = e.target.previousElementSibling.value;
    informacion = {
        'saved': guardado, 
        'post': postID,
        'path': path
    }
    fetch('/guardarPost/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(informacion)
    })
    .then(data => data.json())
    .then((resultados) => {
        if(resultados.recargar == 'True')
        {
            Swal.fire({
                title: `Quitar post de mis guardados`,
                text: "",
                icon: "success",
                confirmButtonText: "Quitar"
              })
              .then(resultados => {
                if(resultados.isConfirmed)
                {
                    window.location.href = ""
                }
              })
        }
        
    })
    
    
}