var university_select = document.getElementById('university-select');
var faculty_select = document.getElementById('faculty-select');
var group_select = document.getElementById('group-select');

function send_group(){
    if (group_select.value !== 0){
        send("setGroup", true, {
            "group_id": group_select.value
        }, function(respons, status){
            if (status === 200){
                location.href='../profile';
            }
        })
    }
}

send("getUniversities", true, {}, function(data){
    for (university of data.data){
        let option = document.createElement('option');
        option.value = university.id;
        option.innerHTML = university.name;
        university_select.append(option);
    }
});

university_select.addEventListener("change", function(){
    if (university_select.value !== 0){
        send("getFaculties", true, {
            "university_id": university_select.value
        }, function(data){
            for (faculty of data.data){
                let option = document.createElement('option');
                option.value = faculty.id;
                option.innerHTML = faculty.name;
                faculty_select.append(option);
            }
        });
    };
});

faculty_select.addEventListener("change", function(){
    if (faculty_select.value !== 0){
        send("getGroups", true, {
            "university_id": university_select.value,
            "faculty_id": faculty_select.value
        }, function(data){
            for (group of data.data){
                let option = document.createElement('option');
                option.value = group.id;
                option.innerHTML = group.name;
                group_select.append(option);
            }
        });
    };
});