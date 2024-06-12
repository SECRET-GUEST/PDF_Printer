import os
from PIL import Image

# Utilisation
input_folder = r"C:\YOUR\PATH\HERE\..."
compile_to_pdf = False  # Mettre True pour compiler toutes les images dans un seul PDF
output_folder_name = "formatted"  # Nom du dossier de sortie
dpi = 300  # Résolution en DPI (points par pouce)
margin_mm = 5  # Marges en millimètres

def process_images(input_folder, compile_to_pdf=False, output_folder_name="formatted", dpi=300, margin_mm=5):
    # Dimensions d'une page A4 en pixels à la résolution spécifiée
    A4_width = round(210 * dpi / 25.4)
    A4_height = round(297 * dpi / 25.4)

    # Marges en pixels
    margin = round(margin_mm * dpi / 25.4)
    printable_width = A4_width - 2 * margin
    printable_height = A4_height - 2 * margin

    # Définir le dossier de sortie
    parent_folder = os.path.dirname(input_folder)
    output_folder = os.path.join(parent_folder, output_folder_name)
    os.makedirs(output_folder, exist_ok=True)

    # Liste pour stocker les images pour le PDF
    images_for_pdf = []

    # Extensions d'image supportées
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif')

    # Fonction pour traiter les images dans un dossier
    def process_folder(folder):
        for root, _, files in os.walk(folder):
            for filename in files:
                if filename.lower().endswith(supported_formats):
                    image_path = os.path.join(root, filename)
                    image = Image.open(image_path)

                    # Redimensionner l'image pour qu'elle rentre dans la zone imprimable tout en conservant les proportions
                    image_ratio = image.width / image.height
                    printable_ratio = printable_width / printable_height

                    if image_ratio > printable_ratio:
                        new_width = printable_width
                        new_height = round(printable_width / image_ratio)
                    else:
                        new_width = round(printable_height * image_ratio)
                        new_height = printable_height

                    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

                    # Créer une image A4 blanche
                    A4_image = Image.new('RGB', (A4_width, A4_height), 'white')

                    # Centrer l'image redimensionnée sur la page A4 avec marges
                    x_offset = (A4_width - new_width) // 2
                    y_offset = (A4_height - new_height) // 2
                    A4_image.paste(resized_image, (x_offset, y_offset))

                    if compile_to_pdf:
                        images_for_pdf.append(A4_image.convert('RGB'))
                    else:
                        # Enregistrer l'image formatée en tant que PDF dans le dossier de sortie
                        output_path = os.path.join(output_folder, os.path.relpath(image_path, input_folder))
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        pdf_path = os.path.splitext(output_path)[0] + ".pdf"
                        A4_image.save(pdf_path, "PDF", resolution=300)

    # Traiter les images dans le dossier principal et les sous-dossiers
    process_folder(input_folder)

    if compile_to_pdf and images_for_pdf:
        pdf_path = os.path.join(output_folder, "compiled_images.pdf")
        images_for_pdf[0].save(pdf_path, save_all=True, append_images=images_for_pdf[1:])

    print("Transformation terminée. Les images formatées se trouvent dans le dossier :", output_folder)
    if compile_to_pdf:
        print("Le PDF compilé se trouve à :", pdf_path)

# Appeler la fonction avec les variables définies
process_images(input_folder, compile_to_pdf, output_folder_name, dpi, margin_mm)
