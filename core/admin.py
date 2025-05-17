# 📁 Fichier : core/admin.py
# 🧠 Rôle : Ce fichier permet de déclarer les modèles (classes) définis dans models.py
#          pour qu’ils soient accessibles depuis l’interface d’administration Django.
#
# 📌 Actuellement, l’app `core` ne contient aucun modèle personnalisé (aucune table spécifique en base de données).
#     - Tu n’as donc rien à enregistrer dans le panneau d’administration pour l’instant.
#     - Ce fichier est néanmoins préparé pour l’avenir.
#
# 🔄 Plus tard, si tu ajoutes un modèle comme ContactMessage, FaqEntry, ou StaticPage dans core/models.py,
#     tu pourras revenir ici et les enregistrer avec la fonction `admin.site.register(...)`.

# ---------------------------------------------------------------------
# 📦 IMPORTS
# ---------------------------------------------------------------------
from django.contrib import admin  # 🔧 Import du module admin natif de Django
# from .models import ...         # 📭 (À décommenter si tu ajoutes des modèles dans core/models.py)

# ---------------------------------------------------------------------
# ✅ ENREGISTREMENT DES MODÈLES (optionnel)
# ---------------------------------------------------------------------
# Exemple à ajouter plus tard :
#
# from .models import ContactMessage
# @admin.register(ContactMessage)
# class ContactMessageAdmin(admin.ModelAdmin):
#     list_display = ("email", "subject", "created_at")  # 🧾 Colonnes visibles dans la liste admin
#     search_fields = ("email", "subject")               # 🔎 Champs que l'on peut chercher dans l'interface

# 🔒 Pour l’instant, ce fichier est vide car aucun modèle n’a encore été défini ici.
#     Tu peux le laisser tel quel sans erreur. Il est prêt à être utilisé quand tu voudras ajouter des modèles publics.
