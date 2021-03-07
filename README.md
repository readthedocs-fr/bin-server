[![PyPI](https://img.shields.io/pypi/v/rtd-bin-server)](https://pypi.org/project/rtd-bin-server)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/readthedocs-fr/bin-server/Continuous%20Integration?logo=github)](https://github.com/readthedocs-fr/bin-server/actions)
[![Discord](https://img.shields.io/discord/238975753969074177?logo=discord)](https://discord.gg/PB9PekTNsg)
[![Documentation](https://img.shields.io/readthedocs/rtd-bin-server?logo=Read%20the%20Docs)](https://rtd-bin-server.readthedocs.io/en/latest/)
[![License](https://img.shields.io/github/license/readthedocs-fr/bin-server)](https://github.com/readthedocs-fr/bin-server/blob/main/LICENSE)

# bin-server

Un outil pour héberger des snippets de code et les partager via une URL.

## Installation

Le service nécessite une version de Python supérieure ou égale à Python 3.7 et un accès à un serveur Redis. Les archives sont hébergés sur [Pypi](https://pypi.org/project/rtd-bin-server/), vous pouvez installer la dernière version stable via `pip` :

	$ pip install rtd-bin-server

Une fois installé, le module `bin` devient accessible et peut être directement lancé via la ligne de commande.

	$ python -m bin

Par défaut, le service ne traite qu'un client à la fois, écoute à l'adresse `localhost:8012` et se connecte à la base de donnée Redis sur `localhost:6379/0`. Changer la configuration par défaut se fait au moyen d'un fichier `dotenv`. Le fichier sera automatiquement détecté s'il est nommé `.env` et qu'il se trouve soit au niveau des sources, soit au niveau du répertoire courant (celui depuis lequel est lancé la commande). Une alternative est de renseigner le fichier de configuration à utiliser via l'option `--rtdbin-config`.

	$ python -m bin --rtdbin-config /chemin/vers/fichier/.env

La configuration complète par défaut est reprise ci-dessous :

    RTDBIN_HOST=localhost
    RTDBIN_PORT=8012
    RTDBIN_MAXSIZE=16kiB
    RTDBIN_DEFAULT_LANGUAGE=text
    RTDBIN_DEFAULT_MAXUSAGE=0
    RTDBIN_DEFAULT_LIFETIME=0
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_DB=0

Par défaut, le service utilise le serveur web `wsgiref` disponible dans la bibliothèque standard de Python pour traiter les requêtes. Ce serveur est propice dans un environnement de développement ou lorsque le volume d'utilisateur est réduit. Pour de meilleures performances, [un serveur tiers compatible wsgi](https://wsgi.readthedocs.io/en/latest/servers.html) peut être utilisé à la place.

	$ pip install gunicorn
	$ gunicorn bin:app

Des fichiers de configuration d'exemples pour `nginx`, `systemd` et `gunicorn` sont disponibles dans le [wiki](https://github.com/readthedocs-fr/bin/wiki/systemd-nginx-gunicorn).

## Contribution

Le développement de `bin` se fait principalement via la communauté Discord **Read The Docs** dans le canal [#bin](https://discord.gg/FECbXpmj7m).

Les sources peuvent être récupérées via Git et le service peut être installé dans un environnement virtuel dédié.

	$ git clone https://github.com/readthedocs-fr/bin.git rtdbin
	$ cd rtdbin
	$ python -m venv
	$ venv/bin/pip install -r requirements.txt
	$ venv/bin/pip install -e .

Une fois installé, vous pouvez vous assurer que le système est correctement opérationnel en lançant la suite de tests unitaires et en vérifiant que le serveur démarre correctement.

	$ venv/bin/python -m unittest
	$ venv/bin/python -m bin &
	$ curl http://localhost:8012/health
	$ kill %%

Les contributions se font sur des branches dédiées, les branches sont nommées en commençant par quelques mots-clés suivis d'un identifiant de l'utilisateur. Les commits sont le plus petit dénominateur de version, sont correctement documentés au moyen d'un message de commit reprenant au minimum un contexte expliquant la nécessité des modifications.

	$ git checkout main
	$ git pull origin main
	$ git checkout -b redo-readme-juc
	$ git commit <<EOF
	doc: redo readme
	
	The readme is the first document users read when they learn
	about the project, the file is by default shown in the project root
	page in github.
	
	The document is very important yet the current one is not very
	good. The new documents are more straight to the point.
	EOF
	$ git push fork redo-readme-juc
