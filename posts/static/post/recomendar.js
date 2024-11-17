let hacerOferta = document.getElementById("hacerOferta")

hacerOferta.addEventListener("click", () => {
    Swal.fire({
        title: "clickeao",
        text: "",
        icon: "success",
        confirmButtonText: "Continuar"
      })
      .then((result) => {
        if(result.isConfirmed)
        {
            alert("si")
        }
      })
})