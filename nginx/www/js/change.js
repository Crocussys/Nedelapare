var date_changed = true;

send("getLesson", true, {
    "id": params.get("id")
}, function(data, status){
    subject.value = data["subject"];
    document.getElementById('one_day').value = data["date"];
    start_time.value = data["time_start"];
    end_time.value = data["time_end"];
    let lesson_type = data["type_of_work"];
    if (lesson_type === "Лекция"){
        type_of_work_selected = 0;
    }else if (lesson_type === "Практика"){
        type_of_work_selected = 1;
    }else if (lesson_type === "Лаб. работа"){
        type_of_work_selected = 2;
    }else{
        type_of_work_selected = 3;
        type_other.value = lesson_type;
    }
    click_type();
    let place = data["place"];
    let place_slice = place.slice(0, place.indexOf(" "));
    let place_select = document.getElementById('place-select');
    if (place_slice == "Аудитория"){
        place_select.options[1].selected = true;
        document.getElementById('place-other').value = place.slice(place.indexOf(" ") + 1);
    }else if (place_slice == "Кабинет"){
        place_select.options[2].selected = true;
        document.getElementById('place-other').value = place.slice(place.indexOf(" ") + 1);
    }else if (place_slice == "Online"){
        place_select.options[3].selected = true;
        document.getElementById('place-other').value = place.slice(place.indexOf(" ") + 1);
    }else{
        place_select.options[0].selected = true;
        document.getElementById('place-other').value = place;
    }
    teacher.value = data["teacher"]["name"];
    document.getElementById('home_work').innerHTML = data["home_work"];
})

document.getElementById('one_day').addEventListener("change", function(){
    if (date_changed){
        document.getElementById('add-save2').remove();
        document.getElementById('add-save3').remove();
        date_changed = false;
    }
})

function delete_lessons(x){
    send("deleteLessons", true, {
        "id": params.get("id"),
        "others": x
    }, function(){
        location.href='/schedule';
    })
}