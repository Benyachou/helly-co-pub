"""Fabrique les trois variantes de 5 minutes à partir de v9-helly-co-5min.html.

    python fabriquer.py   -> v10-helly-co-cinema.html, v11-helly-co-bilingue.html, v12-helly-co-lumiere.html

Toutes les variantes remplacent les photos de femmes non adaptées à la clientèle.
"""
from pathlib import Path

ICI = Path(__file__).resolve().parent
SOURCE = (ICI / 'v9-helly-co-5min.html').read_text(encoding='utf-8')
REPERE_MOTEUR = '// ——— Moteur : une seule fonction render(t), déterministe ———'


def rep(s, a, b):
    assert a in s, a[:70]
    return s.replace(a, b)


def base():
    s = SOURCE
    for a, b in [("'femme-tel'", "'homme-tel'"), ("'copieuse-femme'", "'atelier-impression'"),
                 ("'appel-video'", "'appel-homme'"), ("'duo-documents'", "'deux-hommes-documents'"),
                 ("'famille'", "'famille-musulmane'")]:
        s = rep(s, a, b)
    # point d'accroche commun pour les réglages propres à chaque variante
    s = rep(s, "    if (cale) s._decoupes.forEach(svg => decoupe(svg, lt));",
            "    if (cale) s._decoupes.forEach(svg => decoupe(svg, lt));\n"
            "    if (typeof apresScene === 'function') apresScene(s, lt);")
    return s


def avant_moteur(s, code):
    return rep(s, REPERE_MOTEUR, code + '\n' + REPERE_MOTEUR)


# ———————————————————————————— v10 : cinéma ————————————————————————————
def cinema():
    s = base()
    return rep(s, '<title>Helly-Co Services — boucle de 5 minutes</title>',
               '<title>Helly-Co Services — cinéma</title>')


# ———————————————————————————— v11 : bilingue ————————————————————————————
AR = {
    'Un seul comptoir.': 'كل الخدمات في مكان واحد.',
    'Ici, on s’occupe de :': 'هنا نهتم بـ:',
    'Un seul comptoir pour tout ça :': 'كل هذا في مكان واحد:',
    'Réparation de téléphone': 'إصلاح الهواتف',
    'Accessoires': 'الإكسسوارات',
    'Transfert d’argent': 'تحويل الأموال',
    'Transfert d’argent avec :': 'تحويل الأموال مع:',
    'Démarches administratives': 'الإجراءات الإدارية',
    'Bureautique': 'الطباعة والنسخ',
    'Réparé.': 'تم الإصلاح.',
    'Écran, batterie, prise de charge, caméra.': 'الشاشة، البطارية، منفذ الشحن، الكاميرا.',
    'Tous les téléphones, toutes les marques. Ici, en boutique.': 'جميع الهواتف وجميع الماركات، هنا في المحل.',
    'Écran.': 'الشاشة', 'Batterie.': 'البطارية', 'Prise de charge.': 'منفذ الشحن', 'Caméra.': 'الكاميرا',
    'Haut-parleur.': 'مكبر الصوت', 'Micro.': 'الميكروفون', 'Vitre arrière.': 'الزجاج الخلفي',
    'Toutes les marques.': 'جميع الماركات.',
    'Quel que soit votre téléphone, on regarde avec vous.': 'مهما كان هاتفك، نفحصه معك.',
    'Écran cassé ?': 'شاشة مكسورة؟', 'Batterie qui lâche ?': 'بطارية ضعيفة؟', 'Ne charge plus ?': 'لا يشحن؟',
    'Plus de son ?': 'لا يوجد صوت؟', 'On répare.': 'نصلحه.', 'Passez au comptoir.': 'تفضلوا عندنا.',
    'Avant': 'قبل', 'Après': 'بعد',
    'Écran remplacé, téléphone comme vous l’aimez.': 'شاشة جديدة، وهاتفك كما تحبه.',
    'Ouvert. Réparé. Refermé.': 'نفتحه، نصلحه، نغلقه.',
    'Le travail se fait ici, en boutique.': 'العمل يتم هنا في المحل.',
    'Sans téléphone, plus rien ne marche.': 'بدون هاتف، لا شيء يعمل.',
    'Ne restez pas sans. On le répare ici.': 'لا تبقوا بدونه، نصلحه هنا.',
    'Coques.': 'أغطية الهاتف', 'Coques et protections pour votre téléphone.': 'أغطية وواقيات لهاتفك.',
    'Chargé.': 'مشحون.', 'Chargeurs et câbles.': 'شواحن وكابلات.',
    'Câbles.': 'الكابلات', 'Le bon câble pour votre téléphone.': 'الكابل المناسب لهاتفك.',
    'Chargeurs.': 'الشواحن', 'Protections.': 'الواقيات', 'Recharges.': 'تعبئة الرصيد',
    'Prêt à repartir.': 'جاهز للانطلاق.',
    'Câbles, chargeurs, coques, protections et recharges.': 'كابلات، شواحن، أغطية، واقيات وتعبئة الرصيد.',
    'Reçu.': 'تم الاستلام.',
    'Western Union, MoneyGram, Ria. En espèces ou par carte.': 'ويسترن يونيون، موني غرام، ريا. نقدًا أو بالبطاقة.',
    'Au Maroc et partout dans le monde, en toute sécurité.': 'إلى المغرب وإلى كل أنحاء العالم، بأمان تام.',
    'À vos proches, où qu’ils soient.': 'إلى أحبائكم، أينما كانوا.',
    'Envoyez de l’argent à votre famille, en toute sécurité.': 'أرسلوا المال إلى عائلتكم بأمان.',
    'En espèces ou par carte.': 'نقدًا أو بالبطاقة.',
    'Au Maroc, en Afrique, en Europe et ailleurs.': 'إلى المغرب، إفريقيا، أوروبا وغيرها.',
    'Au Maroc ?': 'إلى المغرب؟', 'En Europe ?': 'إلى أوروبا؟', 'En Afrique ?': 'إلى إفريقيا؟',
    'Plus loin ?': 'أبعد من ذلك؟', 'On envoie.': 'نرسل.',
    'Western Union, MoneyGram, Ria.': 'ويسترن يونيون، موني غرام، ريا.',
    'Envoyé ici. Reçu là-bas.': 'يُرسل من هنا، ويُستلم هناك.',
    'Expliqué.': 'نشرح لكم.',
    'Préfecture, consulats, dossiers. En français, en arabe et en anglais.': 'المحافظة، القنصليات، الملفات. بالفرنسية والعربية والإنجليزية.',
    'Rendez-vous introuvable ?': 'لم تجدوا موعدًا؟', 'Formulaire en ligne ?': 'استمارة على الإنترنت؟',
    'Dossier à compléter ?': 'ملف لإكماله؟', 'On vous aide.': 'نساعدكم.',
    'Préfecture, consulats, démarches.': 'المحافظة، القنصليات، الإجراءات.',
    'Préfecture.': 'المحافظة', 'Consulats.': 'القنصليات', 'Rendez-vous.': 'المواعيد',
    'Formulaires.': 'الاستمارات', 'Dossiers.': 'الملفات',
    'Un formulaire à remplir ?': 'استمارة لملئها؟', 'On le remplit avec vous.': 'نملؤها معكم.',
    'Rempli. Signé.': 'مملوءة. موقّعة.', 'Préfecture, consulats, rendez-vous.': 'المحافظة، القنصليات، المواعيد.',
    'Pas à pas, avec vous.': 'خطوة بخطوة، معكم.',
    'En français, en arabe et en anglais.': 'بالفرنسية والعربية والإنجليزية.',
    'Impressions, photocopies et scans sur place.': 'طباعة، نسخ ومسح ضوئي في عين المكان.',
    'Impressions.': 'الطباعة', 'Photocopies.': 'النسخ', 'Scans.': 'المسح الضوئي',
    'Reliures.': 'التجليد', 'Plastifications.': 'التغليف',
    'Un document à imprimer ?': 'وثيقة للطباعة؟', 'Une photocopie ?': 'نسخة؟', 'Un scan ?': 'مسح ضوئي؟',
    'C’est ici.': 'عندنا.', 'Reliures et plastifications aussi.': 'والتجليد والتغليف أيضًا.',
    'Relié. Plastifié.': 'مجلّد. مغلّف.', 'Reliures et plastifications.': 'التجليد والتغليف.',
    'Écran noir ? Batterie à plat ?': 'شاشة سوداء؟ بطارية فارغة؟', 'On le répare ici.': 'نصلحه هنا.',
    'Nos horaires': 'أوقات العمل',
    'Lundi au jeudi, samedi': 'من الإثنين إلى الخميس، والسبت',
    '9h30 – 19h00, sans interruption': 'من 9:30 إلى 19:00 دون انقطاع',
    'Vendredi': 'الجمعة',
    '9h30 – 13h00 et 14h30 – 19h00': 'من 9:30 إلى 13:00 ومن 14:30 إلى 19:00',
}

CSS_BILINGUE = '''
/* ——— Bilingue : chaque message a sa traduction arabe ——— */
:root { --nuit: #23211F; }
.ar { display: block; text-align: left; font-family: "Segoe UI", Tahoma, Arial, sans-serif; unicode-bidi: plaintext; letter-spacing: 0; font-weight: 600; }
.gros .ar > span { font-size: .42em; color: var(--vert); line-height: 1.3; }
.gros.t300 { font-size: 220px; } .gros.t200 { font-size: 160px; } .gros.t140 { font-size: 120px; }
.legende p { font-size: 40px; }
.legende p.ar { margin-top: 4px; color: #E4E5E8; font-weight: 500; }
.legende b .ar-i, .etiquette .ar-i, .etiq .ar-i { font-family: "Segoe UI", Tahoma, Arial, sans-serif; margin-left: 16px; }
.rafale span small.ar { font-size: 90px; margin-top: 10px; color: #C4C6CA; }
.clair .rafale span small.ar { color: #6B6C70; }
.questions { height: 260px; }
.questions span small.ar { font-size: 72px; margin-top: 6px; }
.carte .ligne .ar > span { font-size: .5em; }
.carte .petit .ar { margin-top: 8px; }
.carte .liste li { font-size: 66px; }
.carte .liste li .ar-i { font-family: "Segoe UI", Tahoma, Arial, sans-serif; font-weight: 600; font-size: .7em; margin-left: 28px; opacity: .75; }
.accroche .ar { margin-top: 10px; color: var(--vert); }
.horaires { font-size: 46px; }
.horaires .ar { font-size: 34px; color: var(--vert); font-weight: 500; }
.horaires h2 .ar { display: inline; margin-left: 16px; font-size: 34px; }
'''

JS_BILINGUE = '''
// ——— Bilingue : on ajoute la traduction arabe sous chaque message ———
const AR = __AR__;
const ar = t => AR[t.replace(/\\s+/g, ' ').trim()];
function traduire() {
  const bloc = (tag, a, cls = 'ar') => `<${tag} class="${cls}" dir="rtl">${a}</${tag}>`;
  for (const g of document.querySelectorAll('.gros, .carte .ligne')) {
    const lignes = [...g.querySelectorAll('.l')];
    const a = ar(lignes.map(l => l.textContent).join(' '));
    if (!a) continue;
    const at = Math.max(...lignes.map(l => parseFloat(l.dataset.at))) + 0.35;
    g.insertAdjacentHTML('beforeend', `<span class="l ar" data-at="${at}"><span>${a}</span></span>`);
  }
  for (const p of document.querySelectorAll('.legende p')) { const a = ar(p.textContent); if (a) p.insertAdjacentHTML('afterend', bloc('p', a)); }
  for (const e of document.querySelectorAll('.legende b, .etiquette, .etiq, .carte .liste li')) {
    const a = ar(e.textContent); if (a) e.insertAdjacentHTML('beforeend', bloc('span', a, 'ar-i'));
  }
  for (const e of document.querySelectorAll('.rafale span, .questions span')) {
    const a = ar(e.textContent); if (a) e.insertAdjacentHTML('beforeend', bloc('small', a));
  }
  for (const e of document.querySelectorAll('.carte .petit, .accroche, .mur .petit, .mur .titre-mur')) {
    const a = ar(e.textContent); if (a) e.insertAdjacentHTML('beforeend', bloc('span', a));
  }
  for (const h of document.querySelectorAll('.horaires h2')) h.insertAdjacentHTML('beforeend', bloc('span', ar(h.textContent)));
  for (const d of document.querySelectorAll('.horaires > div')) {
    const jour = d.querySelector('span').textContent, heures = d.textContent.replace(jour, '');
    d.insertAdjacentHTML('beforeend', bloc('span', `${ar(jour)} : ${ar(heures)}`));
  }
}
traduire();
'''


def bilingue():
    import json
    s = base()
    s = rep(s, '<title>Helly-Co Services — boucle de 5 minutes</title>', '<title>Helly-Co Services — bilingue</title>')
    s = rep(s, '</style>', CSS_BILINGUE + '</style>')
    # la carte des langues est déjà trilingue : on la garde telle quelle
    return avant_moteur(s, JS_BILINGUE.replace('__AR__', json.dumps(AR, ensure_ascii=False, indent=0)))


# ———————————————————————————— v12 : lumière ————————————————————————————
CSS_LUMIERE = '''
/* ——— Lumière : fond clair, photos posées dans un cadre arrondi ——— */
#stage, .scene, .scene.clair { background: var(--papier); color: var(--encre); }
.scene.verte { background: var(--vert); }
.cadre { position: absolute; overflow: hidden; background: #DADCDF; }
.voile { display: none; }
.gros { left: 110px; bottom: 320px; width: 680px; color: var(--encre); }
.gros.t300 { font-size: 128px; } .gros.t200 { font-size: 108px; } .gros.t140 { font-size: 80px; }
.legende { left: 110px; bottom: 120px; max-width: 640px; }
.legende b { color: var(--vert-fonce); }
.legende p { color: var(--encre); font-size: 40px; }
.etiq { top: 30px; background: var(--vert); }
.etiquette, .clair .etiquette { color: var(--vert-fonce); }
.rafale span:last-child, .clair .rafale span:last-child { color: var(--vert-fonce); }
.langues .ar { color: var(--vert-fonce); }
.langues .petit, .accroche { color: #6B6C70; }
.horaires span { color: #6B6C70; }
.horaires h2 { color: var(--vert-fonce); }
.horaires div + div { border-top-color: #DADCDF; }
.nuit .carte .liste li::before { background: var(--vert-fonce); }
.plaques { gap: 12px; }
.plaques span { height: 70px; padding: 0 18px; box-shadow: 0 6px 18px rgba(0,0,0,.10); }
.plaques img { height: 38px; } .plaques .ria img { height: 42px; }
.cadre .bulle.g { left: 40px !important; top: 30px !important; }
.cadre .bulle.d { right: 40px !important; top: 30px !important; left: auto !important; }
'''

JS_LUMIERE = '''
// ——— Lumière : les photos se rangent dans un cadre à droite ———
const CIBLE = { l: 820, t: 70, r: 70, b: 70 };
for (const s of document.querySelectorAll('.scene')) {
  s.classList.add('clair');
  if (s.classList.contains('nuit')) { s.classList.remove('nuit'); s.classList.add('verte'); }
  const contenu = s.querySelectorAll(':scope > .plein, :scope > .moitie, :scope > .voile, :scope > .bulle, :scope > .etiq');
  if (!contenu.length) continue;
  const cadre = document.createElement('div');
  cadre.className = 'cadre';
  s.prepend(cadre);
  contenu.forEach(e => cadre.appendChild(e));
  const etiqs = cadre.querySelectorAll('.etiq');
  if (etiqs[0]) etiqs[0].style.left = '30px';
  if (etiqs[1]) etiqs[1].style.left = 'calc(50% + 30px)';
  s._cadre = cadre;
  // avec un mot découpé, la photo commence en plein écran et se range ensuite
  s._rangement = s.querySelector('.decoupe') ? 3.5 : -1;
}
const lerp = (a, b, p) => a + (b - a) * p;
function apresScene(s, lt) {
  if (!s._cadre) return;
  const p = s._rangement < 0 ? 1 : douce((lt - s._rangement) / 1.1);
  const c = s._cadre.style;
  c.left = `${lerp(0, CIBLE.l, p)}px`; c.top = `${lerp(0, CIBLE.t, p)}px`;
  c.right = `${lerp(0, CIBLE.r, p)}px`; c.bottom = `${lerp(0, CIBLE.b, p)}px`;
  c.borderRadius = `${28 * p}px`;
}
'''


def lumiere():
    s = base()
    s = rep(s, '<title>Helly-Co Services — boucle de 5 minutes</title>', '<title>Helly-Co Services — lumière</title>')
    s = rep(s, '</style>', CSS_LUMIERE + '</style>')
    # logos et mots découpés sur fond clair
    s = rep(s, 'src="assets/mark-blanc.png" alt=""><img class="pour-clair"', 'src="assets/mark-gris.png" alt=""><img class="pour-clair"')
    s = rep(s, "<img ${anime ? 'class=\"i-blanc\"' : ''} src=\"assets/mark-blanc.png\"", "<img ${anime ? 'class=\"i-blanc\"' : ''} src=\"assets/mark-gris.png\"")
    s = rep(s, '<img class="mot-logo" src="assets/texte-sur-fonce.png"', '<img class="mot-logo" src="assets/texte-sur-clair.png"')
    s = rep(s, '<rect width="1920" height="1080" fill="#1E1F22" mask=', '<rect width="1920" height="1080" fill="#F2F3F4" mask=')
    s = rep(s, "c.setAttribute('stroke', '#fff');", "c.setAttribute('stroke', '#1E1F22');")
    s = rep(s, 'const FONDU = 0.4;', 'const FONDU = 0.6;')
    return avant_moteur(s, JS_LUMIERE)


for nom, f in [('v10-helly-co-cinema', cinema), ('v11-helly-co-bilingue', bilingue), ('v12-helly-co-lumiere', lumiere)]:
    (ICI / f'{nom}.html').write_text(f(), encoding='utf-8')
    print(nom)
