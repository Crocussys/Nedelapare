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
        let email = document.getElementById('email').value;
        send("reg", false, {
            "email": email,
            "name": document.getElementById('name').value,
            "password": password.value,
            "position": position
        }, function(data, status){
            if (status === 200){
                location.href = '../wait?msg=0&email=' + email;
            }else{
                console.log(data);
            }
        })
    }else{
        console.log("Пароли не совпадают");
    }
}