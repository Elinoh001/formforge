# FormForge — Étape 1 : structure du projet + navigation + SQLite

## Installation

```bash
python -m venv venv
source venv/bin/activate       # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer l'application (sur ordinateur, pour développer)

```bash
python main.py
```

Au premier lancement :
- le dossier `storage/` est créé automatiquement ;
- la base `storage/formforge.db` est créée avec les 4 tables
  (`applications`, `entities`, `fields`, `records`) ;
- les logs techniques sont écrits dans `storage/formforge.log`.

## Ce qui est testable à cette étape

1. **Écran d'accueil** : titre FORMFORGE + bouton « + Créer une application »
   + bouton « Mes applications ».
2. **Navigation** : les deux boutons mènent à l'écran « Mes applications » ;
   la flèche « ← » ramène à l'accueil.
3. **Liste vide** : au premier lancement, message « Aucune application
   pour le moment. ».
4. **Créer une application** : bouton « + Créer » en bas → popup avec
   Nom / Description / Icône → « Créer » :
   - le nom est obligatoire (sinon message d'erreur dans la popup) ;
   - un `slug` unique est généré automatiquement à partir du nom ;
   - l'application est enregistrée en SQLite (table `applications`) ;
   - la liste se rafraîchit et affiche une carte avec
     `0 entité(s) · 0 enregistrement(s)`.
5. **Persistance** : en relançant `python main.py`, les applications créées
   précédemment sont toujours là (lecture depuis SQLite).

## Vérifier le contenu de la base (optionnel)

```bash
sqlite3 storage/formforge.db "SELECT id, name, slug FROM applications;"
```

## Architecture mise en place à cette étape

```
Screen (ApplicationsScreen)
    ↓
Service (ApplicationService)     ← validation, génération de slug
    ↓
Repository (ApplicationRepository)  ← implémente BaseRepository
    ↓
Database (SQLite)
```

`BaseRepository` est une interface abstraite : la version SaaS future
pourra ajouter une `ApiApplicationRepository` sans changer
`ApplicationService` ni les écrans.

## Prochaine étape (à valider avant de continuer)

- `application_builder_screen.py` dédié (au lieu de la popup) ;
- CRUD Entités (`EntityBuilderScreen`, `EntityRepository`, `EntityService`) ;
- suppression/édition/export sur les cartes d'application.
