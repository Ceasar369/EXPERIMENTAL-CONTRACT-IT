# core/urls.py
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.index, name='index'),  # Landing page publique (sections hero, catégories, etc.)
    
    # --- Pages "For Clients"
    path('how-to-hire/', views.how_to_hire, name='how_to_hire'),  # Guide pour les clients : comment embaucher
    path('talent-marketplace/', views.talent_marketplace, name='talent_marketplace'),  # Liste des talents
    path('project-catalog/', views.project_catalog, name='project_catalog'),  # Catalogue de projets inspirants

    # --- Pages "For Entrepreneurs"
    path('how-to-find-work/', views.how_to_find_work, name='how_to_find_work'),  # Aide pour les entrepreneurs

    # --- Pages "Support"
    path('help/', views.help_support, name='help'),  # Centre d’aide / FAQ
    path('contact/', views.contact, name='contact'),  # Page de contact
    path('trust-safety/', views.trust_safety, name='trust_safety'),  # Page sur la sécurité et la confiance

    # --- Pages "Company"
    path('about/', views.about, name='about'),  # À propos de Contract-it
    path('terms/', views.terms, name='terms'),  # Conditions d'utilisation
    path('privacy/', views.privacy, name='privacy'),  # Politique de confidentialité
    path('cookies/', views.cookies, name='cookies'),  # Politique sur les cookies
    path('accessibility/', views.accessibility, name='accessibility'),  # Accessibilité du site
    
    # 🔗 Routes vers les pages login / signup    
    path('signup/', views.signup, name='signup'),
    path("login/", views.login_view, name="login"), 

    # --- Pages "Mon Espace Entrepreneur"
    path('dashboard/contractor/', views.contractor_dashboard, name='contractor_dashboard'),  # 🔐 Page sécurisée
]
