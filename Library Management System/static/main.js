
const open = document.getElementById('open');
const modal_container = document.getElementById('modal_container');
const close = document.getElementById('close');

open.addEventListener('click', () => {
    modal_container.classList.add('show');
});

close.addEventListener('click', () => {
    modal_container.classList.remove('show');
});


const open1 = document.getElementById('open1');
const modal_container1 = document.getElementById('modal_container1');
const close1 = document.getElementById('close1');

open1.addEventListener('click', () => {
    modal_container1.classList.add('show');
});

close.addEventListener('click', () => {
    modal_container1.classList.remove('show');
});

// test.addEventListener('click', () => {
//     test.classList.replace('apply', 'applied');
// });

// document.querySelector('#apply');
// document.querySelector('#apply')
//     .textContent = 'Applied!';




// function search_job() {
//     let input = document.getElementById('searchbar').value
//     input = input.toLowerCase();
//     let x = document.getElementsByClassName('job-list');
    
//     for (i=0; i<x.length;i++){
//         if (!x[i].innerHTML.toLowerCase().includes(input)){
//             x[i].style.display = "none";
//          }
//          else{
//             x[i].style.display="list-item";
//          }
//     }
// }


// $("a").click(function(){
//     $("a").css("background-color", "");
//     $(this).css("background", "yellow");
// });

// let listbtn = document.getElementsByClassName('link');
// let click = false;

// listbtn.addEventListener('click', () => {
//     if (click) {
//         // applyBtn.innerHTML = "Applied!"
//         listbtn.style = "background-color: #f1c657"
//         click = true
//     } else {
//         // applyBtn.innerHTML = "Apply"
//         listbtn.style = "background-color = #ffffff"
//         click = true
//     }
// });


// const button = document.getElementById('link');
// let btn = false;
// button.addEventListener('click', () => {
//     if (btn) {
//         button.style = "background-color: #ffffff"
//         // button.addEventListener('click', function onClick() {
//         //     button.style.backgroundColor ='#f1c657'
//         // });
//         btn = false
//     } else {
//         button.style = "background-color: #f1c657"
//         btn = true
//     }
// });




    

