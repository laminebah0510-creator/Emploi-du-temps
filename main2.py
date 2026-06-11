import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

########======================== Classe Fields ========================########

class Fields:
    def __init__(self, filename='fields.csv'):
        self.fields_data = {}
        self.load_data(filename)

    ####---------lire le fichier et remplit le dictionnaire fields_data-----####
    def load_data(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            print("colonnes détectées:", reader.fieldnames)
            for row in reader:
                field_id = int(row['ID'])
                self.fields_data[field_id] = {
                    'id': field_id,
                    'hectares': float(row['HECTARES'])
                }
    ####--------Retourne le dictionnaire complet d'un champ via son ID. Retourne None si l'ID n'existe pas--------#####
    def get_field(self, field_id):
        return self.fields_data.get(field_id, None)

    ####-------Retourne uniquement la surface en hectares d'un champ.Retourne None si le champ n'existe pas--------####
    def get_hectares(self, field_id):
        field = self.get_field(field_id)
        return field['hectares'] if field else None

    #####------Retourne le dictionnaire complet de tous les champs----------------#######
    def get_all_fields(self):
        return self.fields_data

    #####------Retourne le nombre total de champs chargés------------------------#####
    def get_total_fields(self):
        return len(self.fields_data)


########======================== Classe Workers ========================########
        #####--------C'est le même fonctionnement que la classe fields--------------#####

class Workers:
    def __init__(self, filename='workers.csv'):
        self.workers_data = {}
        self.load_data(filename)

    def load_data(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            print("colonnes détectées:", reader.fieldnames)
            for row in reader:
                worker_id = int(row['ID'])
                self.workers_data[worker_id] = {
                    'id': worker_id,
                    'first_name': row['FIRST_NAME'],
                    'last_name': row['LAST_NAME'],
                    'start_day': int(row['START_DAY']),
                    'end_day': int(row['END_DAY']),
                    'efficiency': float(row['EFFICIENCY'])
                }

    def get_worker(self, worker_id):
        return self.workers_data.get(worker_id, None)

    def get_first_name(self, worker_id):
        worker = self.get_worker(worker_id)
        return worker['first_name'] if worker else None

    def get_last_name(self, worker_id):
        worker = self.get_worker(worker_id)
        return worker['last_name'] if worker else None

    def get_start_day(self, worker_id):
        worker = self.get_worker(worker_id)
        return worker['start_day'] if worker else None

    def get_end_day(self, worker_id):
        worker = self.get_worker(worker_id)
        return worker['end_day'] if worker else None

    def get_efficiency(self, worker_id):
        worker = self.get_worker(worker_id)
        return worker['efficiency'] if worker else None

    def get_all_workers(self):
        return self.workers_data


########======================== Classe Calculs ========================########

class Calculs:
    def __init__(self, fields, workers):
        self.fields = fields
        self.workers = workers

    ####----------calcule du temps nécessaire pour qu'un travailleur récolte un champ donné-------------######
    def calculer_temps_recolte(self, field_id, worker_id):
        hectares = self.fields.get_hectares(field_id)
        efficiency = self.workers.get_efficiency(worker_id)
        if hectares is None or efficiency is None:
            return None
        return hectares / efficiency

    #####----------Calcule du nombre d'heures de travail effectué par jour par un travailleur en tenant en compte la pause d'une heure-----------#######
    def calculer_heures_disponibles_par_jour(self, worker_id):
        start = self.workers.get_start_day(worker_id)
        end = self.workers.get_end_day(worker_id)
        if start is None or end is None:
            return None
        return (end - start) - 1                                # Déduction de la pause déjeuner

    #####----------Vérifie si un travailleur peut récolter un champ donné dans le temps disponible restant d'un créneau.
    def peut_effectuer_field_dans_periode(self, field_id, worker_id, heures_disponibles):
        temps_necessaire = self.calculer_temps_recolte(field_id, worker_id)
        if temps_necessaire is None:
            return False
        return temps_necessaire <= heures_disponibles

    def generer_emploi_du_temps(self):
        emploi_du_temps = []                                   # Liste de listes [worker_id, field_id, jour]

        # Tri des champs par taille décroissante (greedy)
        fields_restants = list(self.fields.get_all_fields().keys())
        fields_restants.sort(key=lambda f: self.fields.get_hectares(f), reverse=True)

        workers_ids = list(self.workers.get_all_workers().keys())

        jour = 1


        while fields_restants:
            progres = False                                     # Détecte si au moins un champ a été assigné ce jour

            for worker_id in workers_ids:
                start = self.workers.get_start_day(worker_id)
                end = self.workers.get_end_day(worker_id)

                    # Créneau matin : start -> 12h
                    # Créneau après-midi : 13h -> end (pause 12h-13h obligatoire)
                heures_matin = 12 - start
                heures_apres_midi = end - 13

                temps_matin_utilise = 0
                temps_apres_midi_utilise = 0

                for field_id in fields_restants.copy():
                    temps_field = self.calculer_temps_recolte(field_id, worker_id)

                    # Un champ doit tenir entièrement dans un seul créneau
                    if temps_matin_utilise + temps_field <= heures_matin:
                        emploi_du_temps.append([worker_id, field_id, jour])
                        temps_matin_utilise += temps_field
                        fields_restants.remove(field_id)
                        progres = True
                    elif temps_apres_midi_utilise + temps_field <= heures_apres_midi:
                        emploi_du_temps.append([worker_id, field_id, jour])
                        temps_apres_midi_utilise += temps_field
                        fields_restants.remove(field_id)
                        progres = True

            # Sécurité : si aucun champ assigné ce jour, on arrête pour éviter boucle infinie
            if not progres:
                print(f"Attention : aucun champ assigné au jour {jour}, arrêt.")
                break
            jour += 1
        return emploi_du_temps

    ########-----------Estimation du nombre de jours nécessaires-------------------#########
    def calculer_nombre_jours_total(self, emploi_du_temps):
        if not emploi_du_temps:
            return 0
        # le jour max présent dans le planning
        return max(assignment[2] for assignment in emploi_du_temps)

##############===========Réalisation de quelques graphiques=====================############
    def generer_graphique(self, emploi_du_temps, filename='emploi_du_temps.png'):
        workers_ids = list(self.workers.get_all_workers().keys())
        couleurs = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']

    #######---------- Graphique 1 : Répartition des champs par travailleur------- ----####

        plt.figure(figsize=(14, 8))

        nombre_fields_par_worker = {w: 0 for w in workers_ids}
        for assignment in emploi_du_temps:
            worker_id = assignment[0]
            nombre_fields_par_worker[worker_id] += 1

        worker_names = []
        field_counts = []
        colors = []

        for worker_id in workers_ids:
            worker = self.workers.get_worker(worker_id)
            worker_names.append(f"{worker['first_name']} {worker['last_name']}")
            field_counts.append(nombre_fields_par_worker[worker_id])
            colors.append(couleurs[worker_id - 1])

        bars = plt.bar(worker_names, field_counts, color=colors, edgecolor='black', linewidth=1.5)

        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)} champs',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

        plt.xlabel('Travailleurs', fontsize=14, fontweight='bold')
        plt.ylabel('Nombre de champs récoltés', fontsize=14, fontweight='bold')
        plt.title('Répartition des champs par travailleur', fontsize=16, fontweight='bold', pad=20)
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Graphique sauvegardé: {filename}")

    ######------------- Graphique 2 : Diagramme de Gantt détaillé -----------####

        plt.figure(figsize=(16, 10))

        ######-------- Reconstruction du planning jour par jour depuis le 3ème élément de chaque affectation---------####
        schedule_by_day = {}
        for assignment in emploi_du_temps:
            worker_id, field_id, jour = assignment
            if jour not in schedule_by_day:
                schedule_by_day[jour] = {w: [] for w in workers_ids}

            ####---------- Calcul de l'heure de début dans le créneau (matin ou après-midi)--------######
            start_worker = self.workers.get_start_day(worker_id)
            temps_field = self.calculer_temps_recolte(field_id, worker_id)

            #####---------Calcul du cumul de temps déjà utilisé ce jour par ce worker------------#####
            temps_deja_utilise = sum(
                self.calculer_temps_recolte(a[1], a[0])
                for a in emploi_du_temps
                if a[0] == worker_id and a[2] == jour and a[1] != field_id
                   and emploi_du_temps.index(a) < emploi_du_temps.index(assignment)
            )
            schedule_by_day[jour][worker_id].append({
                'field_id': field_id,
                'temps': temps_field,
                'start': temps_deja_utilise
            })
        max_day = max(schedule_by_day.keys())

        #######------------Tracé des barres horizontales du Gantt-------------######
        for day in range(1, max_day + 1):
            for worker_idx, worker_id in enumerate(workers_ids):
                if day in schedule_by_day and worker_id in schedule_by_day[day]:
                    for field_info in schedule_by_day[day][worker_id]:
                        ####------------ Chaque barre représente un champ : position = jour, largeur = durée---------####
                        plt.barh(day * len(workers_ids) - worker_idx,
                                field_info['temps'],
                                left=field_info['start'],       # Décalage horizontal (début)
                                height=0.8,
                                color=couleurs[worker_id - 1],
                                edgecolor='black',
                                linewidth=0.5,
                                 ######---------- Légende affichée uniquement pour la première barre du jour 1--------#####
                                label=f"Worker {worker_id}" if day == 1 and field_info == schedule_by_day[day][worker_id][0] else "")

        ######--------Construction des étiquettes de l'axe Y (Jour + Prénom du worker)-------------######
        yticks = []
        ytick_labels = []
        for day in range(1, max_day + 1):
            for worker_idx, worker_id in enumerate(workers_ids):
                worker = self.workers.get_worker(worker_id)
                yticks.append(day * len(workers_ids) - worker_idx)
                ytick_labels.append(f"J{day} - {worker['first_name']}")

        plt.yticks(yticks, ytick_labels, fontsize=10)
        plt.xlabel('Heures de travail', fontsize=14, fontweight='bold')
        plt.ylabel('Jour et Travailleur', fontsize=14, fontweight='bold')
        plt.title('Planning détaillé - Emploi du temps de récolte', fontsize=16, fontweight='bold', pad=20)
        plt.grid(axis='x', alpha=0.3, linestyle='--')

        #######----------------- Légende avec les couleurs par worker------------------#########
        handles = [mpatches.Patch(color=couleurs[i], label=f"Worker {wid}") for i, wid in enumerate(workers_ids)]
        plt.legend(handles=handles, loc='upper right')

        plt.tight_layout()
        plt.savefig('planning_detaille.png', dpi=300, bbox_inches='tight')
        print("Graphique détaillé sauvegardé: planning_detaille.png")


########======================== Programme principal ========================########

def main():
    ######-------- Chargement des données depuis les fichiers CSV-------------########
    fields = Fields('fields.csv')
    workers = Workers('workers.csv')
    calculs = Calculs(fields, workers)

    print("=" * 60)
    print("Voici les résultats attendus")
    print("=" * 60)
    print()

    #######---------- Affichage du nombre d'éléments chargés pour vérification----------######
    print("Champs chargés:", fields.get_total_fields())
    print("travailleurs chargés:", len(workers.get_all_workers()))
    print()

    #######----------- Lancement de l'algorithme de planification----------------#######
    print("Génération de l'emploi du temps optimal")
    emploi_du_temps = calculs.generer_emploi_du_temps()

    print()
    print("=" * 60)
    print("Emploi du temps optimal:")
    print("=" * 60)
    print()
    print(f"Nombre total d'affectations: {len(emploi_du_temps)}")
    print(f"Nombre de jours total: {calculs.calculer_nombre_jours_total(emploi_du_temps)}")
    print()

    #######-------------Affichage détaillé de chaque affectation avec le temps de récolte--------------########
    print("Détails des affectations [Worker_ID, Field_ID, Jour]:")
    print("-" * 60)
    for i, assignment in enumerate(emploi_du_temps, 1):
        worker_id, field_id, jour = assignment
        worker = workers.get_worker(worker_id)
        field = fields.get_field(field_id)
        temps = calculs.calculer_temps_recolte(field_id, worker_id)
        print(f"{i:3d}. [Worker {worker_id}, Field {field_id:2d}, Jour {jour}] - "
              f"{worker['first_name']} {worker['last_name']} "
              f"récolte {field['hectares']}ha en {temps:.2f}h")
    print()
    print("=" * 60)

    #########----------- Affichage du résultat final sous la forme demandée : liste de listes-----------#########
    print("Résultat sous forme de tableau (liste de listes):")
    print(emploi_du_temps)
    print("=" * 60)

    #########--------------Génération et sauvegarde des graphiques-----------------#########s
    print()
    print("=" * 60)
    print("Génération des graphiques...")
    print("-" * 60)
    calculs.generer_graphique(emploi_du_temps)
    print("=" * 60)
    print()
    print("=" * 100)
    print("Projet terminé avec succès!")
    print("=" * 100)

if __name__ == "__main__":
    main()