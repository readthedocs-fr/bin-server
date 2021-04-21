const deleteButton = document.getElementById('delete-button');
const token = new URLSearchParams(location.search).get('token');

if (token) {
  deleteButton.removeAttribute('hidden');
  deleteButton.addEventListener('click', async () => {
    try {
      const response = await fetch(window.location.pathname, {
        method: 'DELETE',
        headers: {
          Authorization: `Token ${token}`,
        },
      });

      if (!response.ok) {
        const error = new Error(`${response.status} ${response.statusText}\n${await response.text()}`);
        error.response = response;
        throw error;
      }

      location.href = '/';
    } catch (error) {
      console.error(error);
      if (error.response.status === 401) {
        alert("Le token que vous avez fourni est très probablement erroné.");
      } else {
        console.error("Nous vous recommandons d'ouvrir une issue sur https://github.com/readthedocs-fr/bin-server si le problème persiste.");
        alert(`Une erreur est survenue (${error.response?.statusText || error.message}), votre snippet n'a donc pas pu être supprimé. Regardez la console pour plus d'informations.`);
      }
    }
  });
}
