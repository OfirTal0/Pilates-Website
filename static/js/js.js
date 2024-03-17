
function classInfo(event) {
    let classname = event.target;
    classname.style.backgroundImage = "none";
    classname.style.backgroundColor = "rgba(130, 85, 130)"
    let classNumber = classname.id.split("class")[1];
    classname.style.color = "white"; 

    switch(classNumber) {
        case "1":
            classname.innerHTML = "HTML content for class 1";

            break;
        case "2":
            classname.innerHTML = "HTML content for class 2";
            break;
        case "3":
            classname.innerHTML = "HTML content for class 3";
            break;
        default:
            classname.innerHTML = "";
    }
}

function classBasic(event) {
    let classname = event.target;
    let classNumber = classname.id.split("class")[1];

    switch(classNumber) {
        case "1":
            classname.innerHTML = "";
            classname.style.backgroundImage = "url('/static/images/class1name.png')";
            break;
        case "2":
            classname.innerHTML = "";
            classname.style.backgroundImage = "url('/static/images/class2name.png')";
            break;
        case "3":
            classname.innerHTML = "";
            classname.style.backgroundImage = "url('/static/images/class2name.png')";
            break;
        default:
            classname.innerHTML = "";
    }
}

document.getElementById('leadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    var formData = new FormData(event.target);
    axios.post('/new_lead', formData)
    .then(function (response) {
        document.getElementById('יצירת-קשר').scrollIntoView({behavior: 'smooth'});
    })
    document.getElementById('contactForm').style.display = "none";
    document.getElementById('contactSubmit').style.display = "flex";
});

function validateLogin(){
        let message = document.getElementById("message");
        message.innerHTML = "";
        let valid=true;
        Array.from(document.getElementById("loginForm").getElementsByTagName("input")).map(
            item=>{
                if (item.value==""){
                    message.innerHTML+=`Please fill out the ${item.name} <br>`;
                    item.style.backgroundColor="pink";
                    valid=false;
                }
            })
        if (valid){
            document.getElementById("loginForm").submit();
        }
    }


    var slideIndex = 0;

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("image-slide");
    
    if (n >= slides.length - 3) { // Change condition to slides.length - 3
        slideIndex = 0;
    } 
    if (n < 0) {
        slideIndex = slides.length - 4; // Change to slides.length - 4
    }
    
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    
    slides[slideIndex].style.display = "block";  
    slides[slideIndex + 1].style.display = "block"; // Show the next slide
    slides[slideIndex + 2].style.display = "block"; // Show the next slide
    slides[slideIndex + 3].style.display = "block"; // Show the next slide
}