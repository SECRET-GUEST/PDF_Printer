```
██╗███╗   ███╗ ██████╗     ██████╗     ██████╗ ██████╗ ███████╗
██║████╗ ████║██╔════╝     ╚════██╗    ██╔══██╗██╔══██╗██╔════╝
██║██╔████╔██║██║  ███╗     █████╔╝    ██████╔╝██║  ██║█████╗  
██║██║╚██╔╝██║██║   ██║    ██╔═══╝     ██╔═══╝ ██║  ██║██╔══╝  
██║██║ ╚═╝ ██║╚██████╔╝    ███████╗    ██║     ██████╔╝██║     
╚═╝╚═╝     ╚═╝ ╚═════╝     ╚══════╝    ╚═╝     ╚═════╝ ╚═╝     
```

![Javascript](https://img.shields.io/badge/JAVASCRIPT-yellow)
![ALPHA](https://img.shields.io/badge/ALPHA-red) 

# PDF Printer

PDF Printer is a web application and Python script that converts images into PDF files, either individually or by compiling them into a single PDF. The project includes a user-friendly interface that allows for drag-and-drop functionality for easy conversion.

## Link

### [Click here for the website](https://secret-guest.github.io/PDF_Printer/)

## Web Application Usage

1. **Access the Web Application**: Visit the link above to access the application.
2. **Drag-and-Drop**: Drop your images into the drop zone or click to select files.
3. **Settings**:
   - **DPI**: Set the resolution in DPI (dots per inch).
   - **Margins (mm)**: Define the margins in millimeters.
   - **PDF Option**: Choose between creating a single PDF or individual PDF files.
4. **Start the Process**: Click the "Start Processing" button to begin the conversion.
5. **Download Files**: Once the conversion is complete, download the generated files.

## Python Script Usage

The Python script allows you to convert images into PDF files, either individually or by compiling them into a single PDF. Here is how to use it:

### Prerequisites

- Python 3.x
- PIL (Pillow) library

You can install Pillow with the following command:
```sh
pip install pillow
```

### Python Script

```python
import os
from PIL import Image

# Usage
input_folder = r"C:\YOUR\PATH\HERE\..."
compile_to_pdf = False  # Set to True to compile all images into a single PDF
output_folder_name = "formatted"  # Output folder name
dpi = 300  # Resolution in DPI (dots per inch)
margin_mm = 5  # Margins in millimeters

def process_images(input_folder, compile_to_pdf=False, output_folder_name="formatted", dpi=300, margin_mm=5):
    # Dimensions of an A4 page in pixels at the specified resolution
    A4_width = round(210 * dpi / 25.4)
    A4_height = round(297 * dpi / 25.4)

    # Margins in pixels
    margin = round(margin_mm * dpi / 25.4)
    printable_width = A4_width - 2 * margin
    printable_height = A4_height - 2 * margin

    # Define the output folder
    parent_folder = os.path.dirname(input_folder)
    output_folder = os.path.join(parent_folder, output_folder_name)
    os.makedirs(output_folder, exist_ok=True)

    # List to store images for the PDF
    images_for_pdf = []

    # Supported image formats
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif')

    # Function to process images in a folder
    def process_folder(folder):
        for root, _, files in os.walk(folder):
            for filename in files:
                if filename.lower().endswith(supported_formats):
                    image_path = os.path.join(root, filename)
                    image = Image.open(image_path)

                    # Resize the image to fit within the printable area while maintaining aspect ratio
                    image_ratio = image.width / image.height
                    printable_ratio = printable_width / printable_height

                    if image_ratio > printable_ratio:
                        new_width = printable_width
                        new_height = round(printable_width / image_ratio)
                    else:
                        new_width = round(printable_height * image_ratio)
                        new_height = printable_height

                    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

                    # Create a white A4 image
                    A4_image = Image.new('RGB', (A4_width, A4_height), 'white')

                    # Center the resized image on the A4 page with margins
                    x_offset = (A4_width - new_width) // 2
                    y_offset = (A4_height - new_height) // 2
                    A4_image.paste(resized_image, (x_offset, y_offset))

                    if compile_to_pdf:
                        images_for_pdf.append(A4_image.convert('RGB'))
                    else:
                        # Save the formatted image as a PDF in the output folder
                        output_path = os.path.join(output_folder, os.path.relpath(image_path, input_folder))
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        pdf_path = os.path.splitext(output_path)[0] + ".pdf"
                        A4_image.save(pdf_path, "PDF", resolution=300)

    # Process images in the main folder and subfolders
    process_folder(input_folder)

    if compile_to_pdf and images_for_pdf:
        pdf_path = os.path.join(output_folder, "compiled_images.pdf")
        images_for_pdf[0].save(pdf_path, save_all=True, append_images=images_for_pdf[1:])

    print("Processing complete. Formatted images are in the folder:", output_folder)
    if compile_to_pdf:
        print("The compiled PDF is located at:", pdf_path)

# Call the function with the defined variables
process_images(input_folder, compile_to_pdf, output_folder_name, dpi, margin_mm)
```

### Instructions

1. **Define Variables**:
   - `input_folder`: Folder containing the images to process.
   - `compile_to_pdf`: Set to `True` to compile all images into a single PDF, `False` for individual PDFs.
   - `output_folder_name`: Name of the output folder.
   - `dpi`: Resolution in DPI (dots per inch).
   - `margin_mm`: Margins in millimeters.

2. **Run the Script**: Execute the script with Python to convert the images into PDFs according to the defined settings.

3. **Results**: The generated PDF files will be located in the specified output folder.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
