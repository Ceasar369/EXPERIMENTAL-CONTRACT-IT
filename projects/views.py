# ---------------------------------------------------------------------
# 📁 Fichier : projects/views.py
#
# 🎯 Vues HTML classiques de l’application `projects` (CONTRACT-IT)
#
# Ce fichier regroupe les vues nécessaires à :
#    - la création d’un projet (client),
#    - l’affichage de projets publics (entrepreneurs),
#    - le suivi personnel (projets publiés ou attribués),
#    - la visualisation détaillée d’un projet,
#    - l’édition d’un projet (si pas encore attribué).
#
# Chaque vue retourne un template HTML via `render()`.
# Ce fichier ne contient aucune logique d’API, JWT ou DRF.
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# 📦 IMPORTS DJANGO
# ---------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# ---------------------------------------------------------------------
# 📦 IMPORTS INTERNES
# ---------------------------------------------------------------------
from .models import Project, Milestone
from bids.models import Bid  # Pour afficher les soumissions
from accounts.models import CustomUser


# ---------------------------------------------------------------------
# 1. 📝 Créer un nouveau projet (Client)
# ---------------------------------------------------------------------
from django.contrib import messages  # Pour afficher des messages de succès ou d'erreur

@login_required
def create_project_page(request):
    """
    Vue permettant à un client de publier un projet avec jalons.
    - En GET : affiche le formulaire de création.
    - En POST : enregistre le projet + jalons en base de données.

    🔐 Seuls les utilisateurs ayant le rôle `is_client` peuvent accéder à cette vue.
    """

    user = request.user  # Récupère l'utilisateur connecté

    # 🔒 Si ce n'est pas un client, on redirige vers la page d'accueil
    if not user.is_client:
        return redirect("index")

    # -----------------------------------------------------------------
    # 🔁 CAS POST : l'utilisateur soumet le formulaire
    # -----------------------------------------------------------------
    if request.method == "POST":
        # ✅ 1. On récupère tous les champs principaux du formulaire (partie 1)
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        location = request.POST.get("location")
        budget = float(request.POST.get("budget"))
        deadline = request.POST.get("deadline")
        is_public = request.POST.get("is_public") == "True"
        ai_drafted = request.POST.get("ai_drafted") == "True"

        # ✅ 2. On crée le projet dans la base de données
        project = Project.objects.create(
            client=user,
            title=title,
            description=description,
            category=category,
            location=location,
            budget=budget,
            deadline=deadline,
            is_public=is_public,
            ai_drafted=ai_drafted
        )

        # ✅ 3. On récupère les listes de jalons soumises (partie 2)
        titles = request.POST.getlist("milestone_title[]")
        due_dates = request.POST.getlist("milestone_due[]")
        amounts = request.POST.getlist("milestone_amount[]")

        # 🧮 On prépare à vérifier la somme des montants
        total_milestone_budget = 0

        # 🧱 Pour chaque ligne de jalon, on crée un objet Milestone associé
        for i in range(len(titles)):
            amount = float(amounts[i])
            total_milestone_budget += amount

            # 🧱 Création du jalon dans la base de données (lié au projet principal)
            Milestone.objects.create(
                project=project,
                title=titles[i],
                due_date=due_dates[i],
                amount=amount
            )

        # ✅ 4. Vérifie que la somme des montants == budget total
        if round(total_milestone_budget, 2) != round(budget, 2):
            project.delete()  # 🔁 On supprime le projet pour éviter d'enregistrer une structure incohérente
            messages.error(request, "⚠️ La somme des jalons ne correspond pas au budget total.")
            return redirect("create-project")

        # ✅ 5. Tout est bon → on redirige avec un message de confirmation
        messages.success(request, "🎉 Projet créé avec succès !")
        return redirect("my_projects")

    # -----------------------------------------------------------------
    # 👁️ CAS GET : afficher le formulaire vide
    # -----------------------------------------------------------------
    return render(request, 'projects/create_project.html')



# ---------------------------------------------------------------------
# 2. 🔍 Liste des projets disponibles (Entrepreneur)
# ---------------------------------------------------------------------
@login_required
def find_jobs_view(request):
    """
    Affiche la liste des projets publics et actifs à destination des entrepreneurs.

    🔍 Permet de filtrer selon :
        - le budget minimum et maximum
        - la localisation
        - la catégorie de projet

    Les filtres sont transmis via GET dans l’URL (ex : ?budget_min=1000&category=Plomberie).
    """

    # 🔒 Restriction d’accès : seulement les utilisateurs entrepreneurs
    if not request.user.is_contractor:
        return redirect('index')

    # 🧱 Point de départ : projets publics et actifs
    projects = Project.objects.filter(is_public=True, status='active')

    # -----------------------------------------------------------------
    # ✅ Lecture des filtres transmis via GET (avec nettoyage)
    # -----------------------------------------------------------------

    budget_min = request.GET.get('budget_min')
    budget_max = request.GET.get('budget_max')
    location = request.GET.get('location', '').strip()
    category = request.GET.get('category', '').strip()

    # 🔎 Appliquer le filtre budget minimum
    if budget_min:
        try:
            min_val = float(budget_min)
            projects = projects.filter(budget__gte=min_val)
        except ValueError:
            pass  # Ignore en cas d’entrée non numérique

    # 🔎 Appliquer le filtre budget maximum
    if budget_max:
        try:
            max_val = float(budget_max)
            projects = projects.filter(budget__lte=max_val)
        except ValueError:
            pass

    # 🔎 Appliquer le filtre localisation (insensible à la casse)
    if location:
        projects = projects.filter(location__icontains=location)

    # 🔎 Appliquer le filtre catégorie (insensible à la casse)
    if category:
        projects = projects.filter(category__icontains=category)

    # ✅ Trier les projets les plus récents en premier
    projects = projects.order_by('-created_at')

    # 📤 Envoie les projets (filtrés ou non) à la page HTML
    return render(request, 'projects/project_list.html', {
        'projects': projects
    })



# ---------------------------------------------------------------------
# 3. 📄 Détail d’un projet (Client ou Entrepreneur)
# ---------------------------------------------------------------------
@login_required
def project_detail_page(request, project_id):
    """
    Affiche la page de détail d’un projet spécifique.
    Si l’utilisateur est entrepreneur, on vérifie s’il a déjà soumis une proposition.
    """
    project = get_object_or_404(Project, id=project_id)
    user = request.user

    # ⚠️ Vérifie si l’entrepreneur connecté a déjà soumis une proposition
    has_already_bid = False
    if user.is_contractor:
        # ✅ Vérifie si l’entrepreneur a déjà soumis une offre (pour désactiver le bouton « Soumettre »)
        has_already_bid = Bid.objects.filter(project=project, contractor=user).exists()

    # 📦 Récupère les jalons liés à ce projet
    milestones = Milestone.objects.filter(project=project).order_by('due_date')

    return render(request, 'projects/project_details.html', {
        'project': project,
        'has_already_bid': has_already_bid,
        'milestones': milestones,
    })


# ---------------------------------------------------------------------
# 4. 📋 Affiche tous les projets publiés par le client connecté
# ---------------------------------------------------------------------


@login_required
def my_projects_view(request):
    """
    Vue permettant à un client de consulter tous les projets qu’il a publiés,
    accompagnés du nombre de soumissions (bids) reçues pour chacun.

    🔐 Accessible uniquement aux utilisateurs ayant `is_client = True`.

    Retourne un tableau contenant :
      - chaque projet du client
      - le nombre de soumissions associées
    """

    user = request.user

    # 🔒 Vérifie que l'utilisateur est bien un client
    if not user.is_client:
        return redirect("index")  # Redirige les non-clients

    # 🔍 Récupère tous les projets créés par ce client
    projects = Project.objects.filter(client=user).order_by('-created_at')

    # 🧮 Pour chaque projet, compte combien de bids ont été reçues
    projects_with_bids = []

    for project in projects:
        bids_count = Bid.objects.filter(project=project).count()
        projects_with_bids.append({
            'project': project,
            'bids_count': bids_count
        })

    # 📤 Envoie les données au template
    return render(request, 'projects/my_projects.html', {
        'projects_with_bids': projects_with_bids
    })


# ---------------------------------------------------------------------
# 5. ✏️ Modifier un projet existant (Client uniquement)
# ---------------------------------------------------------------------
@login_required
def edit_project_view(request, project_id):
    """
    Permet au client de modifier un projet qu’il a déjà publié.
    Tous les champs du projet sont modifiables, ainsi que les jalons existants.

    ⚠️ Cette vue ne permet pas d’ajouter ou supprimer des jalons (à faire plus tard).
    """

    # 🔍 Récupère le projet ou affiche une 404 s’il n’existe pas
    project = get_object_or_404(Project, id=project_id)

    # 🔒 Vérifie que l’utilisateur connecté est bien le client propriétaire
    if project.client != request.user:
        return redirect("index")  # ❌ Refus d'accès

    # 🔍 Récupère tous les jalons associés à ce projet
    milestones = project.milestones.all()

    # ✅ Si on soumet le formulaire en POST
    if request.method == "POST":
        # 📝 Mise à jour des champs du projet
        project.title = request.POST.get("title", "").strip()
        project.description = request.POST.get("description", "").strip()
        project.category = request.POST.get("category", "").strip()
        project.location = request.POST.get("location", "").strip()
        # 💰 On convertit le budget en float pour l’enregistrer correctement (champ DecimalField)
        project.budget = float(request.POST.get("budget", "").strip())
        project.deadline = request.POST.get("deadline", "").strip()
        project.save()

        # 🔁 Mise à jour des jalons (déjà existants uniquement)
        for i, milestone in enumerate(milestones, start=1):
            milestone.title = request.POST.get(f"milestone_title_{i}", milestone.title)
            milestone.amount = request.POST.get(f"milestone_amount_{i}", milestone.amount)
            milestone.due_date = request.POST.get(f"milestone_due_{i}", milestone.due_date)
            milestone.save()

        # ✅ Redirige vers la page "My Projects" après sauvegarde
        return redirect("my_projects")

    # 🧾 Affiche le formulaire HTML avec les valeurs préremplies
    return render(request, "projects/edit_project.html", {
        "project": project,
        "milestones": milestones,
    })


# ---------------------------------------------------------------------
# 6. 🧰 Liste des projets attribués à un entrepreneur
# ---------------------------------------------------------------------
@login_required
def awarded_projects_view(request):
    """
    Affiche tous les projets où l'utilisateur connecté a été sélectionné comme entrepreneur.

    🔐 Cette vue est réservée aux utilisateurs ayant `is_contractor = True`.

    Retourne un template HTML avec les projets attribués à cet utilisateur.
    """

    # 🔒 Refuse l’accès aux utilisateurs qui ne sont pas des entrepreneurs
    if not request.user.is_contractor:
        return redirect('index')

    # 🔍 Récupère les projets attribués (contractor = user connecté)
    awarded_projects = Project.objects.filter(contractor=request.user).order_by('-created_at')

    # 📤 Envoie au template avec le nom de variable awarded_projects
    return render(request, 'projects/awarded_projects.html', {
        'awarded_projects': awarded_projects
    })
