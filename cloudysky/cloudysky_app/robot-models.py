

#Used ChatGPT 5

#Prompt Used: Create a simplified Django models.py file for a web-based chat app called CloudySky: An Ideologically Consonant Chat Environment.  
# There should be a UserProfile model extending Django’s built-in User with fields for role (either “admin” or “serf”), a short bio text, and an avatar image. 
# A Post model should represent user-created posts, containing fields for author, content, a timestamp for creation, a boolean field is_suppressed to mark whether a post has been hidden by an administrator, 
# and there should be a dropdown menu for a list of suppression reasons. 
# A Comment model should be linked to both a Post and a User, include text content and creation timestamp fields, and also have an is_suppressed boolean and suppression_reason field for moderation. 
# Include a simple Media model for file or image uploads linked to a Post.



#Output 


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("serf", "Serf"),
        ("admin", "Administrator"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="serf")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class SuppressionReason(models.Model):
    """List of preset reasons admins can select when hiding content."""
    reason_text = models.CharField(max_length=200)

    def __str__(self):
        return self.reason_text


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_suppressed = models.BooleanField(default=False)
    suppression_reason = models.ForeignKey(
        SuppressionReason, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Post {self.id} by {self.author.username}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_suppressed = models.BooleanField(default=False)
    suppression_reason = models.ForeignKey(
        SuppressionReason, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Comment {self.id} by {self.author.username}"


class Media(models.Model):
    """Allows attaching media files (like images) to posts."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media", null=True, blank=True)
    file = models.FileField(upload_to="media/")
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Media {self.id} for Post {self.post_id}"