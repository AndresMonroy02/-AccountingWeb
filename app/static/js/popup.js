
// document.getElementById("open").addEventListener("click", function () {
//     document.getElementById(".popup").style.display = "flex";
// });  
// document.querySelector(".close").addEventListener("click", function () {
//     document.querySelector(".popup").style.display = "none";
// });

const openModal = document.getElementById("open");
const modal = document.getElementById("modal-input");
const closeModal = document.getElementById("close");

openModal.addEventListener("click", (e)=> {
    e.preventDefault
    modal.classList.add("modal--show");
});

closeModal.addEventListener("click", (e)=> {
    e.preventDefault
    modal.classList.remove("modal--show");
});
