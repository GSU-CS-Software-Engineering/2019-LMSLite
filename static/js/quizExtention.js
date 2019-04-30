//This function creates the delete button for each question
function updateMAcheckbox(updatedid) {
    var x = document.getElementById(updatedid).value;
    document.getElementById(updatedid).previousElementSibling.value = x;
}

function quizEditPageLoad() {
    event.preventDefault();
         document.getElementById("quizQuestionBtn").style.display = "inline-block";
         var x = document.querySelectorAll("select[id*=id_Question]").length;
         var count = 1;

         var z = document.querySelectorAll("select[id*=type]");

         for (var i = 0; i < z.length; i++) {
             z[i].setAttribute("onchange", "newAnswer(this.id)");
         }

         for (var i = 0; i < x; i++) {
             var deleteBtn = document.createElement("button");
             deleteBtn.setAttribute("id", "deleteBtn " + count);
             deleteBtn.setAttribute("onclick", "deleteElements(this.id)");
             var t = document.createTextNode("Delete Question " + count);
             deleteBtn.appendChild(t);
             var parentP = document.getElementById("id_Question" + (i + 1) + "type").parentNode;
             parentP.insertBefore(deleteBtn, document.getElementById("id_Question" + (i + 1) + "type"));
             count++;

             var e = document.getElementById("id_Question" + (i + 1) + "type");
             var countanswers = document.querySelectorAll("label[for*=id_Question" + (i + 1) + "Answer]").length;

             var arp = document.createElement("p");

             var adda = document.createElement("Button");
             var a = document.createTextNode("+ Answer");
             adda.appendChild(a);
             adda.setAttribute("id", "id_addAnswerBtn " + (i + 1));
             adda.setAttribute("onclick", "addLastAnswer(this.id)");

             var removea = document.createElement("Button");
             var r = document.createTextNode("- Answer");
             removea.appendChild(r);
             removea.setAttribute("id", "id_removeAnswerBtn " + (i + 1));
             removea.setAttribute("onclick", "deleteLastAnswer(this.id)");

             var line = document.createElement("hr");

             if (i < (x - 1)) {
                 var parentnextQ = document.getElementById("id_Question" + (i + 2) + "type").parentNode;
             } else if (i == x - 1) {
                 var parentnextQ = document.getElementById("quizQuestionBtn").parentNode;
             }

             if (e.options[e.selectedIndex].text == "MC") {
                 for (var j = 1; j <= countanswers; j++) {
                     var radio = document.createElement('input');
                     radio.type = "radio";
                     radio.name = "Question" + (i + 1) + "RadioGrp";
                     radio.value = "radio";
                     radio.id = "id_EQuestion" + (i + 1) + "Radio" + j;

                     var answerBx = document.getElementById("id_Question" + (i + 1) + "Answer" + j);
                     answerBx.parentNode.insertBefore(radio, answerBx);
                 }


                 arp.appendChild(adda);
                 arp.appendChild(removea);
                 parentnextQ.parentNode.insertBefore(arp, parentnextQ);
             } else if (e.options[e.selectedIndex].text == "MA") {
                 for (var j = 1; j <= countanswers; j++) {
                     var checkbox = document.createElement('input');
                     checkbox.type = "checkbox";
                     checkbox.name = "Question" + (i + 1) + "CheckboxGrp"
                     checkbox.value = document.getElementById("id_Question" + (i + 1) + "Answer" + j).innerText;
                     checkbox.id = "id_EQuestion" + (i + 1) + "Checkbox" + j;

                     var answerBx = document.getElementById("id_Question" + (i + 1) + "Answer" + j);
                     answerBx.parentNode.insertBefore(checkbox, answerBx);
                 }

                 arp.appendChild(adda);
                 arp.appendChild(removea);
                 parentnextQ.parentNode.insertBefore(arp, parentnextQ);
             }
             parentnextQ.parentNode.insertBefore(line, parentnextQ);
         }

         var quizformlength = document.getElementById("quizForm").length;
         var surveyformlength = document.getElementById("surveyForm").length;
         var courseformlength = document.getElementById("courseDesc").length;

         if (quizformlength > surveyformlength) {
             var x = document.getElementById("quizForm");
             x.style.display = "block";

             var y = document.getElementById("courseDesc");
             y.style.display = "none";

             var z = document.getElementById("hmwkForm");
             z.style.display = "none";

             var t = document.getElementById("surveyForm");
             t.style.display = "none";
         }
         else if (surveyformlength > quizformlength) {
             var t = document.getElementById("surveyForm");
             t.style.display = "block";

             var x = document.getElementById("quizForm");
             x.style.display = "none";

             var y = document.getElementById("courseDesc");
             y.style.display = "none";

             var z = document.getElementById("hmwkForm");
             z.style.display = "none";
         } else {
             var t = document.getElementById("surveyForm");
             t.style.display = "none";

             var x = document.getElementById("quizForm");
             x.style.display = "none";

             var y = document.getElementById("courseDesc");
             y.style.display = "block";

             var z = document.getElementById("hmwkForm");
             z.style.display = "none";
         }
}

//adds new questions including delete button and dropdown box
function newQuestion() {
    event.preventDefault();

    var i = document.querySelectorAll("label[for*=id_Question]:not([for*=Answer])").length;

    var updateDeleteLabel = 1;

    if (i != 0) {
        var deleteBtnContent = document.querySelectorAll("button[id*='deleteBtn ']");
        var last = deleteBtnContent[deleteBtnContent.length - 1].id;
        var splitBtnName = last.split(" ");
        var num2 = splitBtnName[1];
        var updateDeleteLabel = Number(num2) + 1;
    }

    var quizForm = document.getElementById("quizForm");

    var p1 = document.createElement("p");
    p1.setAttribute("id", "pExtender" + updateDeleteLabel);

    var deleteBtn = document.createElement("button");
    deleteBtn.setAttribute("id", "deleteBtn " + updateDeleteLabel);
    deleteBtn.setAttribute("onclick", "deleteElements(this.id)");
    var tx = document.createTextNode("Delete Question " + (i + 1));
    deleteBtn.appendChild(tx);

    var selection = document.createElement("select");
    selection.setAttribute("id", "id_Question" + updateDeleteLabel + "type");
    selection.setAttribute("name", "Question" + updateDeleteLabel + "type");
    selection.setAttribute("onchange", "newAnswer(this.id)")

    var z1 = document.createElement("option");
    z1.setAttribute("value", "1");
    var t1 = document.createTextNode("MC");
    z1.appendChild(t1);

    var z2 = document.createElement("option");
    z2.setAttribute("value", "6");
    var t2 = document.createTextNode("ESS");
    z2.appendChild(t2);

    var z3 = document.createElement("option");
    z3.setAttribute("value", "3");
    var t3 = document.createTextNode("MA");
    z3.appendChild(t3);

    var z4 = document.createElement("option");
    z4.setAttribute("value", "4");
    var t4 = document.createTextNode("FIB");
    z4.appendChild(t4);

    var z5 = document.createElement("option");
    z5.setAttribute("value", "5");
    var t5 = document.createTextNode("TF");
    z5.appendChild(t5);

    var z6 = document.createElement("option");
    z6.setAttribute("value", "2");
    var t6 = document.createTextNode("SR");
    z6.appendChild(t6);

    var z7 = document.createElement("option");
    z7.setAttribute("value", "7");
    var t7 = document.createTextNode("");
    z7.appendChild(t7);

    quizForm.insertBefore(p1, document.getElementById("quizEditExtension"));
    p1.appendChild(deleteBtn);
    p1.appendChild(selection);
    selection.appendChild(z7);
    selection.appendChild(z1);
    selection.appendChild(z2);
    selection.appendChild(z3);
    selection.appendChild(z4);
    selection.appendChild(z5);
    selection.appendChild(z6);

    var p = document.createElement("p");
    p.setAttribute("id", "paragraphExtender" + updateDeleteLabel);

    var qlabel = document.createElement("label");
    qlabel.setAttribute("for", "id_Question " + updateDeleteLabel);

    var t = document.createTextNode("Question " + (i + 1) + ":");
    qlabel.appendChild(t);

    var sQ = document.getElementById("id_Question" + updateDeleteLabel + "type").selectedIndex;
    var sName = document.getElementById("id_Question" + updateDeleteLabel + "type").options;

    var qtArea = document.createElement("TextArea");
    qtArea.setAttribute("for", "id_Question " + updateDeleteLabel);
    qtArea.setAttribute("placeholder", sName[sQ].text + " Question Here");
    qtArea.setAttribute("cols", "40");
    qtArea.setAttribute("rows", "1");
    qtArea.setAttribute("style", "height: 5rem");
    qtArea.setAttribute("maxlength", "1000");
    qtArea.setAttribute("id", "id_Question " + updateDeleteLabel);

    quizForm.insertBefore(p, document.getElementById("quizEditExtension"));
    p.appendChild(qlabel);
    p.appendChild(qtArea);

    var line = document.createElement("hr");
    quizForm.insertBefore(line, document.getElementById("quizEditExtension"));

    window.scrollBy(0, 250);
}

//creates answers for question
function newAnswer(ddid) {
    event.preventDefault();
    var dropdownnum = ddid.match(/\d+/)[0];
    var e = document.getElementById(ddid);

    for (var i = 1; i < 100; i++) {
        if (document.getElementById("id_Question" + dropdownnum + "Answer" + i)) {
            var aParent = document.getElementById("id_Question" + dropdownnum + "Answer" + i).parentNode;
            aParent.remove();
        } else {
            break;
        }
    }

    var arp = document.createElement("p");

    var adda = document.createElement("Button");
    var a = document.createTextNode("+ Answer");
    adda.appendChild(a);
    adda.setAttribute("id", "id_addAnswerBtn " + dropdownnum);
    adda.setAttribute("onclick", "addLastAnswer(this.id)");

    var removea = document.createElement("Button");
    var r = document.createTextNode("- Answer");
    removea.appendChild(r);
    removea.setAttribute("id", "id_removeAnswerBtn " + dropdownnum);
    removea.setAttribute("onclick", "deleteLastAnswer(this.id)");

    if (e.options[e.selectedIndex].text == "MC") {
        for (var i = 1; i < 5; i++) {
            var panswer = document.createElement("p");
            var alabel = document.createElement("label");
            alabel.setAttribute("for", "id_Question" + dropdownnum + "Answer" + i);
            var t = document.createTextNode("Answer " + i + ":");
            alabel.appendChild(t);

            var qanswer = document.createElement("textarea");
            qanswer.setAttribute("id", "id_Question" + dropdownnum + "Answer" + i);

            var radio = document.createElement('input');
            radio.type = "radio";
            radio.name = "Question" + dropdownnum + "RadioGrp";
            radio.value = "radio";
            radio.id = "id_EQuestion" + dropdownnum + "Radio" + i;

            panswer.appendChild(alabel);
            var ddparent = document.getElementById(ddid).parentNode;
            var ddParSibling = ddparent.nextElementSibling;

            for (var j = i; j > 0; j--) {
                panswer.appendChild(radio);
                panswer.appendChild(qanswer);

                ddParSibling = ddParSibling.nextElementSibling;
                var ddpsPar = ddParSibling.parentNode;
                ddpsPar.insertBefore(panswer, ddParSibling);

                if (j == 1 && i == 4 && document.getElementById("id_removeAnswerBtn " + dropdownnum) ==null) {
                    arp.appendChild(adda);
                    arp.appendChild(removea);
                    ddpsPar.insertBefore(arp, ddParSibling);
                }
            }
        }
    } else if (e.options[e.selectedIndex].text == "MA") {
        for (var i = 1; i < 5; i++) {
            var panswer = document.createElement("p");
            var alabel = document.createElement("label");
            alabel.setAttribute("for", "id_Question" + dropdownnum + "Answer" + i);
            var t = document.createTextNode("Answer " + i + ":");
            alabel.appendChild(t);

            var qanswer = document.createElement("textarea");
            qanswer.setAttribute("id", "id_Question" + dropdownnum + "Answer" + i);
            qanswer.setAttribute("onchange","updateMAcheckbox(this.id)");

            var checkbox = document.createElement('input');
            checkbox.type = "checkbox";
            checkbox.name = "Question" + dropdownnum + "CheckboxGrp"
            checkbox.value = "value";
            checkbox.id = "id_EQuestion" + dropdownnum + "Checkbox" + i;
            panswer.appendChild(alabel);

            var ddparent = document.getElementById(ddid).parentNode;
            var ddParSibling = ddparent.nextElementSibling;

            for (var j = i; j > 0; j--) {
                panswer.appendChild(checkbox);
                panswer.appendChild(qanswer);

                ddParSibling = ddParSibling.nextElementSibling;
                var ddpsPar = ddParSibling.parentNode;
                ddpsPar.insertBefore(panswer, ddParSibling);

                if (j == 1 && i == 4 && document.getElementById("id_removeAnswerBtn " + dropdownnum) ==null) {
                    arp.appendChild(adda);
                    arp.appendChild(removea);
                    ddpsPar.insertBefore(arp, ddParSibling);
                }
            }

        }
    } else if (e.options[e.selectedIndex].text == "FIB" || e.options[e.selectedIndex].text == "SR" || e.options[e.selectedIndex].text == "TF") {
        var panswer = document.createElement("p");
        var alabel = document.createElement("label");
        alabel.setAttribute("for", "id_Question" + dropdownnum + "Answer1");
        var t = document.createTextNode("Answer 1:");
        alabel.appendChild(t);

        var qanswer = document.createElement("textarea");
        qanswer.setAttribute("id", "id_Question" + dropdownnum + "Answer1");
        panswer.appendChild(alabel);
        panswer.appendChild(qanswer);
        var ddparent = document.getElementById(ddid).parentNode;
        var ddParSibling = ddparent.nextElementSibling.nextElementSibling;
        var ddpsPar = ddParSibling.parentNode;
        ddpsPar.insertBefore(panswer, ddParSibling);

        if (document.getElementById("id_removeAnswerBtn " + dropdownnum)) {
            var re = document.getElementById("id_removeAnswerBtn " + dropdownnum).parentNode;
            re.remove();
        }
    } else if (e.options[e.selectedIndex].text == "ESS" || e.options[e.selectedIndex].text == "") {
        if (document.getElementById("id_removeAnswerBtn " + dropdownnum)) {
            var re = document.getElementById("id_removeAnswerBtn " + dropdownnum).parentNode;
            re.remove();
        }
    }
}

//deletes a questions and updates all questions
function deleteElements(clicked_id) {
    event.preventDefault();
    var btnName = document.getElementById(clicked_id).id;
    var splitBtnName = btnName.split(" ");
    var num = splitBtnName[1];

    var deleteBtnContent = document.getElementById(clicked_id).innerHTML;
    var splitBtnName = deleteBtnContent.split(" ");
    var num2 = splitBtnName[2];
    var updateDeleteLabel = Number(num) + 1;

    for (var i = updateDeleteLabel; i < 100; i++) {
        if (document.getElementById("deleteBtn " + i)) {
            document.getElementById("deleteBtn " + i).innerHTML = 'Delete Question ' + num2;
            document.querySelector("label[for='id_Question " + i + "']").innerHTML = "Question " + num2 + ":";
            num2++;
        } else {
            continue;
        }
    }

    var qParent = document.getElementById("id_Question " + num).parentNode;
    qParent.remove();

    var acount = document.querySelectorAll("textarea[id*=id_Question" + num + "Answer]").length;

    for (var i = 1; i <= acount; i++) {
        if (document.getElementById("id_Question" + num + "Answer" + i)) {
            var aParent = document.getElementById("id_Question" + num + "Answer" + i).parentNode;
            aParent.remove();
        } else {
            break;
        }
    }

    var typeParent = document.getElementById("id_Question" + num + "type").parentNode;

    if (document.getElementById("id_removeAnswerBtn " + num)) {
        var arbtn = document.getElementById("id_removeAnswerBtn " + num).parentNode;
        var line = arbtn.nextElementSibling;
        line.remove();
        arbtn.remove();
    } else {
        var line = typeParent.nextElementSibling;
        line.remove();
    }
    typeParent.remove();
}

//deletes the last answer choice
function deleteLastAnswer(clicked_id) {
    event.preventDefault();
    var btnName = document.getElementById(clicked_id).id;
    var splitBtnName = btnName.split(" ");
    var num = splitBtnName[1];
    var aNum = Number(num);
    var count = document.querySelectorAll("textarea[id*=id_Question" + aNum + "Answer]").length;

    if (count > 0) {
        var lastqAnswer = document.querySelector("textarea[id*=id_Question" + aNum + "Answer" + count + "]");
        var aParent = lastqAnswer.parentNode;
        aParent.remove();
    }
    window.scrollBy(0, -118);
}

// adds new answer choice
function addLastAnswer(clicked_id) {
    event.preventDefault();
    var btnName = document.getElementById(clicked_id).id;
    var splitBtnName = btnName.split(" ");
    var num = splitBtnName[1];
    var aNum = Number(num);
    var count = document.querySelectorAll("textarea[id*=id_Question" + aNum + "Answer]").length;
    var e = document.getElementById("id_Question" + aNum + "type");

    if (e.options[e.selectedIndex].text == "MC") {
        var panswer = document.createElement("p");
        var alabel = document.createElement("label");
        alabel.setAttribute("for", "id_Question" + aNum + "Answer" + (count + 1));
        var t = document.createTextNode("Answer " + (count + 1) + ":");
        alabel.appendChild(t);

        var qanswer = document.createElement("textarea");
        qanswer.setAttribute("id", "id_Question" + aNum + "Answer" + (count + 1));
        qanswer.setAttribute("onchange","updateMAcheckbox(this.id)");

        var radio = document.createElement('input');
        radio.type = "radio";
        radio.name = "Question" + aNum + "RadioGrp";
        radio.value = "radio";
        radio.id = "id_EQuestion" + aNum + "Radio" + (count + 1);

        panswer.appendChild(alabel);
        var aBtnparent = document.getElementById(clicked_id).parentNode;

        panswer.appendChild(radio);
        panswer.appendChild(qanswer);
        aBtnparent.parentNode.insertBefore(panswer, aBtnparent);
    } else if (e.options[e.selectedIndex].text == "MA") {
        var panswer = document.createElement("p");
        var alabel = document.createElement("label");
        alabel.setAttribute("for", "id_Question" + aNum + "Answer" + (count + 1));
        var t = document.createTextNode("Answer " + (count + 1) + ":");
        alabel.appendChild(t);

        var qanswer = document.createElement("textarea");
        qanswer.setAttribute("id", "id_Question" + aNum + "Answer" + (count + 1));

        var checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.name = "Question" + aNum + "CheckboxGrp"
        checkbox.value = "value";
        checkbox.id = "id_EQuestion" + aNum + "Checkbox" + (count + 1);
        panswer.appendChild(alabel);

        var aBtnparent = document.getElementById(clicked_id).parentNode;

        panswer.appendChild(checkbox);
        panswer.appendChild(qanswer);
        aBtnparent.parentNode.insertBefore(panswer, aBtnparent);
    }
    window.scrollBy(0, 118);
}

    window.onload = quizEditPageLoad;