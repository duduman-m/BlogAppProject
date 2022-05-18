from django.db import models

IN_PROGRESS = 0
APPROVED = 1
REJECTED = 2
STATUS_CHOICES = (
    (IN_PROGRESS, "In progress"),
    (APPROVED, "Approved"),
    (REJECTED, "Rejected")
)


class Article(models.Model):
    """Model containing data of blog posts"""
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=IN_PROGRESS, blank=False)
    written_by = models.ForeignKey("users.Writer", on_delete=models.CASCADE, related_name="articles_written")
    edited_by = models.ForeignKey(
        "users.Writer", on_delete=models.CASCADE, related_name="articles_edited", blank=True, null=True)

    class Meta:
        permissions = [
            ("create", "Can create a new article"),
            ("edit", "Can edit an article"),
            ("approve/reject", "Can approve or reject an article")
        ]
