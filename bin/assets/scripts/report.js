const promptMessage = `\
Vous allez signaler ce snippet auprès de l'administrateur.
Tout abus peut mener à la coupure du service.

Veuillez entrer votre nom ou votre adresse email :`;

const reportForm = document.forms.report;
reportForm.addEventListener('submit', (event) => {
  const name = prompt(promptMessage)?.trim();

  if (!name?.length) {
    event.preventDefault();
    return;
  }

  reportForm.name.value = name;
});
