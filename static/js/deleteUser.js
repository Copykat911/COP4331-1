// list[i].setAttribute("id", "butj" + i);s
function deleteUser() {

    var list = document.getElementsByClassName("dangerb");
    for (var i = 0; i < list.length; i++) 
    {
 
     if(list[i].hasAttribute("style","display: none"))
     {
     list[i].setAttribute("style", "display: inline");
     }
     else
     {
      list[i].setAttribute("style", "display: none");
     }
    }
}
function closedeleteUser() {

  var list = document.getElementsByClassName("dangerb");
  for (var i = 0; i < list.length; i++) 
  {
 
   list[i].setAttribute("style", "display:none");
  }
}

function editUser() {

  var list = document.getElementsByClassName("dangerc");
  for (var i = 0; i < list.length; i++) 
  {
    list[i].setAttribute("id", "butk" + i);
   list[i].setAttribute("style", "display:inline");
  }
}
// function deleteUser() {
//   var x = document.getElementsByClassName("TB");
//   console.log(x)
//   if (x.style === "display:none") {
//     x.style =  "display:inline"
//   } else {
//     x.style = "display:none";
//   }
//   console.log(x)
// } 
