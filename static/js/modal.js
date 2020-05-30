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
    var input, filter, tbody, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    tbody = document.getElementById("myBody");
    tr = tbody.getElementsByTagName("tr");
    for(i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        txtValue = td.textContent || td.innerText;
        if(txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}