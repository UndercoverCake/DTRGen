let form1 = document.querySelector('.form1');
let form2 = document.querySelector('.form2');
let click1 = document.querySelector('.click1');
let click2 = document.querySelector('.click2');

click1.addEventListener('click', (e) => {
    form2.classList.toggle("hidden");
    form1.classList.toggle("hidden");
    e.preventDefault();
})
click2.addEventListener('click', (e) => {
    form2.classList.toggle("hidden");
    form1.classList.toggle("hidden");
    e.preventDefault();
})