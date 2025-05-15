//core/static/core/js/secureFetch.js



// 🔐 Fonction utilitaire pour faire une requête API sécurisée avec gestion automatique du token JWT
async function secureFetch(url, options = {}) {
    // 🔑 On récupère les tokens stockés localement
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
  
    // 📨 On prépare les en-têtes (headers) de la requête avec le access token
    options.headers = {
      ...options.headers,  // préserve les autres headers éventuels
      Authorization: 'Bearer ' + accessToken,  // en-tête d’authentification
      'Content-Type': 'application/json'       // format d’envoi
    };
  
    // 📤 On envoie la requête initiale à l’API
    let response = await fetch(url, options);
  
    // ❌ Si le access token est expiré → on reçoit une erreur 401
    if (response.status === 401) {
      // 🔁 On tente de rafraîchir le token avec le refresh_token
      const refreshResponse = await fetch('/api/accounts/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken })
      });
  
      // ✅ Si le refresh fonctionne : on remplace l’ancien access token par le nouveau
      if (refreshResponse.ok) {
        const data = await refreshResponse.json();
        localStorage.setItem('access_token', data.access);  // on sauvegarde le nouveau token
  
        // 📤 On met à jour l’en-tête d’autorisation avec le nouveau token
        options.headers.Authorization = 'Bearer ' + data.access;
  
        // 🔁 Et on relance la requête initiale avec le nouveau token valide
        response = await fetch(url, options);
      } else {
        // 🚫 Si le refresh échoue (refresh expiré ou invalide), on redirige vers la page de login
        window.location.href = '/login/';
        return;
      }
    }
  
    // 📦 On retourne la réponse finale (soit d’origine, soit relancée)
    return response;
  }
  