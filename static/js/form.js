function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function openAddForm() {
  document.getElementById("myAddForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}

function closeAddForm() {
  document.getElementById("myAddForm").style.display = "none";
}


function searchContact() {
  var input, filter, tbody, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  tbody = document.getElementById("mytbl");
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

function logout() {
  window.location.href = '/logout';
}

function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}