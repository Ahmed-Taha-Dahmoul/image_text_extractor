from django.db import models

class ExtractedText(models.Model):
    image = models.ImageField(upload_to='images/')
    extracted_text = models.TextField()

    def __str__(self):
        return self.image.name
