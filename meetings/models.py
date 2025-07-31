from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Meeting(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    agenda = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, through='MeetingAttendance', related_name='meetings')
    minutes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-date']

class MeetingAttendance(models.Model):
    RESPONSE_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('maybe', 'Maybe'),
    )

    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.CharField(max_length=10, choices=RESPONSE_CHOICES, default='pending')
    attended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('meeting', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.meeting.title}"

class MeetingDocument(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='meeting_documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.meeting.title}"