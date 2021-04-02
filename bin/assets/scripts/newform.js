const form = document.forms['post-snippet'];
const lang = form.lang;
const langs = [...lang.options].slice(1).flatMap((option) => [option.value, option.textContent.toLowerCase()]);
const code = form.code;

const langAliases = {
  txt: langs.indexOf('txt'),
  svg: langs.indexOf('xml'),
  jsonc: langs.indexOf('js'),
  get jsx() {
    return this.jsonc;
  },
  tsx: langs.indexOf('ts'),
  vue: langs.indexOf('html'),
}

// remove the "required" error message that overflows the page
code.addEventListener('invalid', (event) => event.preventDefault());
code.addEventListener('keydown', (event) => {
  if (event.code === 'Tab') {
    // prevents tab from being used to navigate between browser elements
    event.preventDefault();
    const { value, selectionStart, selectionEnd } = code;

    // inserts tab at the position of the caret
    code.value = value.slice(0, selectionStart) + '\t' + value.slice(selectionEnd);

    // puts caret after the newly inserted tab char
    const caretPos = selectionStart + 1;
    code.focus();
    code.setSelectionRange(caretPos, caretPos);
  } else if (event.code === 'KeyS' && (event.ctrlKey || event.metaKey) && form.checkValidity()) {
    // ctrl+s triggers form submission
    event.preventDefault();
    form.submit();
  }
});

window.addEventListener('drop', async (event) => {
  const files = event.dataTransfer.files;
  if (files.length !== 1) {
    return;
  }

  event.preventDefault();
  const file = files[0];
  const fileExtension = file.name.split('.').pop()?.toLowerCase() ?? '';

  const langIndex = langAliases[fileExtension] ?? langs.indexOf(fileExtension);
  if (langIndex === -1 && !confirm("Ce fichier n'est pas dans la liste des langages, voulez-vous quand même le charger ?")) {
    return;
  }

  try {
    code.value = await file.text();
    lang.selectedIndex = Math.ceil((langIndex === -1 ? langAliases.txt : langIndex) / 2) + 1;
  } catch (error) {} // the "file" is a directory (do nothing)
});
