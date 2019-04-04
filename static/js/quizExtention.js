


function newQuestion() {
    var i = document.querySelectorAll("label[for*=id_Question]:not([for*=Answer])").length + 1;
  var selection = document.getElementById("Questiontype").selectedIndex;
  var selectName = document.getElementById("Questiontype").options;

  var quizForm = document.getElementById("quizForm");
  var p = document.createElement("p");
  p.setAttribute("id", "paragraphExtender"+i);

  var qlabel = document.createElement("label");
  qlabel.setAttribute("for", "id_Question"+i);

  var t = document.createTextNode("Question "+i+ " ");
  qlabel.appendChild(t);

  var qtArea = document.createElement("TextArea");
  qtArea.setAttribute("for", "id_Question"+i);
  qtArea.setAttribute("placeholder", selectName[selection].text +" Question Here");

  qtArea.setAttribute("cols", "40");
  qtArea.setAttribute("rows" , "1");
  qtArea.setAttribute("style", "height: 5rem");
  qtArea.setAttribute("maxlength", "1000");

  quizForm.appendChild(p);
  p.appendChild(qlabel);
  p.appendChild(qtArea);

  var showAns=document.getElementById("qSec");
  document.getElementById("demo").innerHTML= showAns.innerHTML;

  i++;


}
