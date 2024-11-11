let form = document.querySelector("form");
let logIn = document.querySelector("#logIn");

form.addEventListener("submit", (e) => {
    e.preventDefault()
})

logIn.addEventListener("click", () => {
    let user = document.querySelector("#user_mail").value;
    let pass = document.querySelector("#pass").value;
    if(user.length == 0 || pass.length == 0)
    {
        Swal.fire({
            title: "Rellena todos los campos para iniciar sesión",
            text: "",
            icon: "error"
          })
          return;
    }
    let information = {
        user_mail:user,
        password:pass
    }
    sentData(information)
})

function sentData(information)
{
    fetch("",{ 
        method: 'POST',
        headers: {
            'Content-Type': "application/json"
        },
        body: JSON.stringify(information)
    })
    .then(response => response.json())
    .then((data) => {
        if('error' in data)
        {
            Swal.fire({
                title: `${data['error']}`,
                text: "",
                icon: "error"
              })
              return
        }
        Swal.fire({
            title: `${data['success']}`,
            text: "",
            icon: "success",
            confirmButtonText: "Continuar"
          })
          .then((result) => {
            if(result.isConfirmed)
            {
                window.location.href = "/"
            }
          })
    });
}
