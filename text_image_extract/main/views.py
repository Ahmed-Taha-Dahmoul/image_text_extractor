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

def upload_image(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('image')
        if uploaded_image:
            # Check if the uploaded file has a simple name (no special characters)
            image_path = os.path.join(settings.MEDIA_ROOT, 'images', uploaded_image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)
            
            # Perform text extraction here
            extracted_text = extract_text(image_path)
            if extracted_text:
                # Create a new ExtractedText object and save it
                extracted_text_obj = ExtractedText(image=uploaded_image, extracted_text=extracted_text)
                extracted_text_obj.save()

                return JsonResponse({'status': 'success', 'text': extracted_text})

    return JsonResponse({'status': 'error', 'message': 'Image upload or text extraction failed.'})




def extract_text(image):
    try:
        img = Image.open(image)
        extracted_text = pytesseract.image_to_string(img, config=settings.TESSERACT_CMD)
        return extracted_text
    except Exception as e:
        return str(e)



