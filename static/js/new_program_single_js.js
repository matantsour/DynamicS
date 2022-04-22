function getFirstElementByName(element_name) {
    var elements = document.getElementsByName(element_name);
    if (elements.length) {
        return elements[0];
    } else {
        return undefined;
    }
}

function deleteRow_update_old_rows(rownumber, number_of_phases) {
    rownumber = parseInt(rownumber, 10); //the current row number
    num_of_phases_int = parseInt(number_of_phases, 10);
    new_num_of_phases = (parseInt(number_of_phases, 10) - 1).toString()
    for (let i = 0; i < rownumber; i++) {
        i = i.toString();
        console.log(i);
        //update tr
        //no need
        //update input
        el = getFirstElementByName("o" + i);
        el.setAttribute("onchange", "single_creation_update_phases(" + new_num_of_phases + ");");

        //update label parameters
        ///"add" label
        el = getFirstElementByName("add_o" + i);
        el.setAttribute("onclick", "addRow(" + i.toString() + "," + new_num_of_phases + ")");
        ///"delete" label
        el = getFirstElementByName("delete_o" + i);
        el.setAttribute("onclick", "deleteRow(" + i.toString() + "," + new_num_of_phases + ")");


    }

    for (let i = (rownumber + 1); i < num_of_phases_int; i++) {

        i = i.toString();
        console.log(i);
        new_number_of_row = parseInt(i, 10) - 1
            //update tr
        el = document.getElementById(i);
        el.setAttribute("id", new_number_of_row);
        //update input
        el = getFirstElementByName("o" + i);
        el.setAttribute("name", "o" + new_number_of_row);
        el.setAttribute("onchange", "single_creation_update_phases(" + new_num_of_phases + ");");

        //update label parameters
        ///"add" label
        el = getFirstElementByName("add_o" + i);
        el.setAttribute("name", "add_o" + new_number_of_row);
        el.setAttribute("onclick", "addRow(" + new_number_of_row + "," + new_num_of_phases + ")");
        ///"delete" label
        el = getFirstElementByName("delete_o" + i);
        el.setAttribute("name", "delete_o" + new_number_of_row);
        el.setAttribute("onclick", "deleteRow(" + new_number_of_row + "," + new_num_of_phases + ")");


    }



}

function deleteRow(rownumber, number_of_phases) {
    if (parseInt(number_of_phases, 10) <= 2) {
        return;
    }

    var table = document.getElementById("phasesEditTable");
    //update old rows
    deleteRow_update_old_rows(rownumber, number_of_phases);
    //delete the current row
    var r = parseInt(rownumber, 10);
    var row = table.deleteRow(r);
    new_number_of_phases = parseInt(number_of_phases, 10) - 1;
    single_creation_update_phases(new_number_of_phases);

}


function addRow_update_old_rows(rownumber, num_of_phases) {
    rownumber = parseInt(rownumber, 10); //the current row number
    num_of_phases_int = parseInt(num_of_phases, 10);
    new_num_of_phases = (parseInt(num_of_phases, 10) + 1).toString()
    for (let i = 0; i <= rownumber; i++) {
        i = i.toString();
        console.log(i);
        //update tr
        //no need
        //update input
        el = getFirstElementByName("o" + i);
        el.setAttribute("onchange", "single_creation_update_phases(" + new_num_of_phases + ");");

        //update label parameters
        ///"add" label
        el = getFirstElementByName("add_o" + i);
        el.setAttribute("onclick", "addRow(" + i.toString() + "," + new_num_of_phases + ")");
        ///"delete" label
        el = getFirstElementByName("delete_o" + i);
        el.setAttribute("onclick", "deleteRow(" + i.toString() + "," + new_num_of_phases + ")");


    }

    for (let i = num_of_phases - 1; i > (rownumber); i--) {

        i = i.toString();
        console.log(i);
        new_number_of_row = parseInt(i, 10) + 1
            //update tr
        el = document.getElementById(i);
        el.setAttribute("id", new_number_of_row);
        //update input
        el = getFirstElementByName("o" + i);
        el.setAttribute("name", "o" + new_number_of_row);
        el.setAttribute("onchange", "single_creation_update_phases(" + new_num_of_phases + ");");

        //update label parameters
        ///"add" label
        el = getFirstElementByName("add_o" + i);
        el.setAttribute("name", "add_o" + new_number_of_row);
        el.setAttribute("onclick", "addRow(" + new_number_of_row + "," + new_num_of_phases + ")");
        ///"delete" label
        el = getFirstElementByName("delete_o" + i);
        el.setAttribute("name", "delete_o" + new_number_of_row);
        el.setAttribute("onclick", "deleteRow(" + new_number_of_row + "," + new_num_of_phases + ")");


    }

}


function addRow(rownumber, number_of_phases) {
    if (parseInt(number_of_phases, 10) >= 8) {
        return;
    }
    var table = document.getElementById("phasesEditTable");
    //update old rows
    addRow_update_old_rows(rownumber, number_of_phases)
        //add the new row
    var r = parseInt(rownumber, 10) + 1
    var row = table.insertRow(r);
    var newrownumber = r;
    newrownumber = newrownumber.toString();
    row.id = newrownumber;
    number_of_phases = number_of_phases + 1
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    new_input_tag = "<input name='o" + newrownumber + "'" + "type='text' onchange='single_creation_update_phases(" + number_of_phases + ")'>";
    cell1.innerHTML = new_input_tag;
    new_add_label_tag = "<label class='newphaseTableOptionsLabel' name='add_o" + newrownumber + "' onclick='addRow(" + newrownumber + "," + number_of_phases + ")'>הוסף</label>"
    cell2.innerHTML = new_add_label_tag;
    new_delete_label_tag = "<label class='newphaseTableOptionsLabel' name='delete_o" + newrownumber + "' onclick='deleteRow(" + newrownumber + "," + number_of_phases + ")'>מחק</label>"
    cell3.innerHTML = new_delete_label_tag;

}



function single_creation_update_phases(number_of_phases) {
    var txt = "";
    for (let i = 0; i < number_of_phases; i++) {
        fieldName = "o" + i.toString();
        fieldVal = document.forms["form"][fieldName].value;
        if (fieldVal != null && fieldVal != "") {
            if (i != number_of_phases)
                txt += "'" + fieldName + "'" + ":" + "'" + fieldVal + "'" + ",";
            else
                txt += "'" + fieldName + "'" + ":" + "'" + fieldVal + "'";
        }
    }
    document.forms["form"]["phases_names"].value = txt;
}

function TheCreatorWasChosen() {
    var choice = document.getElementById("myInput").value;
    document.getElementById("myInput").value = "-";
    var presented_choice = choice.substr(0, choice.indexOf('|'));
    document.getElementById("id_creator_choice").value = choice;
    document.getElementById("id_creator_choice_presented").innerHTML = presented_choice;
}

function TheCreationNameWasChosen() {
    var choice = document.getElementById("insert_creation_name_field").value;
    document.getElementById("id_creation_name").value = choice;

}


function checkForm(number_of_phases) {
    single_creation_update_phases(number_of_phases)
    var a = document.getElementById("id_phases_names").value;
    var b = document.getElementById("id_creator_choice").value;
    var c = document.getElementById("id_creation_name").value;
    if (a == null || a == "" || b == null || b == "" || c == null || c == "") {
        alert("יש למלא שם יוצר, שם יצירה ושלבים");
        return false;
    }
}