let group_title = document.getElementById("group");
let schedule = document.getElementById("schedule");
const days = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];
let xhr1 = new XMLHttpRequest();
xhr1.open("GET", "../api/getGroup/");
xhr1.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr1.setRequestHeader("Authorization", "Token " + localStorage.getItem("token"));
xhr1.send();
xhr1.onload = function() {
    group_title.innerHTML = JSON.parse(xhr1.response).name
};
var date = new Date();
let day = date.getDay();
let start = new Date(date - day + 1 * 24 * 60 * 60 * 1000);
start = start.toISOString();
let end = new Date(date - day + 7 * 24 * 60 * 60 * 1000);
end = end.toISOString();
let xhr2 = new XMLHttpRequest();
xhr2.open("GET", "../api/getLessons/");
xhr2.setRequestHeader("Content-Type", "application/json");
xhr2.setRequestHeader("Authorization", "Token " + localStorage.getItem("token"));
console.log(start.slice(0, start.indexOf("T")));
console.log(end.slice(0, end.indexOf("T")));
xhr2.send(JSON.stringify({"start": start.slice(0, start.indexOf("T")), "end": end.slice(0, end.indexOf("T"))}));
xhr2.onload = function() {
    var i = 1;
    for (let day of xhr2.response){
        let day_html = document.createElement("div");
        day_html.className = "day";
        let p1 = document.createElement("p");
        p1.className = "day-of-the-week";
        p1.innerHTML = days[i % 7];
        day_html.append(p1);
        let p2 = document.createElement("p");
        p2.className = "date";
        p2.innerHTML = start + 1;
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
                p1.innerHTML = lesson.time_start + " " + lesson.time_end;
                time.append(p1);
                head.append(time);
                let body = document.createElement("div");
                let name = document.createElement("p");
                name.className = lesson-name;
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