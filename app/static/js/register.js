const pwd = document.getElementById("password");

pwd.addEventListener("input", () => {
  const pwdVal = pwd.value;
  let result = zxcvbn(pwdVal);

  if (pwdVal != ""){
    document.getElementById("level-0").style.background = "red";
  } else {
    document.getElementById("level-0").style.background = "";
  }

  if (result.score >= 1){
    document.getElementById("level-1").style.background = "orangered";
  } else {
    document.getElementById("level-1").style.background = "";
  }

  if (result.score >= 2){
    document.getElementById("level-2").style.background = "orange";
  } else {
    document.getElementById("level-2").style.background = "";
  }

  if (result.score >= 3){
    document.getElementById("level-3").style.background = "yellowgreen";
  } else {
    document.getElementById("level-3").style.background = "";
  }

  if (result.score >= 4){
    document.getElementById("level-4").style.background = "green";
  } else {
    document.getElementById("level-4").style.background = "";
  }
});

