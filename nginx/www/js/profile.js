var roles = ['Студент', 'Преподаватель', 'Администратор']

send("getMe", true, {}, function(data, status){
    document.getElementById('username').value = data.name;
    document.getElementById('email').innerHTML = data.email;
    document.getElementById('type').innerHTML = roles[data.position]
})

send("getGroup", true, {}, function(data, status){
    document.getElementById('group-name').innerHTML = data.name;
})