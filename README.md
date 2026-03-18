# Minecraft Voxel Engine
Voxel Engine (like Minecraft) in Python and OpenGL.

## Installation automatique des dépendances
- Au premier lancement, le jeu vérifie les dépendances Python et lance automatiquement `pip install -r requirements.txt` si nécessaire.
- Un fichier marqueur `.first_launch_deps_ok` est créé pour éviter de relancer cette installation à chaque démarrage.
- Versions Python supportées: `3.10` et `3.11` (les dépendances actuelles ne sont pas compatibles avec Python `3.12+`).

## Nouvelles fonctionnalités
- Cycle jour/nuit + blocs émissifs (`GLOWSTONE`) pour une gestion de lumière simple.
- Physique joueur: gravité, saut, collisions (désactivable avec noclip).
- Mobs passifs/hostiles avec déplacement basique et dégâts en contact.
- Inventaire créatif: choix de blocs (molette + touches `1..9`) et pose/destruction illimitée.
- Nouveaux blocs: pierre taillée, planches, briques, argile, pierre lumineuse.
- Biomes (plaines, désert, montagnes, neige, marais) influençant terrain et blocs.

## Contrôles
- Déplacement: `ZQSD`
- Saut (physique): `Space`
- Mode noclip (vol): `F`, puis monter/descendre avec `A/E`
- Casser/poser un bloc: clic gauche / clic droit
- Changer de bloc: molette souris ou touches `1..9`

![minecraft](/screenshot/0.jpg)
