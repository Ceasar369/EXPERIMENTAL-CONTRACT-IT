//core/static/core/js/logout.js


// 🔁 Fonction appelée lors de la déconnexion d’un utilisateur
function logout() {
    // 🔐 Supprime le token d’accès stocké dans le navigateur (utilisé pour les appels API sécurisés)
    localStorage.removeItem('access_token');
  
    // ♻️ Supprime également le refresh token qui sert à renouveler le token d'accès
    localStorage.removeItem('refresh_token');
  
    // 🔄 Redirige immédiatement l'utilisateur vers la page de login
    window.location.href = '/login/';
  }
  