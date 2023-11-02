from django.shortcuts import render
from django.http import JsonResponse
from PIL import Image
import pytesseract
from .models import ExtractedText
from django.conf import settings
import os
def index(request):
    return render(request, 'index.html')



from django.core.files import File

from django.core.files.uploadedfile import InMemoryUploadedFile

from django.core.files.uploadedfile import InMemoryUploadedFile

import json
import pytesseract
import re

def upload_image(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('image')
        if uploaded_image:
            image_path = os.path.join(settings.MEDIA_ROOT, 'images', uploaded_image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            extracted_text = extract_text(image_path)
            if extracted_text:
                cleaned_text = clean_and_format_text(extracted_text)

                # Create an instance of ExtractedText model
                extracted_text_instance = ExtractedText(image=uploaded_image, extracted_text=cleaned_text)
                extracted_text_instance.save()  # Save the extracted text along with the image

                response_data = {
                    'status': 'success',
                    'text': cleaned_text,
                    'image_url': extracted_text_instance.image.url,  # Include the image URL in the response
                }
                return JsonResponse(response_data)

    return JsonResponse({'status': 'error', 'message': 'Image upload or text extraction failed.'})


def extract_text(image_path):
    try:
        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img, config=settings.TESSERACT_CMD)
        return extracted_text
    except Exception as e:
        return str(e)



def clean_and_format_text(text):
    # Replace multiple line breaks with a single line break
    cleaned_text = re.sub(r'\n+', '\n', text)

    # Replace multiple spaces with a single space outside code blocks
    cleaned_text = re.sub(r'([^`]) +', r'\1 ', cleaned_text)

    # Maintain code blocks in their structure, including spaces
    code_blocks = re.findall(r'```(.*?)```', cleaned_text, flags=re.DOTALL)
    for block in code_blocks:
        cleaned_text = cleaned_text.replace(f'```{block}```', f'```{block}```')

    return cleaned_text
