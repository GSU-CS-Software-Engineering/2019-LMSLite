function navBarFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}

function showHideQuiz() {
    var x = document.getElementById("quizForm");
    x.style.display = "block";

    var y = document.getElementById("courseDesc");
    y.style.display = "none";

    var z = document.getElementById("hmwkForm");
    z.style.display = "none";
}

function showHideHmwk() {
    var x = document.getElementById("quizForm");
    x.style.display = "none";

    var y = document.getElementById("courseDesc");
    y.style.display = "none";

    var z = document.getElementById("hmwkForm");
    z.style.display = "block";
}

function showHideCourse() {
    var x = document.getElementById("quizForm");
    x.style.display = "none";

    var y = document.getElementById("courseDesc");
    y.style.display = "block";

    var z = document.getElementById("hmwkForm");
    z.style.display = "none";
}