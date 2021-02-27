const locs = [...document.getElementsByClassName('line-number')];
const selectedLocs = document.getElementsByClassName('selected');
const deleteButton = document.getElementById('delete-button');

const snippetId = location.pathname.match(/(\w+)\.\w+$/)[1];
const token = deleteButton.dataset.token || localStorage.getItem(`snippet-${snippetId}`);

handleHash();
if (token) {
  deleteButton.addEventListener('click', () => {
    fetch(window.location.pathname, {
      method: 'DELETE',
      headers: {
        Authorization: `Token ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(res.statusText);
        }

        localStorage.removeItem(`snippet-${snippetId}`);
        location.href = '/';
      })
      .catch((err) => {
        console.error(err);
        if (err.status !== 401) {
          console.error("Nous vous recommandons d'ouvrir une issue sur https://github.com/readthedocs-fr/bin-server si le problème persiste.");
        }
        alert(`Une erreur est survenue (${err.message}), votre snippet n'a donc pas pu être supprimé. Regardez la console pour plus d'informations.`);
      });
  });
} else {
  deleteButton.remove();
}

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
  [...selectedLocs].forEach((e) => e.classList.remove('selected'));
}

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
