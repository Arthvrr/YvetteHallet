import os
import re
import unicodedata

# --- CONFIGURATION ---
DOSSIER = "peintures"
EXCLURE = ["pp.jpeg", "pp.jpg", "cv.docx", "cv.pdf", ".ds_store"]
# METTRE False UNIQUEMENT QUAND TU ES SÛR DE TOI APRÈS UN ESSAI
DRY_RUN = False 

# Dictionnaire pour compter les IDs par technique
# Ex: {'huile-sur-bois': 1, 'aquarelle': 1}
compteurs_style = {}

def nettoyer_texte(texte):
    """Enlève les accents, met en minuscule et remplace les espaces par des tirets."""
    if not texte: return ""
    # Enlever accents
    texte = unicodedata.normalize('NFD', texte).encode('ascii', 'ignore').decode("utf-8")
    texte = texte.lower()
    # Remplacer tout ce qui n'est pas a-z ou 0-9 par un tiret
    texte = re.sub(r'[^a-z0-9]', '-', texte)
    # Enlever les tirets multiples et les tirets de début/fin
    texte = re.sub(r'-+', '-', texte)
    return texte.strip('-')

def extraire_infos(nom_fichier):
    base_name, ext = os.path.splitext(nom_fichier)
    nom_nettoye = base_name # Copie de travail

    # 1. TECHNIQUE (On cherche d'abord, c'est la base du tri)
    technique = "technique-mixte" # Valeur par défaut
    keywords = {
        "huile sur bois": "huile-sur-bois",
        "huile sur toile": "huile-sur-toile",
        "huile sur carton": "huile-sur-carton",
        "acrylique": "acrylique",
        "aquarelle": "aquarelle",
        "encre": "encre",
        "plexi": "plexi",
        "stylo": "stylo",
        "crayon": "crayon",
        "sculpture": "sculpture",
        "cirage": "cirage",
        "cire": "cire",
        "collage": "collage"
    }
    
    # On cherche la technique et on l'enlève du nom pour nettoyer le titre
    found_tech = False
    for key, value in keywords.items():
        if key in nom_nettoye.lower():
            technique = value
            nom_nettoye = re.sub(key, "", nom_nettoye, flags=re.IGNORECASE)
            found_tech = True
            break # On prend la première correspondance (la plus longue idéalement)

    # 2. ANNÉE (4 chiffres)
    annee = "sans-date"
    match_annee = re.search(r'(19\d{2}|20\d{2})', nom_nettoye)
    if match_annee:
        annee = match_annee.group(1)
        # On enlève l'année du nom
        nom_nettoye = nom_nettoye.replace(annee, "")

    # 3. DIMENSIONS
    dimension = "dimension-inconnue"
    # Regex : cherche "80x80", "80 cm x 80", etc.
    match_dim = re.search(r'(\d+(?:[.,]\d+)?\s*(?:cm)?\s*[xX]\s*\d+(?:[.,]\d+)?(?:\s*[xX]\s*\d+(?:[.,]\d+)?)?)', nom_nettoye, re.IGNORECASE)
    if match_dim:
        raw_dim = match_dim.group(1)
        # Nettoyage de la dimension pour le nom de fichier
        clean_dim = re.sub(r'\s*cm\s*', '', raw_dim, flags=re.IGNORECASE) # Enleve "cm"
        clean_dim = re.sub(r'\s*[xX]\s*', 'x', clean_dim) # Normalise le "x"
        clean_dim = clean_dim.replace(',', '.') # Virgule en point
        clean_dim = clean_dim.replace(' ', '') # Enleve les espaces
        
        # Vérification si c'est vraiment une dimension (parfois ça attrape juste un chiffre)
        if 'x' in clean_dim: 
            dimension = clean_dim
            nom_nettoye = nom_nettoye.replace(raw_dim, "")

    # 4. TITRE (Nettoyage final)
    # On enlève les vieux numéros au début (ex: "10 Portrait...")
    nom_nettoye = re.sub(r'^\s*\d+[\s_-]*', '', nom_nettoye)
    
    titre = nettoyer_texte(nom_nettoye)
    
    # Si le titre est vide ou trop court (ex: juste des tirets), on met "sans-titre"
    if len(titre) < 3:
        titre = "sans-titre"

    return technique, dimension, titre, annee, ext

def main():
    print(f"--- DÉBUT DU TRAITEMENT (Simulation: {DRY_RUN}) ---")
    
    if not os.path.exists(DOSSIER):
        print(f"Erreur : Le dossier '{DOSSIER}' n'existe pas.")
        return

    # On trie les fichiers pour que l'ordre des IDs soit alphabétique par rapport aux anciens noms
    fichiers = sorted(os.listdir(DOSSIER))
    total_renommes = 0

    for fichier in fichiers:
        if fichier.lower() in EXCLURE or fichier.startswith('.'):
            continue
        
        # Filtre extensions images/docs
        if not fichier.lower().endswith(('.jpg', '.jpeg', '.png', '.docx')):
            continue

        chem_ancien = os.path.join(DOSSIER, fichier)
        
        # Extraction des données
        tech, dim, titre, annee, ext = extraire_infos(fichier)
        
        # GESTION DU COMPTEUR (ID)
        # Si on n'a jamais vu cette technique, on initialise à 1, sinon on ajoute 1
        if tech not in compteurs_style:
            compteurs_style[tech] = 1
        else:
            compteurs_style[tech] += 1
            
        id_courant = compteurs_style[tech]

        # Normalisation extension
        if ext.lower() == ".jpeg": ext = ".jpg"
        
        # CONSTRUCTION DU NOUVEAU NOM
        # Format : technique-id-dimension-titre-année.jpg
        nouveau_nom = f"{tech}-{id_courant}-{dim}-{titre}-{annee}{ext}".lower()
        
        chem_nouveau = os.path.join(DOSSIER, nouveau_nom)

        # Action
        if chem_ancien != chem_nouveau:
            print(f"[RENAME] {fichier}")
            print(f"      -> {nouveau_nom}")
            
            if not DRY_RUN:
                try:
                    os.rename(chem_ancien, chem_nouveau)
                    total_renommes += 1
                except Exception as e:
                    print(f"ERREUR: {e}")
        else:
            print(f"[OK] {fichier} est déjà correct.")

    print(f"\n--- FINI ---")
    print(f"Fichiers traités. Total: {total_renommes}")
    if DRY_RUN:
        print("⚠️ Ceci était une simulation. Passe la variable DRY_RUN à False pour exécuter réellement.")

if __name__ == "__main__":
    main()