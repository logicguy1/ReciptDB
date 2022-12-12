/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function open_dropdown() {
  console.log("Clicked")
  document.getElementById("dropdown").className = "show";
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.add_img')) {
    document.getElementById("dropdown").className = "";
  }
} 
