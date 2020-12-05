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

function setCaretPos(pos) {
  code.focus();
  code.setSelectionRange(pos, pos);
}

window.addEventListener("keydown", (event) => {
  if (event.code === "Tab") {
    // prevents tab from being used to navigate between browser elements
    event.preventDefault();

    const pos = code.selectionStart;
    const content = code.value;

    // inserts tab at the position of the caret
    code.value = content.substring(0, pos) + '\t' + content.substring(pos);

    // puts caret after the newly inserted tab char
    setCaretPos(pos + 1);
  }
});
