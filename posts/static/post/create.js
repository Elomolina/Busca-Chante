let postForm = document.getElementById("postForm")
let minmax_range = document.getElementById("minmax-range")
minmax_range.addEventListener("input", (e) => {
    let rangoh4 = document.getElementById("rangoh4")
    let rango = parseInt(e.target.value)
    rangoh4.innerHTML = `C$0 - C$ ${e.target.value}`;
})
postForm.addEventListener('submit', (e) => {
    e.preventDefault()
    tipoEspacio()
})

function tipoEspacio() {
    let opciones = document.getElementById("opciones");
    let valor = opciones.value;
    console.log(valor);
    
    if (valor == 'Busco rentar un espacio') {
        let buscar = document.getElementById("buscarBC")
        let ponerRenta = document.getElementById("ponerRenta")
        ponerRenta.style.display = 'none';
        buscar.style.display = 'block';
    }
    else if(valor == 'Quiero poner en renta un espacio')
    {
        let buscar = document.getElementById("buscarBC")
        let ponerRenta = document.getElementById("ponerRenta")
        ponerRenta.style.display = 'block';
        buscar.style.display = 'none';
    }
}
// function rentarOpciones() {

// }