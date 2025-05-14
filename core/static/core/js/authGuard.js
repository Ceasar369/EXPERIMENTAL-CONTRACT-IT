// 🔐 Vérifie si l'utilisateur est connecté (access_token présent)
// Si ce n'est pas le cas → redirige vers /login/
function enforceAuthentication() {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      // ❌ Pas de token → redirection vers page de connexion
      window.location.href = '/login/';
    }
  }