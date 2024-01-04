function toggleMenu(){
    document.getElementById('nav').classList.toggle('visible')
}

document.getElementById("hamburger")
    .addEventListener("click", toggleMenu)
document.getElementById("nav")
    .addEventListener("click", toggleMenu)


$(function () {
        $("#datepicker").datepicker({
            dateFormat: "dd-mm-yy", // Formát data (změňte podle potřeby)
            onSelect: function (dateText) {
                $("#datum").val(dateText); // Uloží vybrané datum do skrytého pole s id 'datum'
            }
        });
        $("#datepicker").datepicker("show");
    });