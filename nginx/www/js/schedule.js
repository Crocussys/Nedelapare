let group_title = document.getElementById("group-name");
let schedule = document.getElementById("schedule");
const days = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];
let xhr_getGroup = new XMLHttpRequest();
xhr_getGroup.open("POST", "/api/getGroup/");
xhr_getGroup.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr_getGroup.setRequestHeader("Authorization", "Token " + localStorage.getItem("token"));
xhr_getGroup.send();
xhr_getGroup.onload = function() {
    if (xhr_getGroup.status === 404){
        location.href = "/group_change"
    }else{
        group_title.innerHTML = JSON.parse(xhr_getGroup.response).name
    }
};
let date = new Date();
let day = date.getDay();
let start = new Date(date - day * 24 * 60 * 60 * 1000 + 1 * 24 * 60 * 60 * 1000);
start = start.toISOString();
let end = new Date(date - day * 24 * 60 * 60 * 1000 + 7 * 24 * 60 * 60 * 1000);
end = end.toISOString();
let xhr_getLessons = new XMLHttpRequest();
xhr_getLessons.open("POST", "/api/getLessons/");
xhr_getLessons.setRequestHeader("Content-Type", "application/json");
xhr_getLessons.setRequestHeader("Authorization", "Token " + localStorage.getItem("token"));
xhr_getLessons.send(JSON.stringify({"start": start.slice(0, start.indexOf("T")), "end": end.slice(0, end.indexOf("T"))}));
xhr_getLessons.onload = function() {
    var i = 1;
    for (let day of JSON.parse(xhr_getLessons.response)){
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
                let border = document.createElement("div");
                border.className = "border";
                lesson_html.append(border);
                lessons_html.append(lesson_html);
            }
        }
        schedule.append(lessons_html);
        i += 1;
    }
};