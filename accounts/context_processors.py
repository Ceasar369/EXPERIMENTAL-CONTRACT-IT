# 📁 Fichier : accounts/context_processors.py
# 🧠 Rôle : Injecter automatiquement des variables liées au rôle utilisateur (client ou entrepreneur)
#          dans tous les templates HTML du site.
#
# 📌 Ce fichier est un "context processor" Django.
#     ➤ Il permet d’ajouter des variables dans tous les templates SANS devoir les passer manuellement dans chaque vue.
#
# ✅ Concrètement, on injecte ici deux variables globales :
#     - `is_client`     → True si l'utilisateur est connecté et possède le rôle client
#     - `is_contractor` → True si l'utilisateur est connecté et possède le rôle entrepreneur
#
# 🧩 Ces variables sont ensuite disponibles dans les templates HTML, par exemple :
#
#     {% if is_client %}       <!-- Afficher un bouton réservé aux clients -->  {% endif %}
#     {% if is_contractor %}   <!-- Afficher des liens réservés aux entrepreneurs -->  {% endif %}
#
# ⚙️ Activation requise :
#     ➤ Tu dois référencer cette fonction dans `settings.py` :
#
#     TEMPLATES = [
#         {
#             ...
#             'OPTIONS': {
#                 'context_processors': [
#                     ...
#                     'accounts.context_processors.user_roles',  # ✅ à inclure ici
#                 ],
#             },
#         },
#     ]
#
# 🛡️ Sécurité : on utilise `getattr()` pour éviter une erreur si l’utilisateur est anonyme (non connecté).

# ---------------------------------------------------------------------
# 🔧 Fonction contextuelle
# ---------------------------------------------------------------------
def user_roles(request):
    """
    🔄 Injecte dynamiquement les rôles de l'utilisateur dans le contexte HTML.

    Retourne un dictionnaire avec :
        - is_client : booléen, True si l'utilisateur est un client
        - is_contractor : booléen, True si l'utilisateur est un entrepreneur

    Ces valeurs seront utilisables dans tous les fichiers HTML sans appel explicite depuis les vues.
    """
    user = request.user  # 🔍 Récupère l’utilisateur connecté (AnonymousUser si non connecté)

    return {
        'is_client': getattr(user, 'is_client', False),         # ✅ True si client, sinon False
        'is_contractor': getattr(user, 'is_contractor', False)  # ✅ True si entrepreneur, sinon False
    }
