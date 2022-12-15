document.onclick = hideMenu;
document.oncontextmenu = rightClick;

var elm = null;

function hideMenu() {
  document.getElementById("contextMenu").style.display = "none";
  elm = null;
}

function rightClick(e) {
  console.log(e.target);

  if (e.target.nodeName != "TD"){
    hideMenu();
    return;
  } 
  e.preventDefault();

  if (document.getElementById("contextMenu").style.display == "block"){
    hideMenu();
  } else {
    elm = e.target;
    var elm_parent = elm.parentNode;
    var menu = document.getElementById("contextMenu");

    // Check if there it is actiaved or not
    var state = elm_parent.children[1].children[0].innerHTML.includes("Deaktiveret");
    if (state){
      menu.children[0].children[1].style.display = "none";
      menu.children[0].children[0].style.display = "block";
    } else {
      menu.children[0].children[0].style.display = "none";
      menu.children[0].children[1].style.display = "block";
    }

    // Check if there is a user assigend
    var state = elm_parent.children[2].innerHTML == "";
    if (state){
      menu.children[0].children[2].style.display = "none";
    } else {
      menu.children[0].children[2].style.display = "block";
    }

    console.log(state)

    menu.style.display = 'block';
    menu.style.left = e.pageX + "px";
    menu.style.top = e.pageY + "px";
  }
}

function toggle(state){
  var elm_parent = elm.parentNode;
  var code = elm_parent.children[0].innerHTML;

  document.getElementById("code").value = code;

  var check = document.getElementById('activate');
  if (state != check.checked) {
    check.click();
  }
  document.getElementById('submit-auto').click();
}

function change_pass(){
  var elm_parent = elm.parentNode;
  var code = elm_parent.children[0].innerHTML;
  document.getElementById("acc").value = code;
}

function delete_row(){
  var elm_parent = elm.parentNode;
  var code = elm_parent.children[0].innerHTML;

  document.getElementById("code_del").value = code;
  document.getElementById('submit-auto2').click();
}
