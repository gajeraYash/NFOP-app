var x = document.getElementsByClassName("alert");

setTimeout(function(){ 
    try {
        for (i = 0; i < 2; i++) {
            x[i].style.display = "none"; 
        }
    }
    catch(err) {
        console.log("Edit Member","Cleared");
    }
}, 5000);

$(function() {
    $('#id_phone_number').mask('(000) 000-0000');
});

