let btn = document.getElementById("button");
let email_inp = document.getElementById("email");
let pass_inp = document.getElementById("password");

btn.addEventListener("click", function () {
    send("login", false, {
        "email": email_inp.value,
        "password": pass_inp.value
    }, function(data, status){
        if (status === 200){
            localStorage.setItem("token", data.token);
            window.location.href = "../schedule/";
        }
    })
});