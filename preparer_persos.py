"""Met chaque portrait IA choisi au format 1920x1080, personnage décalé à droite,
le fond prolongé vers la gauche pour laisser la place au texte.

    python preparer_persos.py yanis=2 hadj=1 ...   (numéro de la variante retenue)
"""
import sys
from pathlib import Path

from PIL import Image, ImageFilter, ImageStat

SOURCE = Path.home() / 'ia-locale' / 'portraits'
SORTIE = Path(__file__).resolve().parent / 'assets' / 'photos' / 'ia-persos'
SORTIE.mkdir(parents=True, exist_ok=True)

for arg in sys.argv[1:]:
    nom, v = arg.split('=')
    v, _, dx = v.partition(':')     # « maman=1:-220 » décale le personnage de 220 px vers la gauche
    img = Image.open(SOURCE / f'{nom}-{v}.png').convert('RGB').resize((1474, 842), Image.LANCZOS)
    # couleur du fond : le coin haut gauche de l'image
    fond = tuple(int(c) for c in ImageStat.Stat(img.crop((0, 0, 160, 160))).median)
    toile = Image.new('RGB', (1920, 1080), fond)
    # personnage réduit, posé en bas à droite, centre vers x = 1305
    x, y = 1920 - 1474 + 120 + int(dx or 0), 1080 - 842
    toile.paste(img, (x, y))
    # fondus progressifs sur les bords gauche et haut de l'image collée
    gauche = Image.linear_gradient('L').rotate(-90).resize((300, 842))
    toile.paste(Image.new('RGB', (300, 842), fond), (x, y), gauche)
    haut = Image.linear_gradient('L').rotate(180).resize((1474, 220))
    toile.paste(Image.new('RGB', (1474, 220), fond), (x, y), haut)
    toile.save(SORTIE / f'{nom}.jpg', quality=92)
    print(nom, v, fond)
