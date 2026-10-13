"""TP 1 - Les notes d'une classe (listes, découpage, compréhensions, sorted)."""

notes = [12, 8, 15, 17, 9, 11, 14, 6, 13, 16]

# --- Question 1 : statistiques de base ---
print("Question 1")
print(f"Nombre de notes : {len(notes)}")
print(f"Moyenne : {sum(notes) / len(notes):.2f}")
print(f"Min : {min(notes)} | Max : {max(notes)}")
# Attendu : 10 notes, moyenne 12.10, min 6, max 17

# --- Question 2 : notes >= 10 et nombre d'ajournés ---
print("\nQuestion 2")
admis = [n for n in notes if n >= 10]
ajournes = len(notes) - len(admis)
print(admis)
print(f"{ajournes} ajournés")
# Attendu : [12, 15, 17, 11, 14, 13, 16] et 3 ajournés

# --- Question 3 : tri sans modifier la liste d'origine, puis top 3 ---
print("\nQuestion 3")
croissant = sorted(notes)  # nouvelle liste, notes reste intacte
print(croissant)
trois_meilleures = sorted(notes, reverse=True)[:3]  # découpage
print(trois_meilleures)
# Attendu : [17, 16, 15]

# --- Question 4 : points après délibération (plafonnés à 10) ---
print("\nQuestion 4")
apres_deliberation = [min(n + 2, 10) if n < 10 else n for n in notes]
print(apres_deliberation)
# Attendu : [12, 10, 15, 17, 10, 11, 14, 8, 13, 16]


# --- Question 5 : histogramme par tranche ---
def histogramme(notes):
    """Affiche une étoile par note, regroupées par tranche."""
    tranches = [(0, 4), (5, 9), (10, 14), (15, 20)]
    for debut, fin in tranches:
        effectif = len([n for n in notes if debut <= n <= fin])
        etiquette = f"{debut}-{fin}"
        print(f"{etiquette:<6}| {'*' * effectif}")


print("\nQuestion 5")
histogramme(notes)


# --- Question 6 : rang d'une note ---
def rang(notes, note):
    """Renvoie la position d'une note dans le classement décroissant (1 = meilleure)."""
    classement = sorted(notes, reverse=True)
    return classement.index(note) + 1


print("\nQuestion 6")
print(f"rang(notes, 14) = {rang(notes, 14)}")  # Attendu : 4

# --- Question 7 (bonus) : fusion sans doublons, ordre conservé ---
print("\nBonus")
fusion = list(dict.fromkeys(notes + [15, 6, 18]))
print(fusion)
# dict.fromkeys garde la première apparition de chaque valeur (ordre d'insertion)