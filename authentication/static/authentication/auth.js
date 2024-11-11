let nav_div = document.querySelector(".nav-div");
let pop_up = document.querySelector(".popUp")
nav_div.addEventListener("click", () => {
    openPopUp()
})

function openPopUp()
{
    pop_up.classList.toggle("show");
}

//close popup on clicking outside of it
document.addEventListener("click", (e) => {
    if(!nav_div.contains(e.target) && !pop_up.contains(e.target))
    {
        pop_up.classList.remove("show");   
    }
    
})