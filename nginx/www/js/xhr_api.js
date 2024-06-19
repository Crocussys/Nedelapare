function send(method, is_authorization = false, data, callback = function(){}){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/" + method + "/");
    xhr.setRequestHeader("Content-Type", "application/json");
    if (is_authorization){
        xhr.setRequestHeader("Authorization", "Token " + localStorage.getItem("token"));
    }
    xhr.send(JSON.stringify(data));
    xhr.onload = function(){
        let response = xhr.response;
        let status = xhr.status;
        if (status < 500 && response !== ""){
            response = JSON.parse(xhr.response)
        }
        callback(response, status);
    };
}