import os

# Dossier où sont tes images
image_folder = "/Users/arthurlouette/Documents/Aarthur/Code/YvetteHallet/peintures"

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
        html_output += f'        <img src="peintures/{img}" alt="{img}" onclick="showZoom(this)">\n'
        html_output += '    </div>\n'
    html_output += '</div>\n\n'

# Écrire le HTML dans un fichier
with open("images_gallery.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("HTML généré dans 'images_gallery.html'.")