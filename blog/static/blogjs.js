function toggle() {
  let menu = document.getElementById("topnav");
  if (menu.className === "navbar") {
    menu.className += " responsive";
  }
  else {
    menu.className = "navbar";
  }

}

function displaySearchBar() {
  let searchBar = document.getElementById("search__form");
  if (searchBar.style.display === "none") {
    searchBar.style.display = "block";
  } else {
    searchBar.style.display = "none";
  }

}

let button = document.getElementById("search__button");
button.addEventListener("click", displaySearchBar);
