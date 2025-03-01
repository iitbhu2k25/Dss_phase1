from django.db import models
from django.urls import reverse
import os

class PDFDocument(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Add FileField
    file = models.FileField(upload_to='pdfs/')
    
    # Check if content_type exists in your database
    # If the column doesn't exist, remove this line or make it null=True
    # content_type = models.CharField(max_length=100, default='application/pdf')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('pdf_detail_api', args=[str(self.id)])
    
    def filename(self):
        return os.path.basename(self.file.name)
    
    @property
    def size_display(self):
        """Display file size in a readable format"""
        size = self.file.size
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024*1024:
            return f"{size/1024:.1f} KB"
        else:
            return f"{size/(1024*1024):.1f} MB"
            
    class Meta:
        db_table = 'confident_pdfdocument'