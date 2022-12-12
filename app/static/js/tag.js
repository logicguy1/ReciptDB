const inp = document.getElementById("color-inp");
const elm = document.getElementById("color-inp-wrapper").getElementsByClassName("exam-color")[0];

inp.addEventListener("input", () => {
  var val = inp.value;

  for (let i = 0; i < val.length; i++){
    if (!"0123456789ABCDEF".includes(val[i].toUpperCase())){
      val = "303030";
    }
  }

  if (val.length != 6){
    val = "303030";
  }

  elm.style = `background-color: #${val}40; border: 1.5px solid #${val}70;`;
});

