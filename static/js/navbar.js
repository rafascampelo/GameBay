document.addEventListener("DOMContentLoaded", () => {
  const menuBtn = document.getElementById("menu-btn");
  const sideMenu = document.getElementById("side-menu");
  const closeBtn = document.getElementById("close-btn");

  menuBtn.addEventListener("click", () => {
    sideMenu.classList.remove("right-[-100%]", "sm:right-[-250px]");
    sideMenu.classList.add("right-0");
  });

  closeBtn.addEventListener("click", () => {
    sideMenu.classList.remove("right-0");
    sideMenu.classList.add("right-[-100%]", "sm:right-[-250px]");
  });
});
