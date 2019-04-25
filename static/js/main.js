function navBarFunction() {
    event.preventDefault();
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}

function showHideQuiz() {
    event.preventDefault();
    var x = document.getElementById("quizForm");
    x.style.display = "block";

    var y = document.getElementById("courseDesc");
    y.style.display = "none";

    var z = document.getElementById("hmwkForm");
    z.style.display = "none";

    var z = document.getElementById("surveyForm");
    z.style.display = "none";
}

function showHideHmwk() {
    event.preventDefault();
    var x = document.getElementById("quizForm");
    x.style.display = "none";

    var y = document.getElementById("courseDesc");
    y.style.display = "none";

    var z = document.getElementById("hmwkForm");
    z.style.display = "block";

    var z = document.getElementById("surveyForm");
    z.style.display = "none";
}

function showHideCourse() {
    event.preventDefault();
    var x = document.getElementById("quizForm");
    x.style.display = "none";

    var y = document.getElementById("courseDesc");
    y.style.display = "block";

    var z = document.getElementById("hmwkForm");
    z.style.display = "none";

    var z = document.getElementById("surveyForm");
    z.style.display = "none";
}

function showHideSurvey() {
    event.preventDefault();
    var x = document.getElementById("quizForm");
    x.style.display = "none";

    var y = document.getElementById("courseDesc");
    y.style.display = "none";

    var z = document.getElementById("hmwkForm");
    z.style.display = "none";

    var p = document.getElementById("surveyForm");
    p.style.display = "block";
}