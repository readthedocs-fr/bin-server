# bin

Un outil pour héberger des snippets de code et les partager via une URL.

## Installer

Pour installer *bin* à des fins d'**hébergement**, rendez vous sur la page des
releases et télécharger la dernière version stable au format `.whl`. Il s'agit
d'une archive *wheel* multi-plateforme pouvant être directement installée sur
votre système. Les dépendances de l'archive seront installées automatiquement à
l'exception de `metrics` qui doit être installée indépendamment.

Note, les utilisateurs sur Windows doivent remplacer `python3` par `py`.

    python3 -m pip install -i https://pypi.drlazor.be bin


Assurez-vous que le service est correctement installé en affichant la page
d'aide :

    python3 -m bin --help

La configuration de l'application se fait soit via un fichier *dot-env* soit
directement via les variables d'environnement. Le format du fichier doit être
comme suit: `NOM=valeur`, un nom par ligne, les lignes vides et les lignes
commençant par un dièse (#) sont ignorées.

La configuration par défaut de bin est :

    RTDBIN_HOST=localhost
    RTDBIN_PORT=8012
    RTDBIN_MAXSIZE=16kiB
    RTDBIN_DEFAULT_LANGUAGE=text
    RTDBIN_DEFAULT_MAXUSAGE=0
    RTDBIN_DEFAULT_LIFETIME=0
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_DB=0

Vous pouvez changer cette configuration par défaut en créant votre propre
fichier de configuration et en renseignant son chemin via l'option en ligne de
commande `--rtdbin-config` :

    python3 -m bin --rtdbin-config /chemin/vers/.env

## Contribuer

Pour installer *bin* à des fins de **développement**, téléchargez la dernière
branche `main` du repository github et installez le projet dans un
environnement virtuel dédié :

    git clone https://github.com/readthedocs-fr/bin.git bin
    cd bin
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
    venv/bin/pip install -e .

Assurez-vous que le service est correctement installé et est fonctionnel en
lançant les tests unitaires :

    venv/bin/python -m unittest

Lancer l'application de développement :

    venv/bin/python -m bin

Toutes les contributions doivent être faites sur une nouvelle branche (basée
sur la dernière `main`). Si vous n'avez pas les droits d'accès au repo officiel
assurez vous de pousser votre branche sur un fork.

    git checkout -b votrebranche
    git remote add fork https://github.com/<votrecompte>/bin
    git push fork $(git branch --show-current)

Chacun de vos ajouts doit être accompagné d'un message de commit exhaustif,
nous recommandons de prendre du temps à leur rédaction vu qu'il s'agit là de la
principale source de documentation technique. En ce sens, nous privilégions la
rédaction des messages de commit au format suivant:

    type: titre sur 50 caractères max

    Un paragraphe établissant le contexte de votre contribution, pour un
    correctif de bug donner les étapes pour reproduire le bug. Il s'agit
    ici d'expliquer POURQUOI votre contribution est un ajout utile.

    Un ou plusieurs paragraphes expliquant votre solution, les différentes
    pistes envisagées et les différentes décisions. Il s'agit ici d'expliquer
    COMMENT vous avez résolu les objectifs/problèmes établis dans le 1er
    paragraphe.

Les différents `types`:

* `imp`, improvement, amélioration d'une fonctionnalité existante
* `ref`, refactor, ré-implémentation conséquente d'une fonctionnalité
* `add`, add, ajout d'une nouvelle fonctionnalité
* `doc`, documentation, ajout/correction relatif à la documentation
* `fix`, fix, correctif de bug
