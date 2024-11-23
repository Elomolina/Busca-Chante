let formPost = document.getElementById("formPost")
let numero_telefono = document.getElementById("numero_telefono")
let updateInfo = document.querySelectorAll(".updateInfo")
let updateButton = document.getElementById("update")
let profilePic = document.getElementById("dropzone-file")
let imagen = document.getElementById("imagen")
let updatePic = document.getElementById("updatePic")
let pic = document.getElementById("pic")

updateInfo.forEach((input) => {
    input.addEventListener("input", enableButton)
})
updateButton.addEventListener("click", () => {
    actualizarDatos()
}) 

formPost.addEventListener("submit", (e) => {
    e.preventDefault()
    validacion()
})

updatePic.addEventListener("click", () => {
    const formData2 = new FormData()
    const file = profilePic.files[0]
    formData2.append("file", file)
    fetch("/actualizarProfilePic/", {
        method: 'POST',
        body: formData2
    })
    .then(() => {
        window.location.href = ""
    })
})
profilePic.addEventListener("change", () => {
    const file = profilePic.files[0];
    const reader = new FileReader();
    reader.onload = function(e)
    {
        const imageDataUrl = e.target.result;
        imagen.src = imageDataUrl;
        imagen.style.display = 'block';
    };
    reader.readAsDataURL(file);
    if(file)
    {
        updatePic.disabled = false;
    }
    else 
    {
        updatePic.disabled = true;
    }
})

numero_telefono.addEventListener("input", validacion)

function actualizarDatos()
{
    const formData = new FormData()
    let informacion = {
        'username': document.getElementById('username').value,
        'nombre': document.getElementById('nombre').value, 
        'apellido': document.getElementById('apellido').value,
        'telefono': document.getElementById('numero_telefono').value
    }
    formData.append('informacion', JSON.stringify(informacion))
    fetch("", {
        method: 'POST', 
        body: formData
    })
    .then(data => data.json())
    .then((resultados) => {
        if('success' in resultados)
        {
            Swal.fire({
                title: "Tus datos han sido actualizados exitosamente",
                text: "",
                icon: "success",
                confirmButtonText: "Continuar"
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
function enableButton()
{
    let contador = 0;
    for(let i = 0; i < updateInfo.length; i++)
    {
        
        if(updateInfo[i].value.length > 0)
        {
            contador++;
        }
    }
    
    if(contador == updateInfo.length && validacion())
    {
        updateButton.disabled = false
    }
    else 
    {
        updateButton.disabled = true
    }
}

function validacion()
{
    const telefono_regex = /^.{8}$/;
    let telefono = document.querySelector(".telefono")
    telefono.innerHTML = ""
    if (!telefono_regex.test(numero_telefono.value))
    {
        let h3 = document.createElement("h3")
        h3.innerHTML = "El número de teléfono no es válido."
        telefono.appendChild(h3);
        updateButton.disabled = true
        return false
        
    }
    else 
    {
        telefono.innerHTML = ""
        updateButton.disabled = false
        return true
    }
}
