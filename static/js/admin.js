function adminSection(event) {
    let usersSection = document.getElementById("usersSection")
    let leadsSection = document.getElementById("leadsSection")
    let classesSection = document.getElementById("classesSection")
    if (event.target.id=="leadsButton") {
        usersSection.style.display = "none"
        classesSection.style.display = "none"
        leadsSection.style.display = "flex"

    } else if (event.target.id=="usersButton") {
        usersSection.style.display = "flex"
        classesSection.style.display = "none"
        leadsSection.style.display = "none"

    } else if (event.target.id=="classesButton") {
        usersSection.style.display = "none"
        classesSection.style.display = "flex"
        leadsSection.style.display = "none"
    } 

}

function addUserSection() {
    let addUserForm = document.getElementById("addUserForm")
    addUserForm.style.display = "flex"
}

function addClassSection() {
    let addClassForm = document.getElementById("addClassForm")
    addClassForm.style.display = "flex"
}