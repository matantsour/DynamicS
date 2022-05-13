function ThePhaseWasChosen() {
    var choice = document.getElementById("myInput").value;
    document.getElementById("myInput").value = "-";
    document.getElementById("id_creator_creation_phase").value = choice;
    document.getElementById("id_creator_creation_phase_presented").innerHTML = choice;
}
