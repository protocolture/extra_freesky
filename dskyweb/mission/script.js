$(document).ready(function() {
    let currentSelection = 1;
    const totalSelections = 4;

    $(".container").addClass("hidden");

    $("#acceptMission").click(function() {
        $("#missionText").addClass("hidden");
        $("#selection1").removeClass("hidden");
    });

    $(".square").click(function() {
        const selectedChoice = $(this).data("choice");
        $("#option" + currentSelection).text(selectedChoice);

        $(this).parent().addClass("hidden");

        currentSelection += 1;

        if (currentSelection <= totalSelections) {
            $("#selection" + currentSelection).removeClass("hidden");
        } else {
            $(".selected-option").removeClass("hidden");
            $("#teamSelection").removeClass("hidden");
        }
    });

    $(".char").click(function() {
        const characterName = $(this).find("h2").text();
        $.get(`http://192.168.20.71/char${characterName.replace('Char ', '')}`, function(data) {
            console.log(`Character ${characterName} was selected.`);
        });
    });
});
