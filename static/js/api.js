async function getFromAPI(path, callback, params = new URLSearchParams()) {
    try {
        const response = await fetch(`${path}?${params}`)
        if (!checkResponse(response)) throw new Error("Could not fetch response from API");
        callback(await response.json());
    } catch (e) {
        console.log(e)
    }
}

function checkResponse(response) {
    return response && response.status === 200;
}

// Fonction pour formater la date correctement (ISO sans 'Z')
function formatDate(dateString) {
    if (!dateString) return ""; // Éviter les erreurs si l'entrée est vide
    const date = new Date(dateString); // Convertir en objet Date
    return date.toISOString().slice(0, -1); // Enlever le 'Z' pour rester en UTC
}
function parseISODate(isoString) {
    if (!isoString) return "";
    const date = new Date(isoString);
    return date.toLocaleString(); // Format selon la locale de l'utilisateur
}
