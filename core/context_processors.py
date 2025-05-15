# core/context_processors.py

# 💡 CONTEXT PROCESSOR DJANGO — user_roles
# -----------------------------------------
# Ce fichier contient une fonction utilisée par Django pour injecter
# des variables globales dans TOUS les templates HTML de ton site.
#
# Ici, la fonction `user_roles()` ajoute automatiquement deux variables :
#     - `is_client` → True si l'utilisateur connecté est un client
#     - `is_contractor` → True si l'utilisateur connecté est un entrepreneur
#
# Grâce à ce fichier, tu peux utiliser ces deux variables directement
# dans n'importe quel fichier HTML (ex: base2.html, dashboard, etc.) :
#
#     {% if is_client %} ... {% endif %}
#
# ⚠️ Ce fichier doit être déclaré dans settings.py pour être actif :
#     TEMPLATES > OPTIONS > context_processors :
#         'core.context_processors.user_roles'
#
# 🔐 Bonus : le code utilise `getattr()` pour éviter toute erreur si
# l'utilisateur est anonyme ou que le champ n'existe pas.

def user_roles(request):
    user = request.user

    return {
        'is_client': getattr(user, 'is_client', False),
        'is_contractor': getattr(user, 'is_contractor', False),
    }
