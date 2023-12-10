var menu_int = document.getElementById('menu_interact')

menu_int.addEventListener('mouseenter', function(){
    var menu = document.querySelector('.menu');
    menu.style.width = '300px';
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
    var menu = document.querySelector('.menu');
    var backdrop = document.querySelector('.backdrop');
    menu.style.width = '60px';
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

/*function openMenu(){
    var menu = document.querySelector('.menu');
    menu.style.width = '300px';
    var backdrop = document.querySelector('.backdrop');
    backdrop.style.display = 'block';
    var lessons = document.querySelectorAll('.lessons');
    lessons.forEach(function(lesson) {
    lesson.style.filter = 'blur(5px)';
    });
    var but = document.querySelector('.menu-button')
    but.style.width = '300px';
    }

    function closeMenu(){
    var menu = document.querySelector('.menu');
    var backdrop = document.querySelector('.backdrop');
    menu.style.width = '60px';
    backdrop.style.display = 'none';
    var lessons = document.querySelectorAll('.lessons');
    lessons.forEach(function(lesson) {
    lesson.style.filter = 'none';
    });
    var but = document.querySelector('.menu-button')
    but.style.width = '60px';
    };
    */