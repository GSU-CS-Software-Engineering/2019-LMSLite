function newQuestion() {
  event.preventDefault();

  var i = document.querySelectorAll("label[for*=id_Question]:not([for*=Answer])").length + 1;

  var quizForm = document.getElementById("quizForm");

  var p1 = document.createElement("p");
  p1.setAttribute("id", "pExtender"+i);

  var selection = document.createElement("select");
  selection.setAttribute("id", "Question" +i+ "type");
  selection.setAttribute("name", "Question" +i+ "type");

  var z1 = document.createElement("option");z1.setAttribute("value", "1");
  var t1 = document.createTextNode("MC");z1.appendChild(t1);

  var z2 = document.createElement("option");z2.setAttribute("value", "6");
  var t2 = document.createTextNode("ESS");z2.appendChild(t2);

  var z3 = document.createElement("option");z3.setAttribute("value", "3");
  var t3 = document.createTextNode("MA");z3.appendChild(t3);

  var z4 = document.createElement("option");z4.setAttribute("value", "4");
  var t4 = document.createTextNode("FIB");z4.appendChild(t4);

  var z5 = document.createElement("option");z5.setAttribute("value", "5");
  var t5 = document.createTextNode("TF");z5.appendChild(t5);

  var z6 = document.createElement("option");z6.setAttribute("value", "2");
  var t6 = document.createTextNode("SR");z6.appendChild(t6);

  var z7 = document.createElement("option");z7.setAttribute("value", "7");
  var t7 = document.createTextNode("");z7.appendChild(t7);

  quizForm.appendChild(p1);
  p1.appendChild(selection);
  selection.appendChild(z7);selection.appendChild(z1);selection.appendChild(z2);
  selection.appendChild(z3);selection.appendChild(z4);selection.appendChild(z5);
  selection.appendChild(z6);

  var p = document.createElement("p");
  p.setAttribute("id", "paragraphExtender"+i);

  var qlabel = document.createElement("label");
  qlabel.setAttribute("for", "id_Question"+i);

  var t = document.createTextNode("Question "+i+ " ");
  qlabel.appendChild(t);

  var sQ = document.getElementById("Question"+i+"type").selectedIndex;
  var sName = document.getElementById("Question"+i+"type").options;

  var qtArea = document.createElement("TextArea");
  qtArea.setAttribute("for", "id_Question"+i);
  qtArea.setAttribute("placeholder", sName[sQ].text +" Question Here");

  qtArea.setAttribute("cols", "40");
  qtArea.setAttribute("rows" , "1");
  qtArea.setAttribute("style", "height: 5rem");
  qtArea.setAttribute("maxlength", "1000");

  quizForm.appendChild(p);
  p.appendChild(qlabel);
  p.appendChild(qtArea);
}
