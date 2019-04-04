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

function removeElement(elementId){
    var element = document.getElementById(elementId);
    element.parentNode.removeChild(element);


}
function addElement(parentId, elementTag, elementId, html) {
    // Adds an element to the document
    var p = document.getElementById(parentId);
    var newElement = document.createElement(elementTag);
    newElement.setAttribute('id', elementId);
    newElement.innerHTML = html;
    p.appendChild(newElement);
}