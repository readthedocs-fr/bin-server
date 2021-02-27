const locs = [...document.getElementsByClassName('line-number')];
const selectedLocs = document.getElementsByClassName('selected');

handleHash();

window.addEventListener('hashchange', () => {
  clearSelections();
  handleHash();
})

locs.forEach((loc, i) => {
  loc.addEventListener('click', () => {
    // add the line location to the URL without affecting the history and without triggering a hashchange
    window.history.replaceState(undefined, undefined, `#L${i + 1}`);
    clearSelections();
    loc.nextElementSibling.classList.add('selected');
  })
})

function clearSelections() {
  [...selectedLocs].forEach((element) => element.classList.remove('selected'));
}

function handleHash() {
  const hashMatch = location.hash.match(/^#L(\d+)(?:-L(\d+))?$/i);
  if (!hashMatch) {
    return;
  }

  let start = +hashMatch[1];
  let end = hashMatch[2] ? +hashMatch[2] : undefined;
  if (end && start > end) {
    [start, end] = [end, start];
  }
  if (start <= 0 || start > locs.length || end && (end <= 0 || end > locs.length)) {
    return;
  }

  locs[start - 1].nextElementSibling.classList.add('selected');

  if (!end || start === end) {
    return;
  }

  // scroll to the first line of the selection
  locs[start - 1].nextElementSibling.scrollIntoView();
  for (let i = start; i < end; i++) {
    locs[i].nextElementSibling.classList.add('selected');
  }
}
