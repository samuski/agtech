from django.db import models

class Upload(models.Model):
    file = models.FileField(upload_to='uploads/')
    result_file = models.FileField(upload_to='results/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Upload {self.id} at {self.uploaded_at}"
