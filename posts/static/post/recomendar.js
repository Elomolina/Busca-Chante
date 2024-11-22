let hacerOferta = document.getElementById("hacerOferta")
let checkboxOfertas = document.querySelectorAll(".checkboxOfertas")
let equis = document.querySelectorAll(".equis")
let editarBoton = document.getElementById("editarBoton")
let borrarBoton = document.getElementById("borrarBoton")
let buscarInfo = document.querySelectorAll(".buscarInfo")
let buscarChanteButton = document.getElementById("buscarChanteButton")
let contador = 0;
let minmax_range = document.getElementById("minmax-range")
minmax_range.addEventListener("input", (e) => {
    let rangoh4 = document.getElementById("rangoh4")
    let rango = parseInt(e.target.value)
    rangoh4.innerHTML = `C$0 - C$ ${e.target.value}`;
})




buscarChanteButton.addEventListener("click", actualizarDatos)

editarBoton.addEventListener("click", () => {
  desbloquearBoton()
})

buscarInfo.forEach((buscar) => {
  buscar.addEventListener("input", desbloquearBoton)
})

function desbloquearBoton()
{
    let contador = 0;
    buscarInfo.forEach((renta) => {
        if(renta.value.length > 0)
        {
            contador++;
        }
    })
    if(contador == buscarInfo.length && minmax_range.value > 0)
    {
      buscarChanteButton.disabled = false
    }
    else 
    {
      buscarChanteButton.disabled = true
    }
}
borrarBoton.addEventListener("click", () => {
  let buscarID = document.getElementById("buscarID").value 
  Swal.fire({
    title: "¿Estás seguro que deseas borrar la búsqueda?",
    text: "",
    icon: "question",
    confirmButtonText: "Borrar búsqueda"
})
.then((result) => {
    if(result.isConfirmed)
    {
        fetch(`/borrarBusqueda/`, {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(buscarID)
        })
        .then(data => data.json())
        .then((resultados) => {
            window.location.href = "/buscarEspacio/"
        })
    }
})
})

equis.forEach((equi) => {
  equi.addEventListener("click", borrarOferta)
})
checkboxOfertas.forEach((oferta) => 
  {
    oferta.addEventListener("change", enableButton)
  })


hacerOferta.addEventListener("click", () => {
  ofertas()  
})

function ofertas()
{
  ofers = []
  checkboxOfertas.forEach((oferta) => 
  {
    if(oferta.checked)
    {
      postId = oferta.previousElementSibling.value;
      ofers.push(postId)
      
    } 
  })
  fetch("", {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(ofers)
  })
  .then(data => data.json())
  .then(resultados => {
    Swal.fire({
      title: `${resultados['success']}`,
      text: "",
      icon: "success",
      confirmButtonText: "Continuar"
    })
    .then((result) => {
      if(result.isConfirmed)
      {
          window.location.href = ""
          
      }
    })
  })
  
}

function camposRellenados(boton, info) {
  let contador = 0;
  info.forEach((r) => {

      if (r.value.length > 0) {
          contador++;

      }
  })
  if (info == buscarInfo) {
      if (contador == info.length) {
          boton.disabled = false;
          return

      }
      else {
          boton.disabled = true;
          return
      }
  }
  else {
      //todos los campos fueron rellenados
      if (contador == info.length) {
          boton.disabled = false;
          return
      }
      else {
          boton.disabled = true;
          return
      }
  }
}

function enableButton()
{
  console.log("cambio");
  
  contador = 0;
  checkboxOfertas.forEach((oferta) => {
    if(oferta.checked)
    {
      contador++;
    }
  })
  //ninguna oferta checked
  if(contador == 0)
    {
    hacerOferta.disabled = true;

  }
  else 
  {
    hacerOferta.disabled = false;
  }
}
function borrarOferta(e)
{
  let ofertaPost = e.target.previousElementSibling.value
  Swal.fire({
    title: `Eliminar oferta`,
    text: "Si la oferta no cumple con lo que buscas puedes eliminarla",
    icon: "question",
    confirmButtonText: "Borrar Oferta"
  })
  .then((result) => {
    if(result.isConfirmed)
    {
        //borrar post
        fetch('/borrarOferta/', {
          method: 'POST', 
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(ofertaPost)
        })
        .then(data => data.json())
        .then(resultados => {
          window.location.href = ""
        })
    }
  })
  
  
}

function actualizarDatos()
{
  informacion = {
    'buscarID': document.getElementById('buscarID').value,
    'tipoCasa': document.getElementById('opciones').value, 
    'precio': document.getElementById('minmax-range').value,
    'ubicacion': document.getElementById('ubicacion').value,
    'descripcion': document.getElementById('descripcion').value
  }
  Swal.fire({
    title: `Actualizar búsqueda`,
    text: "Actualiza los datos de tu búsqueda",
    icon: "success",
    confirmButtonText: "Actualizar búsqueda"
  })
  .then((resultados) => {
    if(resultados.isConfirmed)
    {
      fetch('/actualizarBusqueda/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(informacion)
      })
      .then(data => data.json())
      .then((results) => {
        if('success' in results)
        {
          window.location.href = ""
        }
      })
    }

  })
  
}