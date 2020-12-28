const locs = [...document.getElementsByClassName('line-number')];
const selectedLocs = document.getElementsByClassName('selected');

handleHash();
window.addEventListener('hashchange', () => {
  [...selectedLocs].forEach((e) => e.classList.remove('selected'));
  handleHash();
})

locs.forEach((loc, i) => {
  loc.addEventListener('click', () => {
    // add the line location to the URL without affecting the history and without triggering a hashchange
    window.history.replaceState(undefined, undefined, `#L${i + 1}`);
    // remove all selected lines
    [...selectedLocs].forEach((e) => e.classList.remove('selected'));
    loc.nextElementSibling.classList.add('selected');
  })
})

function handleHash() {
  const hashMatch = location.hash.match(/^(?:#L(\d+)(?:-L(\d+))?)$/i);
  if (!hashMatch) {
    return;
  }
  let start = parseInt(hashMatch[1], 10);
  let end = hashMatch[2] ? parseInt(hashMatch[2], 10) : undefined;
  if (end && start > end) {
    [start, end] = [end, start];
  }
  if (start <= 0 || start > locs.length || end && end <= 0 || end > locs.length) {
    return;
  }
  if (!end) {
    locs[start - 1].nextElementSibling.classList.add('selected');
    return;
  }
  for (let i = start - 1; i <= locs.length && i < end; i++) {
    const line = locs[i].nextElementSibling;
    line.classList.add('selected');
    if (i === start - 1) {
      // scroll to the first line of the selection
      line.scrollIntoView();
    }
  }
}
