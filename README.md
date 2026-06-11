#  Projet Algorithme 2025-2026 : Optimisation d'un emploi du temps agricole

## Présentation

Ce projet a été réalisé dans le cadre du module d'Algorithmique de la formation Business Data Sciences à l'Université Catholique de l'Ouest (UCO).

L'objectif est de construire un emploi du temps permettant à un agriculteur et à son fils en alternance de récolter l'ensemble de leurs champs dans un temps minimal, tout en respectant plusieurs contraintes liées aux horaires de travail et à l'organisation des tâches.

Le projet a été développé en Python et repose sur la manipulation de données, la programmation orientée objet et la mise en œuvre d'algorithmes de planification.

---

## Objectifs du projet

* Lire et exploiter les données relatives aux champs agricoles et aux travailleurs.
* Générer un planning de récolte cohérent.
* Minimiser le nombre de jours nécessaires à la récolte.
* Respecter les contraintes horaires définies dans l'énoncé.
* Produire un tableau récapitulatif des affectations des travailleurs aux différents champs.

---

## Contraintes à respecter

* Chaque travailleur dispose d'horaires de travail spécifiques.
* Une pause déjeuner obligatoire d'une heure doit être prise entre 12h et 14h.
* Un champ doit être récolté en une seule fois.
* Il est interdit de commencer un champ puis de le terminer ultérieurement.
* Certaines journées peuvent comporter des périodes sans activité.

---

## Architecture du projet

### Classe `Fields`

Cette classe permet :

* de lire les données de l'annexe FIELDS ;
* de stocker les informations relatives aux champs ;
* de récupérer les caractéristiques d'un champ à partir de son identifiant.

### Classe `Workers`

Cette classe permet :

* de lire les données de l'annexe WORKERS ;
* de gérer les horaires de travail ;
* de récupérer les informations d'un travailleur à partir de son identifiant.

### Classe `Calculs`

Cette classe regroupe :

* les fonctions de calcul ;
* les méthodes d'affectation des travailleurs ;
* la génération du planning final ;
* les calculs de durée nécessaires à la récolte.

---

## Résultats attendus

Le programme génère un tableau de planification contenant :

| Worker ID | Field ID |
| --------- | -------- |
| 1         | 12       |
| 2         | 5        |
| ...       | ...      |

Chaque ligne représente l'affectation d'un travailleur à un champ donné.

---

## Technologies utilisées

* Python
* Programmation Orientée Objet (POO)
* Manipulation de données
* Algorithmes de planification
* Matplotlib (bonus graphique)

---

## Compétences développées

* Conception de classes en Python
* Programmation orientée objet
* Gestion de données structurées
* Résolution de problèmes algorithmiques
* Organisation et planification de tâches
* Analyse de contraintes métier

---

## Perspectives d'amélioration

* Mise en place d'algorithmes d'optimisation plus avancés.
* Visualisation graphique améliorée du planning.
* Ajout d'une interface utilisateur.
* Comparaison de plusieurs stratégies de planification.

---

## Auteur

**Mohamed Lamine Bah**

Étudiant en Business Data Sciences

Compétences : Python • SQL • R • Power BI • Analyse de données • Statistiques

Projet réalisé dans le cadre du module d'Algorithmique – Année universitaire 2025-2026.
