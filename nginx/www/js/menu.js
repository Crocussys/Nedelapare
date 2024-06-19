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
    send("logout", true, {}, function(){
        window.location.href = "/"
    })
}

send("getMe", true, {}, function(data, status){
    username_html.innerHTML = data.name;
})