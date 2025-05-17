# 📁 Fichier : contractit_backend/urls.py
# 🎯 Ce fichier définit toutes les URL accessibles depuis le navigateur ou les requêtes API.
# Il gère :
#    - les redirections automatiques vers la langue préférée
#    - les routes de l’API REST (non traduisibles)
#    - les routes HTML traduites (via `i18n_patterns`)
#    - les outils de changement de langue (`/i18n/`)

# ---------------------------------------------------------------------
# 📦 IMPORTS DJANGO
# ---------------------------------------------------------------------
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns  # 🔄 Pour internationalisation des routes HTML
from django.shortcuts import redirect             # 🔁 Pour rediriger /
from django.utils import translation
from django.conf.urls.static import static  # ✅ Nécessaire pour servir les fichiers médias en mode DEBUG


from contractit_backend import settings              # 🌐 Pour détecter la langue préférée

# ---------------------------------------------------------------------
# 🌍 FONCTION : redirige automatiquement `/` vers `/fr/` ou `/en/`
# ---------------------------------------------------------------------
def redirect_to_language_root(request):
    """
    Détecte la langue préférée de l'utilisateur (à partir des cookies ou headers HTTP)
    et le redirige automatiquement vers le chemin de langue correspondant.
    Ex : si le navigateur est en français → redirige `/` vers `/fr/`
    """
    lang = translation.get_language_from_request(request, check_path=False)
    return redirect(f'/{lang}/')

# ---------------------------------------------------------------------
# 🔗 ROUTES GLOBALES — NON traduisibles (API REST, langue)
# ---------------------------------------------------------------------
urlpatterns = [
    # 🔁 Redirection automatique de `/` vers `/fr/` ou `/en/`
    path('', redirect_to_language_root, name='redirect-to-lang'),

    # 🌐 Endpoint pour gérer les changements de langue (formulaires ou JS)
    path('i18n/', include('django.conf.urls.i18n')),

    # 🔧 Endpoints de l’API (non traduits, fixes)
    path('api/accounts/', include('accounts.urls')),
    path('api/projects/', include('projects.urls')),
]

# ---------------------------------------------------------------------
# 🔗 ROUTES HTML — Traduisibles (prefixées par /fr/, /en/, etc.)
# ---------------------------------------------------------------------
urlpatterns += i18n_patterns(
    # 🏠 Pages publiques (accueil, à propos, etc.)
    path('', include('core.urls')),

    # 🛠️ Interface d’administration Django (avec /fr/admin/)
    path('admin/', admin.site.urls),

    # 🧱 Pages HTML liées aux projets (création, liste…)
    path('projects/', include('projects.urls')),

    # 👤 Pages HTML liées aux comptes (connexion, inscription…)
    path('accounts/', include('accounts.urls')),

    # 📩 Pages HTML liées aux soumissions (bids)
    path('bids/', include('bids.urls')),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)