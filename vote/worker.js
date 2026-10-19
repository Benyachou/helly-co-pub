// Service de vote pour la page des versions Helly-Co.
//   GET  /resultats           -> { "v10": 3, "v11": 5, ... }
//   POST /vote {appareil, version}
// Chaque appareil a un identifiant aléatoire (gardé dans son navigateur) :
// un seul vote par appareil, qu'il peut changer.
const VERSIONS = ['v10', 'v11', 'v12'];
const ORIGINE = 'https://benyachou.github.io';

const entetes = {
  'Access-Control-Allow-Origin': ORIGINE,
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Content-Type': 'application/json',
};
const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: entetes });

async function compter(env) {
  const totaux = Object.fromEntries(VERSIONS.map(v => [v, 0]));
  let cursor;
  do {
    const page = await env.VOTES.list({ prefix: 'vote:', cursor });
    for (const k of page.keys) {
      const v = k.metadata && k.metadata.version;
      if (v in totaux) totaux[v]++;
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  return totaux;
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (req.method === 'OPTIONS') return new Response(null, { headers: entetes });
    if (req.method === 'GET' && url.pathname === '/resultats') return json(await compter(env));
    if (req.method === 'POST' && url.pathname === '/vote') {
      let corps;
      try { corps = await req.json(); } catch { return json({ erreur: 'Requête invalide.' }, 400); }
      const { appareil, version } = corps || {};
      if (!VERSIONS.includes(version)) return json({ erreur: 'Version inconnue.' }, 400);
      if (typeof appareil !== 'string' || !/^[a-z0-9-]{16,64}$/.test(appareil)) return json({ erreur: 'Appareil invalide.' }, 400);
      await env.VOTES.put(`vote:${appareil}`, version, { metadata: { version } });
      return json(await compter(env));
    }
    return json({ erreur: 'Introuvable.' }, 404);
  },
};
