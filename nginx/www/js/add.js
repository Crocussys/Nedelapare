var DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];
var WEEKS = ["Чётная", "Нечётная"]
var TYPE_ELEMS = ["type-lecture", "type-practice", "type-lab"]

var day_selected = [];
var even_odd_selected = 0;
var type_of_work_selected = 0;

var style = getComputedStyle(document.documentElement);
var params = new URLSearchParams(document.location.search);

var type_lecture = document.getElementById('type-lecture');
var type_practice = document.getElementById('type-practice');
var type_lab = document.getElementById('type-lab');
var type_other = document.getElementById('type-other');

// var subject = document.getElementById('subject');
var week_select = document.getElementById('week-select');
var start_time = document.getElementById('start_time');
var end_time = document.getElementById('end_time');
var teacher = document.getElementById('teacher');

// function jump(x){
//     console.log(x.value);
//     if (x.value.lenght >= 4){
//         do {
//             x = x.nextSibling;
//         } while (!(/time/.test(x.type)));
//         x.focus();
//     }
// }

function click_day(){
    if (week_select.value > 0){
        let elems = document.getElementById('add_week').children;
        for (let i = 0; i < elems.length; i++){
            let elem = elems[i];
            let flag = true;
            for (let j = 0; j < day_selected.length; j++){
                if (day_selected[j] === i){
                    elem.style.backgroundColor = style.getPropertyValue("--main-blue-color");
                    let p = elem.children[0];
                    p.style.color = style.getPropertyValue("--white-color");
                    flag = false;
                    break
                }
            }
            if (flag){
                elem.style.borderColor = style.getPropertyValue("--main-blue-color");
                elem.style.backgroundColor = style.getPropertyValue("--white-color");
                let p = elem.children[0];
                p.style.color = style.getPropertyValue("--main-blue-color");
            }
        }
    }
}

function click_days(i){
    let flag = true;
    for (let j = 0; j < day_selected.length; j++){
        if (day_selected[j] == i){
            day_selected.splice(j, 1);
            flag = false;
            break;
        }
    }
    if (flag){
        day_selected.push(i);
    }
}

function click_even_odd(){
    if (week_select.value == 2){
        let elems = document.getElementById('even-odd').children;
        for (let i = 0; i < elems.length; i++){
            let elem = elems[i];
            if (i === even_odd_selected){
                elem.style.backgroundColor = style.getPropertyValue("--main-blue-color");
                let p = elem.children[0];
                p.style.color = style.getPropertyValue("--white-color");
            } else {
                elem.style.borderColor = style.getPropertyValue("--main-blue-color");
                elem.style.backgroundColor = style.getPropertyValue("--white-color");
                let p = elem.children[0];
                p.style.color = style.getPropertyValue("--main-blue-color");
            }
        }
    }
}

function click_type(){
    for (let i = 0; i < 3; i++){
        let elem = document.getElementById(TYPE_ELEMS[i]);
        if (i === type_of_work_selected){
            elem.style.backgroundColor = style.getPropertyValue("--main-blue-color");
            let p = elem.children[0];
            p.style.color = style.getPropertyValue("--white-color");
        } else {
            elem.style.borderColor = style.getPropertyValue("--main-blue-color");
            elem.style.backgroundColor = style.getPropertyValue("--white-color");
            let p = elem.children[0];
            p.style.color = style.getPropertyValue("--main-blue-color");
        }
    }
}

function add_week(elem){
    let block = document.createElement("div");
    block.className = "add-week";
    block.id = "add_week";
    block.onclick = click_day;
    for (let i = 0; i < 7; i++){
        let day = document.createElement("div");
        day.className = "add-week-days";
        day.onclick = () => {
            click_days(i);
        };
        let p = document.createElement("p");
        p.innerHTML = DAYS[i];
        day.append(p);
        block.append(day);
    }
    elem.append(block);
    click_day();
}

function get_dates(response, every, start=null, even=false, odd=false){
    let ans = [];
    let start_semester = Date.parse(response["start_semester"])
    let end_semester = Date.parse(response["end_semester"])
    let pointer = Date.parse(response["monday_first_week"])
    let week = 1;
    while (pointer > start_semester){
        pointer -= 7 * 24 * 60 * 60 * 1000;
        week -= 1;
    }
    if (start === null){
        start = week;
    }
    while (week < start){
        pointer += 7 * 24 * 60 * 60 * 1000;
        week += 1;
    }
    if ((even && week % 2 == 1) || (odd && week % 2 == 0)){
        pointer += 7 * 24 * 60 * 60 * 1000;
        week += 1;
    }
    for (let i = 0; i < day_selected.length; i++){
        let day = new Date(pointer + day_selected[i] * 24 * 60 * 60 * 1000);
        while (day <= end_semester){
            if (day >= start_semester){
                let day_str = day.toISOString();
                ans.push(day_str.slice(0, day_str.indexOf("T")));
            }
            day.setDate(day.getDate() + 7 * every);
        }
    }
    return ans;
}

if (params.size == 0){
    click_day();
    click_type();
    var repetition = document.getElementById('repetition');
    week_select.addEventListener("change", function(){
        repetition.innerHTML = "";
        if (week_select.value == 0){
            let block = document.createElement("div");
            block.className = "add-week";
            let inp = document.createElement("input");
            inp.className = "add-week-day";
            inp.id = "one_day";
            inp.type = "date";
            inp.valueAsDate = new Date();
            block.append(inp);
            repetition.append(block);
        } else if (week_select.value == 1){
            add_week(repetition)
        } else if (week_select.value == 2){
            let block = document.createElement("div");
            block.className = "add-week";
            block.id = "even-odd";
            block.onclick = click_even_odd;
            for (let i = 0; i < 2; i++){
                let day = document.createElement("div");
                day.className = "add-button";
                day.onclick = () => {even_odd_selected = i};
                let p = document.createElement("p");
                p.innerHTML = WEEKS[i];
                day.append(p);
                block.append(day);
            }
            repetition.append(block);
            add_week(repetition);
            click_even_odd()
        } else if (week_select.value == 3){
            let block = document.createElement("div");
            block.className = "add-week";
            let p1 = document.createElement("p");
            p1.className = "add-text";
            p1.innerHTML = "Каждые";
            block.append(p1);
            let inp = document.createElement("input");
            inp.className = "add-week-week";
            inp.id = "inp-week-1";
            inp.type = "number";
            inp.value = 3;
            inp.min = 1;
            block.append(inp);
            let p2 = document.createElement("p");
            p2.className = "add-text";
            p2.innerHTML = "недели, начиная с";
            p2.style.marginLeft = "17px";
            block.append(p2);
            let inp2 = document.createElement("input");
            inp2.className = "add-week-week";
            inp2.id = "inp-week-2";
            inp2.type = "number";
            inp2.value = 1;
            block.append(inp2);
            let p3 = document.createElement("p");
            p3.className = "add-text";
            p3.innerHTML = "недели";
            p3.style.marginLeft = "17px";
            block.append(p3);
            repetition.append(block);
            add_week(repetition);
        } else if (week_select.value == 4){
            let block = document.createElement("div");
            block.className = "add-week";
            let inp = document.createElement("input");
            inp.className = "add-weeks";
            inp.id = "inp-weeks";
            inp.placeholder = "Номера недель через пробел";
            block.append(inp);
            repetition.append(block);
            add_week(repetition);
        }
    })
}
