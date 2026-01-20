# Digicheese

Digicheese est une application de fidélisation client d'une formagerie, permettant la gestion de colis de goodies à des clients.

## Introduction

L'application Digicheese est une application python totalement dockerisée.

Sa mise en place passe par trois fichiers clés:

- la **Dockerfile** qui défini notre container d'API et de tests.
- le **requirements.txt** qui liste les dépendences de notre application python.
- le **docker-compose.yml** qui orchestre les différents containers dont notre application à besoin.

Côté containerisation, nous aurons trois containers:

- **fastapi**: contenant les fichiers de notre API et de nos Tests.
- **mariadb**: contenant notre Base De Données.
- **adminer**: permettant d'accéder à notre Base De Données plus facilement.

## Technologies

Pour réaliser ce projet, nous nous sommes basés sur les technologies suivantes:

```bash
- FastApi # Api.
- Uvicorn # Serveur.
- SqlAlchemy # ORM.
- MariaDB # Base De Données.
- Pytest # Environnement de Tests.
- Faker # Création de fausses données.
- Docker # Service de Containerisation.
- Swagger # Interface Graphique autogénérée pour l'API.
- Adminer # Interface Graphique pour accéder à la Base de Données.
```

## Project Structure

```bash
.
├── api/                # Dossier du Code source de l'API FastAPI
│   ├── main.py         # Point d'entrée de notre API FastAPI
│   ├── database.py     # Fichier de connexion à la BDD.
│   ├── dbseed/         # Seed permettant de peupler la BDD.
│   ├── models/         # models SQLAlchemy permettant la création des Tables en BDD.
│   ├── repositories/   # Couche d'accès aux données
│   ├── services/       # Couche de logique métier
│   ├── routers/        # Définitions des routes de l'API
│   └── schemas/        # Schemas pydantic pour la validation des données
│
├── tests/              # Dossier de la suite des Tests
│   ├── __init__.py     # Prérequis pytest pour exécuter les tests
│   ├── conftest.py     # Configuration Pytest et fixtures
│   └── test_client.py  # Fichier de test, ici pour les routes client.
│
├── .gitignore          # Fichiers et Dossiers ignorés par Git
├── Dockerfile          # Dockerfile permettant de build l'API FastAPI
├── docker-compose.yml  # Configuration Docker Compose
├── requirements.txt    # Dépendences python
├── .env                # Variables d'Environnement
├── .env.example        # Exemple de variables d'environnement pour le fichier .env
└── README.md           # Documentation du Projet
```

## Prérequis

Le projet nécessite de pouvoir exécuter un environnement docker & docker desktop, le plus facile étant simplement d'installer Docker Desktop, voici un lien pour l'installer:

- **Docker Desktop**: [Guide d'Installation](https://www.docker.com/products/docker-desktop/)

## Pour Commencer

### 1. Cloner le répertoire du projet

#### Option 1: En HTTP

```bash
git clone https://github.com/Laynaria/projet2-groupe2-digicheese.git
cd Projet-FastAPI-Docker
```

#### Option 2: En SSH

```bash
git clone git@github.com:Laynaria/projet2-groupe2-digicheese.git
cd Projet-FastAPI-Docker
```

### 2. Configurer les Variables d'Dnvironnement

Copier le fichier `.env.example` à la racine, et nommez sa copie `.env`,
définissez ensuite les variables.

Attention à bien avoir les mêmes valeur pour les couples de variables suivantes :

- **USER** et **DB_USER**
- **PASSWORD** et **DB_PASSWORD**
- **DATABASE** et **DB_NAME**
- **PORT_DB_VISUALISATION** et **DB_PORT**

### 3. Pour Build et Lancer l'application

Pour build les images Docker et démarrer tous les services (FastAPI et MariaDB):

```bash
docker-compose up --build
```

Une fois les containers lancés, l'application est accessible sur:
**[http://localhost:8000](http://localhost:8000)**

La documentation auto-générée de l'API se trouve sur:

- Swagger UI: **[http://localhost:8000/docs](http://localhost:8000/docs)**
- ReDoc: **[http://localhost:8000/redoc](http://localhost:8000/redoc)**

### 4. Stopper l'Application

Pour stopper et supprimer tous les containers utilisez la commande suivante:

```bash
# -v flag removes the volumes
docker-compose down -v
```

## Gestion de la BDD

Pour intéragir avec le service MariaDB, notre Service de Gestion de Base de Données Relationelles, plusieurs options sont possible :

### Option 1 : Accès via Adminer

Adminer est un client léger permettant d'accéder à des Base de Données à partir d'un navigateur web.

Naviguez sur **[http://localhost:8070](http://localhost:8070)** et utilisez les identifiants suivant:

- **System**: MySQL/MariaDB
- **Server**: db
- **Username**: admin
- **Password**: Admin123!
- **Database**: digicheese

Attention, si vous avez modifiez les variables d'environnement dans votre fichier `.env`, n'oubliez pas d'utilisez les valeurs que vous avez choisies à la place.

### Option 2: Accès via le Container MariaDB

Pour ouvrir un terminal MariaDB dans son container, lancez la commande:

```bash
docker-compose exec db mysql -u root -p
```

Utilisez ensuite le mot de passe `MYSQL_ROOT_PASSWORD` défini dans votre `.env` .

## Seed de la BDD

Notre API est conçue avec un seeding automatique, afin de peupler la base de données de fausses données pour un environnement de dev ou de démonstration.

Si vous souhaitez mettre ce projet en production, il vous suffit de ne pas renseigner dans le `.env` les variables d'environnement à partir de **SEED_DB** jusqu'à **SEED_USERS**

## Éxécution des Tests

### Option 1: Lancer les Tests dans un Container de Test Dédié

Pour lancer les tests dans un container disposable, utilisez la commande suivante:

```bash
docker-compose run --rm fastapi pytest -W ignore::DeprecationWarning
```

Cette commande permettra de plus d'ignorer les Warnings de Dépréciation, inutiles pour notre cas.

### Option 2: Lancer les Tests à l'intérieur du Container FastAPI

Pour lancer les Tests manuellement, entrez dans le container grâce à la commande:

```bash
docker-compose exec fastapi bash
```

Puis éxécutez les tests avec la commande:

```bash
pytest -W ignore::DeprecationWarning
```

Encore une fois, cette commande ignorera les Warnings de Dépréciation.

## Pour Déboguer

Pour accéder au container FastAPI pour le débogage utilisez la commande:

```bash
docker-compose exec fastapi bash
```

Vous pourrez accéder aux logs dans les containers FastAPI ou MariaDB avec les commandes suivantes:

```bash
docker-compose logs fastapi
docker-compose logs db
```
