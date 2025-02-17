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
   git clone https://github.com/enchantuer/HIDS
   cd hids-hybride
   ```

2. **Lancer avec Docker**  
   ```bash
   docker-compose up -d
   ```

3. **Accéder à l’interface**  
   Ouvrir un navigateur et aller sur :  
   ```
   http://localhost:8080
   ```