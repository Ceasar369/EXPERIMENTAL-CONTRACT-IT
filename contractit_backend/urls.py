# contractit_backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from django.utils import translation

# 🌐 Fonction de redirection automatique selon la langue préférée de l’utilisateur
def redirect_to_language_root(request):
    lang = translation.get_language_from_request(request, check_path=False)
    return redirect(f'/{lang}/')  # ex: /fr/ ou /en/

# 🔗 Routes NON traduisibles (API REST, admin technique, etc.)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # pour le changement de langue
    path('', redirect_to_language_root, name='redirect-to-lang'),  # redirige automatiquement / vers /en/ ou /fr/

    # ✅ API REST (doit rester hors de i18n_patterns)
    path('api/accounts/', include('accounts.urls')),
    path('api/projects/', include('projects.urls')),
]

# 🔗 Routes traduisibles (affichées dans l’interface utilisateur HTML)
urlpatterns += i18n_patterns(
    path('', include('core.urls')),                # pages publiques (index, login, signup, etc.)
    path('admin/', admin.site.urls),               # interface d’administration Django
    path('projects/', include('projects.urls')),   # vues HTML liées aux projets
    path('accounts/', include('accounts.urls')),   # si tu veux des vues HTML comptes (optionnel)
    path('bids/', include('bids.urls')),
)
