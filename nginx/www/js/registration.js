var password = document.getElementById('password');
var password2 = document.getElementById('password2');

function load(){
    let position = 0;
    if (document.getElementById('student').checked === true){
        position = 0;
    }else if (document.getElementById('teacher').checked === true){
        position = 1;
    }
    if (password.value === password2.value){
        let xhr = new XMLHttpRequest();
        let email = document.getElementById('email').value;
        xhr.open("POST", "../api/reg/");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify({
            "email": email,
            "name": document.getElementById('name').value,
            "password": password.value,
            "position": position
        }));
        xhr.onload = function() {
            if (xhr.status === 200){
                location.href = '../wait?email=' + email;
            }else{
                console.log(JSON.parse(xhr.response));
            }
        }
    }else{
        console.log("Пароли не совпадают");
    }
}