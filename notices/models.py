from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class NoticeCategory(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color code
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Notice Categories"

    def __str__(self):
        return self.name

class Notice(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(NoticeCategory, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_active = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    valid_until = models.DateTimeField(null=True, blank=True)
    attachment = models.FileField(upload_to='notice_attachments/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-is_pinned', '-created_at']

class NoticeReadStatus(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('notice', 'user')

    def __str__(self):
        return f"{self.user.username} read {self.notice.title}"