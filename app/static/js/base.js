var elm = document.getElementById('close-err');

function close(){
  document.getElementsByClassName('notifcation')[0].style.opacity = "0";
}

elm.addEventListener("click", () => {
  close();
});

setTimeout(close, 5000);
