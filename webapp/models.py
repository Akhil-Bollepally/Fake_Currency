from django.db import models

class UploadHistory(models.Model):
    image = models.ImageField(upload_to='upload/')
    result = models.CharField(max_length=10)  # REAL / FAKE
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"
