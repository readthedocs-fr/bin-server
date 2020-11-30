const code = document.getElementsByName("code")[0];
const button = document.querySelector(".post-snippet button");
const svg = button.querySelector("svg");

button.addEventListener("click", (event) => {
  if (!code.value) {
    event.preventDefault();
  }
});

code.addEventListener("input", () => {
  if (code.value) {
    button.classList.add("valid");
    svg.classList.add("valid");
    return;
  }

  button.classList.remove("valid");
  svg.classList.remove("valid");
});
