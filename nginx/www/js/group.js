let xhr_group_getGroup = new XMLHttpRequest();
xhr_group_getGroup.open("POST", "../api/getGroup/");
xhr_group_getGroup.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr_group_getGroup.setRequestHeader("Authorization", "Token " + localStorage.getItem("token"));
xhr_group_getGroup.send();
xhr_group_getGroup.onload = function() {
    let data = JSON.parse(xhr_group_getGroup.response)
    document.getElementById('group-name').innerHTML = data.name;
    document.getElementById('university').innerHTML = data.university;
    document.getElementById('faculty').innerHTML = data.faculty;
    document.getElementById('monday_first_week').value = data.monday_first_week;
    document.getElementById('start_semester').value = data.start_semester;
    document.getElementById('end_semester').value = data.end_semester;
    document.getElementById('students_count_number').innerHTML = data.users_count;
    let students = document.getElementById('students');
    for (student of data.users){
        let group_student = document.createElement('div');
        group_student.className = "group-student";
        let group_avatar = document.createElement('div');
        group_avatar.className = "group-avatar";
        let background_avatar = document.createElement('img');
        background_avatar.className = "group-avatar-img"
        background_avatar.src = "/static/img/background_avatar.svg";
        group_avatar.append(background_avatar);
        let default_avatar = document.createElement('img');
        default_avatar.className = "group-avatar-img"
        default_avatar.src = "/static/img/default_avatar.svg";
        group_avatar.append(default_avatar);
        let border_avatar = document.createElement('img');
        border_avatar.className = "group-avatar-img"
        border_avatar.src = "/static/img/border_avatar.svg";
        group_avatar.append(border_avatar);
        group_student.append(group_avatar);
        let student_name = document.createElement('p');
        student_name.className = "group-student-name";
        student_name.innerHTML = student.name;
        group_student.append(student_name);
        let delete_link = document.createElement('a');
        let delete_svg = document.createElement('img');
        delete_svg.src = "/static/img/delete.svg";
        delete_link.append(delete_svg);
        group_student.append(delete_link);
        students.append(group_student);
    }
};