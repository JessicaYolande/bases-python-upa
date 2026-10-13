"""TP 5 - Carnet de notes : application en ligne de commande.

Structure imposée : un dictionnaire {matricule: {"nom", "prenom", "notes"}}
où "notes" est un dictionnaire {matière: [liste de notes]}.
"""
import json
from datetime import datetime
from functools import wraps

etudiants = {
    "L3-001": {
        "nom": "Rakoto",
        "prenom": "Soa",
        "notes": {"Python": [15, 14], "Réseaux": [12]},
    },
    "L3-002": {
        "nom": "Rabe",
        "prenom": "Andry",
        "notes": {"Python": [9, 13], "Réseaux": [11, 10]},
    },
}

historique = []  # liste globale de tuples (date et heure, nom de la fonction, arguments)


# ---------------------------------------------------------------- Décorateurs
def journaliser(fonction):
    """Ajoute un tuple (date et heure, nom, arguments) à l'historique à chaque appel."""
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historique.append((horodatage, fonction.__name__, args + tuple(kwargs.values())))
        return fonction(*args, **kwargs)
    return enveloppe


def note_valide(fonction):
    """Refuse toute note qui n'est pas comprise entre 0 et 20."""
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        note = kwargs["note"] if "note" in kwargs else args[2]
        if not 0 <= note <= 20:
            raise ValueError(f"Note invalide ({note}) : elle doit être comprise entre 0 et 20")
        return fonction(*args, **kwargs)
    return enveloppe


def etudiant_existe(fonction):
    """Vérifie que le matricule (premier argument) existe avant d'exécuter la fonction."""
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        matricule = kwargs["matricule"] if "matricule" in kwargs else args[0]
        if matricule not in etudiants:
            raise ValueError(f"Matricule inconnu : {matricule}")
        return fonction(*args, **kwargs)
    return enveloppe


# ----------------------------------------------------------------- Fonctions
@journaliser
def ajouter_etudiant(matricule, nom, prenom):
    """Crée un étudiant ; refuse un matricule déjà existant."""
    if matricule in etudiants:
        raise ValueError(f"Le matricule {matricule} existe déjà")
    etudiants[matricule] = {"nom": nom, "prenom": prenom, "notes": {}}


# Le journal est le décorateur le plus proche de la fonction : seuls les appels
# valides (matricule connu, note correcte) sont donc enregistrés dans l'historique.
@etudiant_existe
@note_valide
@journaliser
def ajouter_note(matricule, matiere, note):
    """Ajoute une note, crée la matière si besoin."""
    etudiants[matricule]["notes"].setdefault(matiere, []).append(note)


def nom_complet(matricule):
    """Renvoie « Prénom Nom » pour un matricule."""
    e = etudiants[matricule]
    return f"{e['prenom']} {e['nom']}"


@etudiant_existe
def moyenne_matiere(matricule, matiere):
    """Moyenne d'un étudiant dans une matière (0.0 s'il n'a pas de note)."""
    notes = etudiants[matricule]["notes"].get(matiere, [])
    return sum(notes) / len(notes) if notes else 0.0


@etudiant_existe
def moyenne_generale(matricule):
    """Moyenne des moyennes de matières."""
    moyennes = [sum(n) / len(n) for n in etudiants[matricule]["notes"].values() if n]
    return sum(moyennes) / len(moyennes) if moyennes else 0.0


def classement():
    """Liste de tuples (nom complet, moyenne) triée par moyenne décroissante."""
    liste = [(nom_complet(m), moyenne_generale(m)) for m in etudiants]
    return sorted(liste, key=lambda paire: paire[1], reverse=True)


def majors():
    """Dictionnaire matière -> nom du meilleur étudiant dans cette matière."""
    matieres = {m for e in etudiants.values() for m in e["notes"]}
    resultat = {}
    for matiere in sorted(matieres):
        candidats = [mat for mat, e in etudiants.items() if matiere in e["notes"]]
        meilleur = max(candidats, key=lambda mat: moyenne_matiere(mat, matiere))
        resultat[matiere] = nom_complet(meilleur)
    return resultat


def sauvegarder(fichier):
    """Enregistre le carnet en JSON."""
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(etudiants, f, ensure_ascii=False, indent=2)


@journaliser
def charger(fichier):
    """Relit le carnet depuis un fichier JSON."""
    with open(fichier, "r", encoding="utf-8") as f:
        donnees = json.load(f)
    etudiants.clear()
    etudiants.update(donnees)


# ---------------------------------------------------------------------- Menu
@etudiant_existe
def afficher_bulletin(matricule):
    """Affiche le bulletin d'un étudiant."""
    print(f"\nBulletin de {nom_complet(matricule)} ({matricule})")
    for matiere, notes in etudiants[matricule]["notes"].items():
        print(f"  {matiere} : {notes} -> moyenne {moyenne_matiere(matricule, matiere):.2f}")
    print(f"  Moyenne générale : {moyenne_generale(matricule):.2f}")


MENU = """
===== CARNET DE NOTES =====
1. Ajouter un étudiant
2. Ajouter une note
3. Afficher un bulletin
4. Afficher le classement
5. Afficher les majors
6. Afficher l'historique
7. Sauvegarder
8. Quitter
"""


def menu():
    """Boucle principale de l'application."""
    while True:
        print(MENU)
        choix = input("Votre choix : ").strip()
        try:
            if choix == "1":
                matricule = input("Matricule : ").strip()
                nom = input("Nom : ").strip()
                prenom = input("Prénom : ").strip()
                ajouter_etudiant(matricule, nom, prenom)
                print("Étudiant ajouté.")
            elif choix == "2":
                matricule = input("Matricule : ").strip()
                matiere = input("Matière : ").strip()
                try:
                    note = float(input("Note : ").replace(",", "."))
                except ValueError:
                    print("Erreur : la note doit être un nombre.")
                    continue
                ajouter_note(matricule, matiere, note)
                print("Note ajoutée.")
            elif choix == "3":
                afficher_bulletin(input("Matricule : ").strip())
            elif choix == "4":
                print("\nClassement")
                for rang, (nom, moyenne) in enumerate(classement(), start=1):
                    print(f"{rang}. {nom} {moyenne:.2f}")
            elif choix == "5":
                print("\nMajors par matière")
                for matiere, nom in majors().items():
                    print(f"  {matiere} : {nom}")
            elif choix == "6":
                print("\nHistorique")
                if not historique:
                    print("  (vide)")
                for horodatage, nom_fonction, arguments in historique:
                    print(f"  {horodatage} | {nom_fonction} | {arguments}")
            elif choix == "7":
                sauvegarder("carnet.json")
                print("Carnet sauvegardé dans carnet.json")
            elif choix == "8":
                print("Au revoir !")
                break
            else:
                print("Choix invalide, tapez un nombre de 1 à 8.")
        except ValueError as erreur:
            print(f"Erreur : {erreur}")


if __name__ == "__main__":
    menu()