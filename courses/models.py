import random
import string
from django.db import models
from django.contrib.auth.models import User

def generate_share_code():
    chars = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choice(chars) for _ in range(6))
        if not ListeCourses.objects.filter(share_code=code).exists():
            return code 


class ListeCourses(models.Model):
    nom = models.CharField(max_length=100)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    share_code = models.CharField(
        max_length=6, 
        unique = True,
        blank = True,
        db_index=True,
        verbose_name="Code de partage"
    )

    membres = models.ManyToManyField(
        User, 
        related_name="listes_partagees", 
        blank=True,
        verbose_name="Autres personnes"
        )

    def save(self, *args, **kwargs):
        if not self.share_code:
            self.share_code = generate_share_code()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nom

class Article(models.Model):
    liste = models.ForeignKey(ListeCourses, on_delete=models.CASCADE, related_name='articles')
    nom = models.CharField(max_length=100)
    quantite = models.PositiveIntegerField(default=1)
    achete = models.BooleanField(default=False)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.quantite})"
