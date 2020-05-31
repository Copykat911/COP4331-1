function searchModal() {
    // Get the modal
    var modal = document.getElementById("mySearchModal");
    // Get the button that opens the modal
    var btn = document.getElementById("mySearchBtn");
    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];
    // When the user clicks the button, open the modal 
    btn.onclick = function() {
            modal.style.display = "block";
        }
        // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
            modal.style.display = "none";
        }
        // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if(event.target == modal) {
            modal.style.display = "none";
        }
    }
}
function searchContact() {
    var input, filter, listfname, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    chip = document.getElementsByName("chip");
    listfname = chip.getElementsByClassName("listfname")
    for(i = 0; i < listfname.length; i++) {

        txtValue = listfname[i].textContent
        if(txtValue.toUpperCase().indexOf(filter) > -1) {
            chip[i].style.display = "";
        } else {
            chip[i].style.display = "none";
        }
    }
}

