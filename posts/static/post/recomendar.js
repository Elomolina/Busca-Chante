let hacerOferta = document.getElementById("hacerOferta")
let checkboxOfertas = document.querySelectorAll(".checkboxOfertas")
let equis = document.querySelectorAll(".equis")
let borrarBoton = document.getElementById("borrarBoton")
let contador = 0;
let minmax_range = document.getElementById("minmax-range")
minmax_range.addEventListener("input", (e) => {
    let rangoh4 = document.getElementById("rangoh4")
    let rango = parseInt(e.target.value)
    rangoh4.innerHTML = `C$0 - C$ ${e.target.value}`;
})

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