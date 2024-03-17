const classLimit = 6; 

const hebToEngDays = {
    "ראשון": 0, // Sunday
    "שני": 1,   // Monday
    "שלישי": 2, // Tuesday
    "רביעי": 3, // Wednesday
    "חמישי": 4, // Thursday
    "שישי": 5,   // Friday
    "שבת": 6    // Saturday
};

function displayClasses() {
    axios.get("http://127.0.0.1:5000/api/classes").then(response=> {
        const classes = response.data;
        const days = new Set();
        const hours = new Set();

        classes.forEach(classItem=> {
            days.add(classItem.day);
            hours.add(classItem.hour);
        });

        const sortedDays = Array.from(days).sort((a, b) => {
            return hebToEngDays[a] - hebToEngDays[b];
        });
        const sortedHours = Array.from(hours).sort((a, b) => a - b);

        const table = document.createElement("table");
        const thead = document.createElement("thead");
        const tbody = document.createElement("tbody");
        const daysRow = document.createElement("tr");
        const emptyHeader = document.createElement("th");

        daysRow.appendChild(emptyHeader);

        sortedDays.forEach(day=> {
            const dayHeader = document.createElement("th");
            dayHeader.textContent = day;
            daysRow.appendChild(dayHeader);
        })

        thead.appendChild(daysRow);

        sortedHours.forEach(hour=> {
            const hourRow = document.createElement("tr");
            const hourHeader = document.createElement("th");
            hourHeader.textContent = `${hour}:00`;
            hourRow.appendChild(hourHeader);

            sortedDays.forEach(day => {
                const classForHourAndDay = classes.find(classItem => classItem.day === day && classItem.hour === hour);
                const classCell = document.createElement("td");
                const classCellDiv = document.createElement("div");
                classCellDiv.innerHTML = classForHourAndDay ? classForHourAndDay.className : "";
                const classButtonCell = document.createElement("button");

                if (classForHourAndDay && classForHourAndDay.subscribers < classLimit && classForHourAndDay.userInClass == false) {
                    classButtonCell.innerHTML = "הזמן שיעור";
                    classButtonCell.addEventListener("click", () => {
                        bookClass(classForHourAndDay);
                    });
                } else if (classForHourAndDay && classForHourAndDay.userInClass == true) {
                    classButtonCell.innerHTML = "שיעור מוזמן - הסר רישום"
                    classButtonCell.style.backgroundColor = "rgba(128, 0, 128, 0.58)";
                    classButtonCell.addEventListener("click", () => {
                       removeClass(classForHourAndDay);
                    });

                } else {
                    classButtonCell.innerHTML = "שיעור מלא";
                    classButtonCell.disabled = true;
                    classButtonCell.style.backgroundColor = "gray";
                    classButtonCell.style.cursor = "not-allowed";
 
                }  

                if (classForHourAndDay) {
                    classCell.appendChild(classCellDiv);
                    classCell.appendChild(classButtonCell);
                }
                
                hourRow.appendChild(classCell);
            });

            tbody.appendChild(hourRow);

        });

        table.appendChild(thead);
        table.appendChild(tbody);

        // Append the table to the DOM
        const classesContent = document.getElementById("classesContent");
        classesContent.innerHTML = ""; // Clear previous content
        classesContent.appendChild(table);
    });
}


displayClasses()

function bookClass(classForHourAndDay) {
    console.log(classForHourAndDay);

    axios.post('/api/classes/book', {id: classForHourAndDay.id}).then(response => {
        console.log("pass")
})
    location.reload();

}


function removeClass(classForHourAndDay) {
    console.log(classForHourAndDay);
    const confirmed = window.confirm("Are you sure you want to remove this class?");

    if (confirmed) {
        axios.post('/api/classes/remove', {id: classForHourAndDay.id}).then(response => {
            console.log("pass")
    })
        location.reload();
    }

}
