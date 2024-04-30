let backdrop = document.createElement("div");
backdrop.className = "backdrop";
document.body.prepend(backdrop);

var menu_int = document.getElementById('menu_interact');
var background_top = document.getElementById('background-top');
var background_bottom = document.getElementById('background-bottom');
let username_html = document.getElementById('user-text');

menu_int.addEventListener('mouseenter', function(){
    menu_int.style.width = '300px';
    background_top.style.width = '300px';
    background_bottom.style.width = '300px';
    var backdrop = document.querySelector('.backdrop');
    backdrop.style.display = 'block';
    var lessons = document.querySelectorAll('.lessons');
    lessons.forEach(function(lesson) {
        lesson.style.filter = 'blur(4px)';
    });
    var but = document.querySelectorAll('.menu-button')
    but.forEach(function(btn){
        btn.style.width = '300px'
    });
    var text = document.querySelectorAll(".menu-text")
    text.forEach(function(txt){
        txt.style.transition = 'opacity 0.5s'
        txt.style.opacity = 1;
    });
});

menu_int.addEventListener("mouseleave", function(){
    var backdrop = document.querySelector('.backdrop');
    menu_int.style.width = '60px';
    background_top.style.width = '60px';
    background_bottom.style.width = '60px';
    backdrop.style.display = 'none';
    var lessons = document.querySelectorAll('.lessons');
    lessons.forEach(function(lesson) {
    lesson.style.filter = 'none';
    });
    var but = document.querySelectorAll('.menu-button')
    but.forEach(function(btn){
        btn.style.width = '60px';
    });
    var text = document.querySelectorAll(".menu-text")
    text.forEach(function(txt){
        txt.style.transition = 'none';
        txt.style.opacity = 0;
    });
});

function logout(){
    let xhr_logout = new XMLHttpRequest();
    xhr_logout.open("POST", "../api/logout/");
    xhr_logout.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr_logout.setRequestHeader("Authorization", "Token " + localStorage.getItem("token"));
    xhr_logout.send();
    xhr_logout.onload = function() {
        window.location.href = "/"
    };
}

let xhr_getMe = new XMLHttpRequest();
xhr_getMe.open("POST", "../api/getMe/");
xhr_getMe.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr_getMe.setRequestHeader("Authorization", "Token " + localStorage.getItem("token"));
xhr_getMe.send();
xhr_getMe.onload = function() {
    username_html.innerHTML = JSON.parse(xhr_getMe.response).name;
};