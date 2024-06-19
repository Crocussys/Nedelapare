send("is_login", true, {}, function(data, status){
    if (status === 423){
         window.location.href = "/wait?msg=1"
    }else if (status !== 200){
        window.location.href = "/"
    }
});