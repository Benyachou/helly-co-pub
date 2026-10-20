// Service de vote pour la page des versions Helly-Co.
//   GET  /resultats           -> { "v10": 3, "v11": 5, ... }
//   POST /vote {appareil, version}
// Chaque appareil a un identifiant aléatoire (gardé dans son navigateur) :
// un seul vote par appareil, qu'il peut changer.
const VERSIONS = ['v10', 'v11', 'v12', 'v13', 'v15'];
const ORIGINE = 'https://benyachou.github.io';

const entetes = {
  'Access-Control-Allow-Origin': ORIGINE,
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Content-Type': 'application/json',
};
const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: entetes });

// Les totaux sont tenus dans une seule clé, mise à jour à chaque vote :
// le résultat est ainsi visible tout de suite (la liste des clés, elle, met jusqu'à une minute).
async function totaux(env) {
  const t = (await env.VOTES.get('totaux', 'json')) || {};
  return Object.fromEntries(VERSIONS.map(v => [v, Math.max(0, t[v] || 0)]));
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (req.method === 'OPTIONS') return new Response(null, { headers: entetes });
    if (req.method === 'GET' && url.pathname === '/resultats') return json(await totaux(env));
    if (req.method === 'POST' && url.pathname === '/vote') {
      let corps;
      try { corps = await req.json(); } catch { return json({ erreur: 'Requête invalide.' }, 400); }
      const { appareil, version } = corps || {};
      if (!VERSIONS.includes(version)) return json({ erreur: 'Version inconnue.' }, 400);
      if (typeof appareil !== 'string' || !/^[a-z0-9-]{16,64}$/.test(appareil)) return json({ erreur: 'Appareil invalide.' }, 400);
      const cle = `vote:${appareil}`;
      const avant = await env.VOTES.get(cle);
      const t = await totaux(env);
      if (avant === version) return json(t);
      if (avant in t) t[avant] = Math.max(0, t[avant] - 1);
      t[version]++;
      await env.VOTES.put(cle, version);
      await env.VOTES.put('totaux', JSON.stringify(t));
      return json(t);
    }
    return json({ erreur: 'Introuvable.' }, 404);
  },
};
