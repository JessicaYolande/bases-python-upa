"""TP 3 - Le stock d'une épicerie (dictionnaires imbriqués, get, items, JSON)."""
import json
from collections import Counter

stock = {
    "riz": {"prix": 3200, "quantite": 50},
    "huile": {"prix": 9500, "quantite": 12},
    "sucre": {"prix": 4000, "quantite": 30},
    "savon": {"prix": 1500, "quantite": 0},
}

# --- Question 1 : affichage du stock ---
print("Question 1")
for produit, infos in stock.items():
    print(f"{produit} : {infos['prix']} Ar, quantité {infos['quantite']}")

# --- Question 2 : valeur totale du stock ---
print("\nQuestion 2")
valeur_totale = sum(infos["prix"] * infos["quantite"] for infos in stock.values())
print(f"Valeur totale : {valeur_totale:,} Ar".replace(",", " "))  # Attendu : 394 000 Ar

# --- Question 3 : produits en rupture ---
print("\nQuestion 3")
ruptures = [produit for produit, infos in stock.items() if infos["quantite"] == 0]
print(ruptures)  # Attendu : ['savon']


# --- Question 4 : vendre ---
def vendre(stock, produit, quantite):
    """Vend un produit. Renvoie un tuple (succes, message)."""
    article = stock.get(produit)
    if article is None:
        return False, f"Produit inconnu : {produit}"
    if quantite > article["quantite"]:
        return False, f"Stock insuffisant pour {produit} ({article['quantite']} disponibles)"
    article["quantite"] -= quantite
    return True, f"Vente de {quantite} {produit} réussie"


print("\nQuestion 4")
print(vendre(stock, "riz", 5))        # vente réussie
print(vendre(stock, "farine", 1))     # produit inconnu
print(vendre(stock, "huile", 100))    # quantité trop grande


# --- Question 5 : ajouter un produit ---
def ajouter_produit(stock, nom, prix, quantite):
    """Ajoute un produit, refuse un produit déjà présent. Renvoie (succes, message)."""
    if nom in stock:
        return False, f"{nom} existe déjà"
    stock[nom] = {"prix": prix, "quantite": quantite}
    return True, f"{nom} ajouté"


print("\nQuestion 5")
print(ajouter_produit(stock, "farine", 2800, 20))
print(ajouter_produit(stock, "riz", 3200, 10))

# --- Question 6 : prix augmentés de 10 % ---
print("\nQuestion 6")
prix_hausse = {produit: round(infos["prix"] * 1.10) for produit, infos in stock.items()}
print(prix_hausse)

# --- Question 7 : compter les ventes ---
print("\nQuestion 7")
ventes = ["riz", "sucre", "riz", "huile", "riz"]

compteur = {}
for produit in ventes:
    compteur[produit] = compteur.get(produit, 0) + 1
print(compteur)  # Attendu : {'riz': 3, 'sucre': 1, 'huile': 1}
print(dict(Counter(ventes)))

# --- Question 8 : sauvegarde et rechargement JSON ---
print("\nQuestion 8")
with open("stock.json", "w", encoding="utf-8") as f:
    json.dump(stock, f, ensure_ascii=False, indent=2)

with open("stock.json", "r", encoding="utf-8") as f:
    stock_recharge = json.load(f)

print(f"Les deux dictionnaires sont égaux : {stock == stock_recharge}")  # Attendu : True