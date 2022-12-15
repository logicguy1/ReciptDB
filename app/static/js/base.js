var elm = document.getElementById('close-err');

function close(){
  document.getElementsByClassName('notifcation')[0].style.opacity = "0";
}

if (elm){
  elm.addEventListener("click", () => {
    close();
  });
  setTimeout(close, 5000);
}


function open_popup(){
  document.getElementById('popup-form').style.display = "block";
}

function close_popup(){
  document.getElementById('popup-form').style.display = "none";
}
