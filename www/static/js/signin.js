const btn = document.getElementById("button");
const email_inp = document.getElementById("email");
const pass_inp = document.getElementById("password");

btn.addEventListener("click", function () {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "../api/login/");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({"email": email_inp.value, "password": pass_inp.value}));
    xhr.onload = function() {
        if (xhr.status === 200){
            localStorage.setItem("token", JSON.parse(xhr.response).token);
            window.location.href = "../schedule/";
        }
    };
});