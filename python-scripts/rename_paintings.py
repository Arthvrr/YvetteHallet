import os
import re

# Dossier contenant les peintures
folder = "../peintures"

# Fonction de nettoyage de nom (enlève accents, espaces, caractères spéciaux)
def clean_filename(filename):
    # Supprimer l'extension temporairement
    name, ext = os.path.splitext(filename)

    # Convertir en minuscules
    name = name.lower()

    # Remplacer les espaces et caractères spéciaux par des tirets
    name = re.sub(r"[^a-z0-9]+", "-", name)

    # Supprimer les tirets au début/fin
    name = name.strip("-")

    # Rattacher l'extension
    return f"{name}{ext.lower()}"

# Renommer les fichiers
def rename_images():
    if not os.path.exists(folder):
        print(f"❌ Le dossier '{folder}' n'existe pas.")
        return

    existing_names = set()
    counter = 1

    for filename in os.listdir(folder):
        old_path = os.path.join(folder, filename)

        if not os.path.isfile(old_path):
            continue

        # Nettoyer le nom
        new_name = clean_filename(filename)

        # Assurer un nom unique
        base, ext = os.path.splitext(new_name)
        while new_name in existing_names or os.path.exists(os.path.join(folder, new_name)):
            new_name = f"{base}-{counter}{ext}"
            counter += 1

        existing_names.add(new_name)

        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"✅ {filename} → {new_name}")

    print("\n✨ Tous les fichiers ont été renommés avec succès !")

if __name__ == "__main__":
    rename_images()