// core/static/core/js/submit_project.js

// 🧾 Script pour gérer la soumission sécurisée du formulaire de création de projet
// Utilise secureFetch.js pour envoyer les données avec le token JWT

document.addEventListener("DOMContentLoaded", () => {
    // 🔍 On sélectionne les éléments du DOM
    const form = document.getElementById("project-form");
    const successMsg = document.getElementById("success-message");
    const errorMsg = document.getElementById("error-message");

    // 🔁 Écoute la soumission du formulaire
    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // ❌ Empêche le rechargement de la page

        // 🧾 Construction de l’objet projet à partir des champs
        const data = {
            title: form.title.value,
            description: form.description.value,
            budget: form.budget.value,
            deadline: form.deadline.value,
            location: form.location.value,
            category: form.category.value,
            ai_drafted: form.ai_drafted.value === "true"
        };

        try {
            // 🔐 Envoie sécurisé via JWT avec secureFetch.js
            const response = await secureFetch("/api/projects/", {
                method: "POST",
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                // ✅ Message de confirmation (peut rester visible si on veut tester)
                successMsg.style.display = "block";
                errorMsg.style.display = "none";

                // 🧹 Réinitialise le formulaire
                form.reset();

                // ⏳ Petite pause avant redirection
                setTimeout(() => {
                    // 🚀 Redirige vers le dashboard client après 1.5 seconde
                    window.location.href = "/dashboard/client/";
                }, 1500);
            } else {
                // ❌ Affiche l’erreur retournée par l’API
                successMsg.style.display = "none";
                errorMsg.style.display = "block";
                errorMsg.textContent = result.detail || "❌ Error publishing project.";
            }

        } catch (error) {
            // ⚠️ Si exception réseau ou autre
            successMsg.style.display = "none";
            errorMsg.style.display = "block";
            errorMsg.textContent = `❌ ${error.message}`;
        }
    });
});
