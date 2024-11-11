let inputs_div = document.querySelectorAll(".inputs-div");
let next = document.querySelector("#next");
let back = document.querySelector("#back");
let form = document.querySelector("form");
let register_button = document.querySelector("#register-button");

console.log(inputs_div);

form.addEventListener("submit", (e) => {
    e.preventDefault();
})

next.addEventListener("click", (e) => {
    let div = '';
    for (let i = 0; i < inputs_div.length; i++) {
        div = inputs_div[i];
        if (div.classList.contains('open')) {
            if (div.classList.contains('send')) {
                //next es el primero
                div = inputs_div[0];
            }
            else {
                //div es el siguiente
                div = inputs_div[i].nextElementSibling;
            }
            inputs_div[i].classList.add("close");
            inputs_div[i].classList.remove("open");
            div.classList.add("open");
            div.classList.remove("close");
            break;
        }
    }


})

back.addEventListener("click", (e) => {
    let div = '';
    for (let i = 0; i < inputs_div.length; i++) {
        div = inputs_div[i];
        if (div.classList.contains('open')) {
            if (div.classList.contains('correo')) {
                //next es el primero
                div = inputs_div[inputs_div.length - 1];
            }
            else {
                //div es el siguiente
                div = inputs_div[i].previousElementSibling;
            }
            inputs_div[i].classList.add("close");
            inputs_div[i].classList.remove("open");
            div.classList.add("open");
            div.classList.remove("close");
            break;
        }
    }

})

register_button.addEventListener("click", () => {
    let information = {
        correo: document.getElementById("correo").value,
        telefono: document.getElementById("telefono").value,
        nombre: document.getElementById("nombre").value,
        apellido: document.getElementById("apellido").value,
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
        confirmation: document.getElementById("confirmation").value,
    }
    for (let clave in information) {
        //asegurarnos que todos los campos fueron rellenados
        if (information[clave] == '') {
            Swal.fire({
                title: "Parece que no has rellenado todos los campos",
                text: "Asegurate de rellenar todos los campos para continuar 🤠",
                icon: "error"
            });
            return;

        }

    }
    //regex confirmando longitud pass
    const regex = /^(?=.*[!@#$%^&*()_\-+={}[\]:;"'<>,.?/~`|\\]).{8,}$/;
    if (!regex.test(information["password"])) {
        Swal.fire({
            title: "La contraseña debe tener mas de 8 caracteres y por lo menos un simbolo ☹️",
            text: "Verifica que la contraseña cumpla los requisitos",
            icon: "error"
        });
        return;
    }
    //regex confirmando correo
    const correo_regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!correo_regex.test(information["correo"])) {
        Swal.fire({
            title: "La dirección de correo no es una dirección válida ☹️",
            text: "Verifica el correo",
            icon: "error"
        });
        return;
    }
    const telefono_regex = /^.{8}$/;
    if (!telefono_regex.test(information["telefono"])) {
        Swal.fire({
            title: "Ingresa un número telefónico válido 📱",
            text: "Verifica el teléfono",
            icon: "error"
        });
        return;
    }
    //asegurarnos que la confirmacion de pass es igual al pass
    if (information["password"] != information["confirmation"]) {
        Swal.fire({
            title: "Las contraseñas no coinciden ☹️",
            text: "",
            icon: "error"
        });
        return;
    }
    //despues de todas las verifaciones enviamos info a back
    //verificamos que el correo y user no esten en la bd.
    sentData(information)
})

function sentData(information) {
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(information)
    })
        .then(response => response.json())
        .then(data => {
            //verificar datos de usuario
            if ('error' in data) {
                Swal.fire({
                    title: `${data['error']}`,
                    text: "",
                    icon: "error"
                })
                return;

            }
            Swal.fire({
                title: `${data['success']}`,
                text: "",
                icon: "success",
                confirmButtonText: 'Continuar'
            }).then((result) => {
                if (result.isConfirmed) {
                    //funcion para limpiar inputs
                    window.location.href = data['path']
                }
            })
        })

}