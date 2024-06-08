var days = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];

var group_title = document.getElementById("group-name");
var schedule = document.getElementById("schedule");
var lesson_change = document.getElementById("lesson-change");

var date = new Date();

var monday_first_week = 0;
var isLoading = false;
var week = 0;

send("getGroup", true, {}, get_group)

function get_group(response, status){
    if (status === 404){
        location.href = "/group_change"
    }else{
        let data = JSON.parse(response)
        group_title.innerHTML = data.name;
        monday_first_week = Date.parse(data.monday_first_week);
        week = Math.ceil((date - monday_first_week) / 86400000 / 7);
        click_week(0);
    }
}

function get_lesson(id){
    send("getLesson", true, {
        "id": id
    }, function(response, status){
        let data = JSON.parse(response);
        document.getElementById("change-name").innerHTML = data["subject"];
        let time_start = data["time_start"];
        let time_end = data["time_end"];
        document.getElementById("change-time").innerHTML = time_start.slice(0, time_start.lastIndexOf(":")) + "-" + time_end.slice(0, time_end.lastIndexOf(":"));
        document.getElementById("change-group").innerHTML = data["group"];
        document.getElementById("change-type").innerHTML = data["type_of_work"];
        document.getElementById("change-place").innerHTML = data["place"];
        document.getElementById("change-teacher").innerHTML = "Преподаватель: " + data["teacher"]["name"];
        document.getElementById("change-home_work").innerHTML = data["home_work"];
        document.getElementById("change-button").onclick = () => {
            location.href='/change/?id=' + id;
        }
        lesson_change.style.width = "40%";
        lesson_change.style.padding = "35px 105px";
    })
}

function click_week(x){
    if (x === -1){
        week -= 1;
    }else if (x === 1){
        week += 1;
    }
    let start = new Date(monday_first_week + (week - 1) * 7 * 24 * 60 * 60 * 1000);
    let end = new Date(monday_first_week + week * 7 * 24 * 60 * 60 * 1000 - 24 * 60 * 60 * 1000);
    let start_str = start.toISOString();
    let end_str = end.toISOString();
    document.getElementById("prev_week").innerHTML = week - 1;
    document.getElementById("next_week").innerHTML = week + 1;
    send("getLessons", true, {
        "start": start_str.slice(0, start_str.indexOf("T")),
        "end": end_str.slice(0, end_str.indexOf("T"))
    }, get_lessons);
}

function restore(){
    lesson_change.style.width = "0px";
    lesson_change.style.padding = "0px";
}

function get_lessons(response, status) {
    schedule.innerHTML = "";
    var i = 1;
    for (let day of JSON.parse(response)){
        let day_html = document.createElement("div");
        day_html.className = "day";
        let p1 = document.createElement("p");
        p1.className = "day-of-the-week";
        p1.innerHTML = days[i % 7];
        day_html.append(p1);
        let p2 = document.createElement("p");
        p2.className = "date";
        let date_arr = day.day.split("-");
        p2.innerHTML = date_arr[2] + "." + date_arr[1];
        day_html.append(p2);
        schedule.append(day_html);
        let lessons_html = document.createElement("div");
        lessons_html.className = "lessons";
        let lessons = day.lessons;
        if (lessons.length === 0){
            let p1 = document.createElement("p");
            p1.className = "empty";
            p1.innerHTML = "Пусто";
            lessons_html.append(p1);
        }else{
            for (lesson of lessons){
                let lesson_html = document.createElement("div");
                lesson_html.className = "lesson";
                lesson_html.value = lesson.id;
                lesson_html.onclick = () => {get_lesson(lesson_html.value)};
                let head = document.createElement("div");
                head.className = "lesson-head";
                let time = document.createElement("div");
                time.className = "time";
                let p1 = document.createElement("p");
                let time_start = lesson.time_start;
                let time_end = lesson.time_end;
                p1.innerHTML = time_start.slice(0, time_start.lastIndexOf(":")) + " " + time_end.slice(0, time_end.lastIndexOf(":"));
                time.append(p1);
                head.append(time);
                let body = document.createElement("div");
                let name = document.createElement("p");
                name.className = "lesson-name";
                name.innerHTML = lesson.subject;
                body.append(name);
                let type = document.createElement("p");
                type.className = "other-info";
                type.innerHTML = lesson.type_of_work;
                body.append(type);
                if (lesson.place !== null){
                    let place = document.createElement("p");
                    place.className = "other-info";
                    place.innerHTML = lesson.place;
                    body.append(place);
                }
                head.append(body);
                lesson_html.append(head)
                lessons_html.append(lesson_html);
            }
        }
        schedule.append(lessons_html);
        i += 1;
    }
};