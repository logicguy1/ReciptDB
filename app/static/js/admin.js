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

function get_sysinf(){
  fetch('/api/get_stats')
  .then(response => response.json())
  .then((data) => {
    console.log(data);

    // Configure system info
    var sysinf = data.sysinf;
    document.getElementById("process-cpu").style.width = `${sysinf.cpu.cpu_usage}%`;
    document.getElementById("proc-cpu").innerHTML = `${sysinf.cpu.cpu_usage}%`;

    elm = document.getElementById("used-cpu")
    elm.innerHTML = ""
    for (let i = 0; i < sysinf.cpu.top.length; i++){
      elm.innerHTML += sysinf.cpu.top[i] + "<br>"
    }

    document.getElementById("process-mem").style.width = `${sysinf.memory.percent_used}%`;
    document.getElementById("proc-mem").innerHTML = `${sysinf.memory.percent_used}%`;
    document.getElementById("used-mem").innerHTML = `${sysinf.memory.used}GB`;
    document.getElementById("left-mem").innerHTML = `${sysinf.memory.total}GB`;

    document.getElementById("process-hdd").style.width = `${sysinf.disk_space.percent_used}%`;
    document.getElementById("proc-hdd").innerHTML = `${sysinf.disk_space.percent_used}%`;
    document.getElementById("used-hdd").innerHTML = `${sysinf.disk_space.used}GB`;
    document.getElementById("left-hdd").innerHTML = `${sysinf.disk_space.total}GB`;

    document.getElementById("os").innerHTML = sysinf.os;
    document.getElementById("uptime").innerHTML = sysinf.uptime;
    document.getElementById("host").innerHTML = sysinf.hostname;
    document.getElementById("ip").innerHTML = sysinf.ip;
    document.getElementById("mysql").innerHTML = sysinf.mysql;
    document.getElementById("nginx").innerHTML = sysinf.nginx;

  });

  // setTimeout(get_sysinf, 10000);
}

get_sysinf();
