# 📁 Fichier : accounts/permissions.py
# 🔒 Ce fichier contient des classes de permissions personnalisées qui permettent
# de restreindre l’accès à certaines vues Django selon le rôle de l’utilisateur.
# Par exemple, on veut que certaines pages ne soient accessibles qu’aux clients,
# et d’autres qu’aux entrepreneurs. Ce système est important pour offrir
# une expérience sécurisée et cohérente pour chaque type d’utilisateur.

# 📦 On importe la base nécessaire pour créer des permissions
from django.contrib.auth.decorators import user_passes_test  # ✅ Outil natif Django pour créer des décorateurs conditionnels

# ---------------------------------------------------------------------
# 🎯 Décorateur : uniquement pour les utilisateurs qui sont des entrepreneurs
# Ce décorateur peut être utilisé au-dessus d’une vue pour dire :
# "Cette page ne doit être visible que si l’utilisateur est connecté ET est un entrepreneur."
# ---------------------------------------------------------------------
def contractor_required(view_func):
    """
    Décorateur personnalisé à appliquer sur une vue.
    Il permet de s'assurer que l'utilisateur est authentifié
    ET qu’il a le rôle 'entrepreneur' (is_contractor = True).
    Si ce n’est pas le cas, il est redirigé vers la page de connexion.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_contractor,  # 🧠 Condition à respecter
        login_url='/login/'                                # 🔁 Redirection si la condition échoue
    )
    return actual_decorator(view_func)  # 🔄 On retourne la vue modifiée par le décorateur


# ---------------------------------------------------------------------
# 🎯 Décorateur : uniquement pour les utilisateurs qui sont des clients
# Ce décorateur permet de restreindre certaines vues HTML aux clients.
# Exemple typique : le dashboard client, ou la page pour publier un projet.
# ---------------------------------------------------------------------
def client_required(view_func):
    """
    Décorateur personnalisé pour s'assurer que l'utilisateur connecté est un client.
    Il vérifie que l'utilisateur est authentifié ET qu’il a le rôle 'client' (is_client = True).
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_client,  # ✅ Condition de permission
        login_url='/login/'                            # 🔁 Redirection vers la connexion si la vérification échoue
    )
    return actual_decorator(view_func)


# ---------------------------------------------------------------------
# 🎯 Décorateur : accepte les clients OU les entrepreneurs
# Ce cas est utile pour des vues partagées, par exemple la modification du profil utilisateur,
# ou l’accès à une messagerie commune, où les deux rôles peuvent avoir un accès légitime.
# ---------------------------------------------------------------------
def client_or_contractor_required(view_func):
    """
    Ce décorateur est plus flexible : il accepte les utilisateurs connectés
    qui sont soit clients, soit entrepreneurs (ou les deux).
    Cela est utile pour des sections partagées entre les deux rôles.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_client or u.is_contractor),  # 🧩 L’un OU l’autre
        login_url='/login/'
    )
    return actual_decorator(view_func)


# ---------------------------------------------------------------------
# 🔄 NOTE POUR TRANSITION FUTURE — API & Django REST Framework
# Ce fichier contient uniquement des décorateurs de permissions pour les vues HTML classiques (ex. : @client_required).
# Une fois que la version classique (HTML) de la plateforme sera terminée, testée et fonctionnelle,
# la prochaine étape sera de migrer progressivement certaines vues vers des APIs REST sécurisées.
#
# ➤ Lors de cette transition, ce fichier devra être complété ou divisé en deux :
#     1. Garder les décorateurs HTML existants ici pour les vues Django classiques (/admin, pages internes…).
#     2. Ajouter un nouveau bloc (ou un fichier `rest_permissions.py`) contenant des classes héritant de BasePermission,
#        par exemple :
#            - class IsClient(BasePermission): ...
#            - class IsContractor(BasePermission): ...
#        Ces classes seront utilisées dans les views DRF (APIView, ViewSet, etc.)
#
# Ces permissions REST seront nécessaires pour sécuriser les endpoints des dashboards API,
# les projets, les profils, les paiements, etc., selon le rôle utilisateur et le token JWT associé.
