let xhr = new XMLHttpRequest();
xhr.open("POST", "../api/is_login/");
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr.setRequestHeader("Authorization", "Token " + localStorage.getItem("token"));
xhr.send();
xhr.onload = function() {
    if (xhr.status !== 200){
        window.location.href = "/"
    }
};