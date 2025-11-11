import os

# Dossier où se trouve ce script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Dossier où sont tes images
image_folder = os.path.join(script_dir, "../peintures")

# Vérifier que le dossier existe
if not os.path.exists(image_folder):
    raise FileNotFoundError(f"❌ Le dossier {image_folder} est introuvable.")

# Récupérer tous les fichiers images
images = [f for f in os.listdir(image_folder)
          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Trier les images par nom
images.sort()

# Nombre de cartes par ligne
cards_per_row = 3

html_output = ""

for i in range(0, len(images), cards_per_row):
    html_output += '<div class="row">\n'
    for img in images[i:i+cards_per_row]:
        html_output += f'    <div class="card">\n'
        html_output += f'        <img src="../peintures/{img}" alt="{img}" onclick="showZoom(this)">\n'
        html_output += '    </div>\n'
    html_output += '</div>\n\n'

# 🔥 Sauvegarder le HTML dans le même dossier que le script
output_file = os.path.join(script_dir, "images_gallery_en.html")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"✅ HTML généré dans '{output_file}'. ({len(images)} images traitées)")