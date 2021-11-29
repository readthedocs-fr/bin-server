const langSelection = document.getElementById('lang-selection');

langSelection.addEventListener('change', (event) => {
  location.href = location.href.replace(/(\.\w+)?$/, '.' + event.target.value);
});
