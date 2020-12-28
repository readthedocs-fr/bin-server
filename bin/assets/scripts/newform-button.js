const code = document.forms[0].code;

// remove the "required" error message that overflows the page
code.addEventListener('invalid', (event) => event.preventDefault());
code.addEventListener('keydown', (event) => {
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
