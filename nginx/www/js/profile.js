var roles = ['Студент', 'Преподаватель', 'Администратор']

let xhr_profile_getMe = new XMLHttpRequest();
xhr_profile_getMe.open("POST", "../api/getMe/")
xhr_profile_getMe.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr_profile_getMe.setRequestHeader("Authorization", "Token " + localStorage.getItem("token"));
xhr_profile_getMe.send();
xhr_profile_getMe.onload = function() {
    let data = JSON.parse(xhr_profile_getMe.response)
    document.getElementById('username').value = data.name;
    document.getElementById('email').innerHTML = data.email;
    document.getElementById('type').innerHTML = roles[data.position]
}

let xhr_profile_getGroup = new XMLHttpRequest();
xhr_profile_getGroup.open("POST", "../api/getGroup/");
xhr_profile_getGroup.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr_profile_getGroup.setRequestHeader("Authorization", "Token " + localStorage.getItem("token"));
xhr_profile_getGroup.send();
xhr_profile_getGroup.onload = function() {
    document.getElementById('group-name').innerHTML = JSON.parse(xhr_profile_getGroup.response).name;
};