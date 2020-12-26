const form = document.forms[0];
const code = form.code;
const button = form.getElementsByTagName('button')[0];

button.addEventListener('click', (event) => {
  if (!code.value) {
    event.preventDefault();
  }
});

code.addEventListener('input', () => {
  if (code.value) {
    button.classList.add('valid');
    return;
  }
  button.classList.remove('valid');
});

window.addEventListener('keydown', (event) => {
  if (event.code === 'Tab') {
    // prevents tab from being used to navigate between browser elements
    event.preventDefault();

    const pos = code.selectionStart;
    const content = code.value;

    // inserts tab at the position of the caret
    code.value = content.substring(0, pos) + '\t' + content.substring(pos);

    // puts caret after the newly inserted tab char
    const caretPos = pos + 1;
    code.focus();
    code.setSelectionRange(caretPos, caretPos);
  }
});
