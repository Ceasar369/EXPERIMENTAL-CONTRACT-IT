# 📁 Fichier : core/models.py
# 🧠 Rôle : Ce fichier contient les définitions des modèles de base de données pour l'application `core`.
#          Les modèles sont des classes Python qui représentent des objets que tu veux stocker dans la base de données
#          (par exemple : formulaire de contact, articles de blog, pages statiques, questions fréquentes...).
#
# ✅ Actuellement, l'application `core` est principalement utilisée pour afficher des pages publiques,
#    donc elle ne contient pas encore de modèle actif.
#
# ⚙️ Ce fichier reste néanmoins un point central où tu pourras ajouter plus tard :
#     - un modèle `ContactMessage` (pour stocker les messages envoyés via la page Contact Us),
#     - un modèle `FaqEntry` (pour des FAQ dynamiques modifiables depuis l’admin),
#     - un modèle `StaticPage` (pour gérer des pages personnalisées éditables par l’admin).

# ---------------------------------------------------------------------
# 📦 IMPORTS
# ---------------------------------------------------------------------
from django.db import models  # 🧱 Import du module de modélisation de Django (obligatoire)

# ---------------------------------------------------------------------
# 📌 EXEMPLE DE MODÈLE FUTUR — Formulaire de contact (à activer si besoin plus tard)
# ---------------------------------------------------------------------
# class ContactMessage(models.Model):
#     """📝 Représente un message envoyé par un visiteur via la page de contact du site."""
#
#     name = models.CharField(max_length=100)  # 👤 Nom de l’expéditeur
#     email = models.EmailField()              # 📧 Adresse courriel
#     subject = models.CharField(max_length=150)  # 🏷 Sujet du message
#     message = models.TextField()             # 💬 Contenu du message
#     created_at = models.DateTimeField(auto_now_add=True)  # 🕒 Date d’envoi
#
#     def __str__(self):
#         return f"Message from {self.name} — {self.subject}"

# ---------------------------------------------------------------------
# 📌 EXEMPLE DE MODÈLE FUTUR — Entrée de FAQ
# ---------------------------------------------------------------------
# class FaqEntry(models.Model):
#     """📚 Représente une question fréquente et sa réponse affichée dans la page Help."""
#
#     question = models.CharField(max_length=255)  # ❓ La question
#     answer = models.TextField()                 # 💡 La réponse
#     is_active = models.BooleanField(default=True)  # ✅ Pour afficher ou cacher l'entrée
#
#     def __str__(self):
#         return self.question

# ---------------------------------------------------------------------
# 📌 À SAVOIR :
# - Chaque modèle défini ici crée une table dans ta base de données après migration (`makemigrations` + `migrate`)
# - Tu pourras ensuite les enregistrer dans `admin.py` pour les voir dans l’interface admin Django
# - Tu pourras aussi créer des formulaires, des vues et des templates pour afficher/traiter ces modèles
