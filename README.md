# HIDS - système de détection d'intrusion basé sur l'hôte et l'IA

## Introduction  
Notre **HIDS** (Host Intrusion Detection System) est composé de **deux éléments principaux** :  
- **Agents** installés sur chaque machine, responsables de la collecte et de l’analyse des requêtes.  
- **Serveur central**, chargé de la gestion des alertes et de l’interface utilisateur.  

Notre solution hybride combine 3 systèmes de vérifications :
- **analyse locale**
- **vérification cloud**
- **intelligence artificielle**

---

##  Fonctionnalités  

###  **Agents locaux**  
Chaque machine exécute un agent qui **surveille et analyse les requêtes** à l’aide de **trois méthodes de vérification** :  

- **Analyse locale** : Détection basée sur des **signatures connues** avec **Yara, Snort et Suricata**.
- **Vérification en ligne** : Interrogation d’**APIs de sécurité** (VirusTotal, AbuseIPDB, OTX) pour identifier les menaces connues.  
- **Détection avancée** : Utilisation d’un **modèle d’IA** entraîné à repérer des **comportements suspects et anomalies**.  

### ️ **Serveur central**  
Le serveur **centralise et affiche les alertes** grâce à une **interface graphique sécurisée**. Il permet aux administrateurs de :  
- **Suivre l’état des machines** protégées.  
- **Gérer les alertes et incidents**.  
- **Mettre à jour** les méthodes de vérification en temps réel.  

---


##  Installation  

1. **Cloner le projet**  
   ```bash
   git clone -b tls_server --single-branch https://github.com/enchantuer/HIDS
   cd HIDS
   ```
2. **Mise en place des variables d'environnement**
   Renomer le fichier `hidden.env` en `.env`
   ```bash
   mv hidden.env .env
   ```
   Puis changer les variable d'environnement dans le fichier selon vos préférence
   * Il est fortement conseiller de changer la clé secret django : `DJANGO_SECRET_KEY`
   * Afin de pouvoir acceder au site depuis l'exterieur de la machine, il faut ajouter les ip hôtes utiliser pour se connecter au site dans `DJANGO_ALLOWED_HOSTS` en les séparent d'une virgule (`,`)

4. **Lancer avec Docker**  
   * Lancer le serveur
      ```bash
      docker compose up --build
      ```
   * Lancer les clients de test
      ```bash
      docker compose --profile agents up --build client1 client2
      ```

5. **Premier lancement / Mise à jour**
   Lors du premier lancement ou des mises à jour, il est important d'effectuer les migrations afin de créer les tables dans la base de données.
   ```bash
   docker compose exec -it django_app python manage.py migrate
   ```
   
   Si vous souhaitez créer un utilisateur premier utilisateur administrateur, utiliser la commande suivant :
   ```bash
   docker compose exec -it django_app python manage.py createsuperuser
   ```

4. **Accéder à l’interface**  
   Ouvrir un navigateur et aller sur :
   ```
   http://localhost:8000/dashboard
   ```

   Pour le pannel administrateur :  
   ```
   http://localhost:8000/admin
   ```
