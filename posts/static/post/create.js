let postForm = document.getElementById("postForm")
let minmax_range = document.getElementById("minmax-range")
let rentarChanteButton = document.getElementById("rentarChanteButton")
let buscarChanteButton = document.getElementById("buscarChanteButton")
let rentarInfo = document.querySelectorAll(".rentarInfo")
let buscarInfo = document.querySelectorAll(".buscarInfo")
let inputImage = document.getElementById("multiple_files")
let archivos = []

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
    if (valor == 'Busco rentar un espacio') {
        let buscar = document.getElementById("buscar")
        let ponerRenta = document.getElementById("ponerRenta")
        ponerRenta.style.display = 'none';
        buscar.style.display = 'block';
    }
    else if (valor == 'Quiero poner en renta un espacio') {
        let buscar = document.getElementById("buscar")
        let ponerRenta = document.getElementById("ponerRenta")
        ponerRenta.style.display = 'block';
        buscar.style.display = 'none';
    }
}
inputImage.addEventListener("change", () => {
    let archivos_div = document.querySelector(".archivos")
    archivos_div.innerHTML = "";
    for (let i = 0; i < inputImage.files.length; i++) {
        archivos.push(inputImage.files[i]);

    }
    for (let i = 0; i < archivos.length; i++) {
        //agregamos archivos
        let div = document.createElement("div")
        let h3 = document.createElement("h3")
        let button = document.createElement("button")
        h3.innerHTML = archivos[i].name
        button.innerHTML = "eliminar"
        button.classList.add("eliminarButton")
        div.appendChild(h3)
        div.appendChild(button)
        div.classList.add("divImagenes")
        archivos_div.appendChild(div)

    }
    let eliminarButton = document.querySelectorAll(".eliminarButton")

    eliminarButton.forEach((boton) => {
        boton.addEventListener("click", eliminarArchivo)
    })

})

rentarInfo.forEach((r) => {
    r.addEventListener("input", () => {
        camposRellenados(rentarChanteButton, rentarInfo)
    })

})

buscarInfo.forEach((r) => {
    r.addEventListener("input", () => {
        camposRellenados(buscarChanteButton, buscarInfo)
    })

})

function camposRellenados(boton, info) {
    let contador = 0;

    info.forEach((r) => {

        if (r.value.length > 0) {
            contador++;

        }
    })
    if (info == buscarInfo) {
        if (contador == info.length && minmax_range.value > 0) {
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

function eliminarArchivo(e) {


    let divImagenes = document.querySelectorAll(".divImagenes")
    let file_name = e.target.previousElementSibling;
    console.log(file_name);
    for (let i = 0; i < divImagenes.length; i++) {
        console.log(divImagenes[i].firstChild);

        if (divImagenes[i].firstChild == file_name) {
            for (let i = 0; i < archivos.length; i++) {
                if (archivos[i].name == file_name.innerHTML) {
                    //eliminamos archivo
                    archivos.splice(i, 1)

                }

            }

        }

    }
    e.target.parentNode.remove()
}