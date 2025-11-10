# Assure-toi d'avoir installé la librairie qrcode : pip install qrcode[pil]

import qrcode

# URL à convertir en QR code
url = "https://www.facebook.com/profile.php?id=100016873663558"

# Créer l'objet QR code
qr = qrcode.QRCode(
    version=1,  # taille du QR code (1 à 40, 1 = petit)
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,  # taille de chaque "case"
    border=4      # largeur de la bordure
)

# Ajouter l'URL
qr.add_data(url)
qr.make(fit=True)

# Générer l'image
img = qr.make_image(fill_color="black", back_color="white")

# Sauvegarder l'image
img.save("./python-scripts/qrcode.png")

print("QR code généré et sauvegardé dans qrcode.png")