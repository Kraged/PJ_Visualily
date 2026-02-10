from flask import Blueprint, jsonify, render_template, request
from PIL import Image, ExifTags
import base64
from io import BytesIO

playground_bp = Blueprint('playground', __name__)

@playground_bp.route('/playground')
def index():
    return render_template('playground.html')

# @playground_bp.route('/playground/upload', methods=['GET', 'POST'])
# def upload():
#     # 1. Clear the slate: Start with a fresh empty dictionary for every request
#     full_info = {} 

#     if request.method == 'POST':
#         file = request.files.get('file')
#         if not file:
#             return "No file", 400

#         img = Image.open(file)
        
#         # --- Handle Orientation ---
#         exif_data = img.getexif()
#         if exif_data:
#             orientation = exif_data.get(274)
#             if orientation == 3: img = img.rotate(180, expand=True)
#             elif orientation == 6: img = img.rotate(270, expand=True)
#             elif orientation == 8: img = img.rotate(90, expand=True)

#             # --- Deep Metadata Extraction ---
#             # Loop through primary EXIF tags
#             for tag_id, value in exif_data.items():
#                 tag_name = ExifTags.TAGS.get(tag_id, tag_id)
#                 full_info[str(tag_name)] = str(value)

#             # Dig into sub-directories (IFDs) for "Rich" info (GPS, Interoperability, etc.)
#             # This is where 'MakerNotes' and detailed camera settings usually live
#             for ifd_id in [0x8769, 0x8825, 0x0100]: # Common IFD offsets
#                 try:
#                     ifd = exif_data.get_ifd(ifd_id)
#                     for tag_id, value in ifd.items():
#                         tag_name = ExifTags.TAGS.get(tag_id, tag_id)
#                         full_info[f"{tag_name}"] = str(value)
#                 except:
#                     continue

#         # Add basic info last so it stays at the top/bottom
#         full_info["Final_Resolution"] = f"{img.size[0]} x {img.size[1]}"
#         # Prepare Image for Display
#         buffered = BytesIO()
#         img.save(buffered, format="JPEG")
#         img_str = base64.b64encode(buffered.getvalue()).decode()
#         image_data = f"data:image/jpeg;base64,{img_str}"

#         return render_template('playground.html', info=full_info, uploaded_image=image_data)

#     return render_template('playground.html', info=None)



@playground_bp.route('/api/analyze', methods=['POST'])
def analyze():
    # 'file' matches the name given in FormData on the frontend
    img_file = request.files.get('file')
    full_info = {}
    
    if not img_file:
        return jsonify({'message': 'No image uploaded', 'result': 'error'}), 400

    # --- Handle Orientation ---
    img = Image.open(img_file)
    original_format = img.format if img.format else "PNG" # Default to PNG if unknown
    exif_data = img.getexif()
    if exif_data:
        orientation = exif_data.get(274)
        if orientation == 3: img = img.rotate(180, expand=True)
        elif orientation == 6: img = img.rotate(270, expand=True)
        elif orientation == 8: img = img.rotate(90, expand=True)

        # --- Deep Metadata Extraction ---
        # Loop through primary EXIF tags
        for tag_id, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            full_info[str(tag_name)] = str(value)

        # Dig into sub-directories (IFDs) for "Rich" info (GPS, Interoperability, etc.)
        # This is where 'MakerNotes' and detailed camera settings usually live
        for ifd_id in [0x8769, 0x8825, 0x0100]: # Common IFD offsets
            try:
                ifd = exif_data.get_ifd(ifd_id)
                for tag_id, value in ifd.items():
                    tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                    full_info[f"{tag_name}"] = str(value)
            except:
                continue

    # Add basic info last so it stays at the top/bottom
    full_info["Final_Resolution"] = f"{img.size[0]} x {img.size[1]}"
    # Prepare Image for Display
    buffered = BytesIO()
    img.save(buffered, format=original_format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    image_data = f"data:image/{original_format.lower()};base64,{img_str}"
    
    # For now, we just return the filename to prove it worked
    return jsonify({
        'message': full_info, 
        'imagedp': image_data,
        'result': 'success'
    })
    # # 1. Clear the slate: Start with a fresh empty dictionary for every request
    # full_info = {} 

    # if request.method == 'POST':
    #     file = request.files.get('file')
    #     if not file:
    #         return "No file", 400

    #     img = Image.open(file)
        
    #     # --- Handle Orientation ---
    #     exif_data = img.getexif()
    #     if exif_data:
    #         orientation = exif_data.get(274)
    #         if orientation == 3: img = img.rotate(180, expand=True)
    #         elif orientation == 6: img = img.rotate(270, expand=True)
    #         elif orientation == 8: img = img.rotate(90, expand=True)

    #         # --- Deep Metadata Extraction ---
    #         # Loop through primary EXIF tags
    #         for tag_id, value in exif_data.items():
    #             tag_name = ExifTags.TAGS.get(tag_id, tag_id)
    #             full_info[str(tag_name)] = str(value)

    #         # Dig into sub-directories (IFDs) for "Rich" info (GPS, Interoperability, etc.)
    #         # This is where 'MakerNotes' and detailed camera settings usually live
    #         for ifd_id in [0x8769, 0x8825, 0x0100]: # Common IFD offsets
    #             try:
    #                 ifd = exif_data.get_ifd(ifd_id)
    #                 for tag_id, value in ifd.items():
    #                     tag_name = ExifTags.TAGS.get(tag_id, tag_id)
    #                     full_info[f"{tag_name}"] = str(value)
    #             except:
    #                 continue

    #     # Add basic info last so it stays at the top/bottom
    #     full_info["Final_Resolution"] = f"{img.size[0]} x {img.size[1]}"
    #     # Prepare Image for Display
    #     buffered = BytesIO()
    #     img.save(buffered, format="JPEG")
    #     img_str = base64.b64encode(buffered.getvalue()).decode()
    #     image_data = f"data:image/jpeg;base64,{img_str}"
        
    # return jsonify(full_info)