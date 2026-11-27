---
name: research-agent
version: 0.2.1
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-11-22
description: "À utiliser lorsque des projets de recherche scientifique doivent être menés de façon structurée, des sources recueillies ou des affirmations validées (ex. 'établir l'état de l'art', 'rechercher des articles', 'vérifier sources et affirmations', /research-agent). Exécute un pipeline de recherche centré projet avec portes en direct, preuves PDF, limites d'affirmation et contrôles de publication. Ne PAS utiliser pour de simples recherches web informelles sans exigence de preuve scientifique."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: research
tags: [research-pipeline, evidence, pdf-validation, publication-gates, pubmed, arxiv, literature-review, science]
language: fr
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/ResearchAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---



<img src="banner.png" width="100%" alt="research-agent banner">

> **Français** — Version française officielle de la compétence `research-agent`.

# Research Agent — Agent de recherche scientifique

Cette version constitue l'origine centrale du paquet. Au sein de
`<OneDrive>/.TOPICS/.RESEARCH`, le pipeline actuel du projet et de recherche fait
foi ; le code PubMed/arXiv fourni n'est qu'un outil de recherche optionnel.

## Chaîne d'autorité contraignante

1. Mission utilisateur en cours et règles globales `AGENTS.md` / `GPT.md` / `CLAUDE.md`.
2. Fichiers actuels propres au projet, état en direct, verrous, décisions et
   registres. Les suites numérotées et pointeurs explicites `Current` priment sur
   leurs prédécesseurs ; les archives et copies de conflit ne deviennent jamais
   tacitement une autorité de substitution.
3. Pipeline en direct à la racine de recherche : en particulier `CLAUDE.md`, `START*`,
   `MASTER*`, `POLICY*`, `PUBLIKATIONSVERFAHREN.md`, `QUALITY_RULES*`, pointeurs actuels
   de statut/`TODO` ainsi que `CHECKS-LOG.txt` et `CHECKS-REG.md`.
4. Cette compétence et ses scripts de recherche génériques.

Au démarrage, lire `~/.codex/GPT.md`, les deux fichiers globaux `CLAUDE.md`, les règles de recherche
et les fichiers locaux actuels du projet `KONZEPT*`, de planification, `TODO*`, `BEWEISNOTIZ*`,
de décisions, de publication et de bibliographie. En cas de contradiction, appliquer le principe fail-closed.

## Portes en direct et mutations

- Un fichier `CHECKS-LOG.txt` récent et illisible constitue une porte dure en lecture seule.
- Avant toute sélection ou modification : vérifier `CHECKS-REG.md`, le registre du projet,
  les décisions, le cas échéant le plan Fable, les verrous, les copies de conflit et
  l'état en direct.
- Documenter les blocages (holds) BACH/BYUM et leur expiration exclusivement avec `fc_get_time`.
- Dans OneDrive, utiliser FileCommander pour la navigation, les lectures, métadonnées, sommes
  de contrôle, verrous cloud et exécutions. Avant toute écriture, poser un verrou étroit, préserver
  les verrous et modifications d'autrui, et ne retirer que son propre verrou à la fin.
- Ne pas contourner de manière autonome les décisions produit/métier, délais de carence (cooldowns),
  clones canoniques manquants, portes de reproduction et autorisations à usage unique déjà consommées.

## Règles de preuve, d'affirmation, de calcul et de publication

- Exploiter tôt les trouvailles locales `.WISSEN`, puis vérifier les énoncés scientifiques sur les
  sources primaires. Lier exactement phrase/section/page, hypothèses, normalisation et type d'objet ;
  dater les requêtes volatiles.
- Ne retenir les PDF comme sources qu'après vérification de `%PDF-`, d'un nombre de pages/extraction
  de texte lisible et d'un SHA-256. Les fichiers HTML, CAPTCHA, 404 et emplacements réservés ne comptent pas.
- Séparer mesure, preuve à long terme, incertitude et piste de recherche ; ne jamais promouvoir un
  proxy, préflight, revue ou exécution partielle au rang d'affirmation scientifique.
- Les artefacts allemands destinés à l'utilisateur final utilisent de vrais trémas/umlauts. Ne vérifier
  EN/DE et un artefact combiné que si le pipeline actuel l'autorise : structure, bibliographie, build,
  extraction et encodage.
- Calcul (Compute) exclusivement selon le contrat en direct `.COMPUTE`/du projet et les règles de placement.
  Aucune exécution longue sur ordinateur portable, relance, poursuite, modification de file ni exécution
  unique déjà consommée sans autorisation explicite. Un timeout ou une erreur d'infrastructure n'est pas un
  résultat mathématique négatif.
- Téléversement (upload), passage en public, soumission, inscription au registre et release sont des
  portes utilisateur séparées. La préparation et le dry-run ne valent pas publication.
- Clôture uniquement après les tests/builds requis, la relecture (readback) des artefacts, la mise à jour
  des registres projet et racine, le cas échéant la mémoire d'automatisation/passation et le retrait des
  propres verrous temporaires. Mentionner explicitement les portes restantes.

## Assistant bibliographique optionnel

Les modules Python suivants utilisent exclusivement la bibliothèque standard
(`urllib`, `xml`, `json`). Ils assistent la recherche et la revue, mais ne remplacent
aucun des contrôles d'autorité ou de preuve ci-dessus.

## Architecture

```
ResearchAgent (Orchestrateur)
  sources/          Sources de données (PubMed, arXiv)
    base.py         Dataclasses Article/SearchResult, Source ABC
    pubmed.py       NCBI E-utilities (esearch + efetch)
    arxiv.py        API Atom d'arXiv
  workflows/        Workflows de recherche
    quick_search.py Recherche rapide multi-sources
    literature_review.py  Revue de littérature en 4 phases
```

## Utilisation comme bibliothèque Python

```python
from scripts.agent import ResearchAgent

agent = ResearchAgent()

# Recherche rapide
result = agent.search("machine learning diagnostics", max_results=10)
print(result)

# Revue de littérature structurée
plan = agent.create_review_plan("transformer architectures", years=3)
print(plan.total_articles, "articles trouvés")

# Enregistrer le résultat
agent.save_result(result, "research_ml.md", fmt="markdown")
```

## Utilisation en CLI

```bash
cd scripts
python -m ResearchAgent search "quantum computing" --max 20
python -m ResearchAgent review "CRISPR gene editing" --years 5
```

## Sources de données

| Source | API | Limite de débit | Accès |
|--------|-----|-----------------|-------|
| PubMed | NCBI E-utilities | 3/s (sans clé), 10/s (avec clé) | Gratuit |
| arXiv | Atom REST API | Non documentée | Gratuit |

Extensible : les nouvelles sources implémentent la classe abstraite `Source` depuis `sources/base.py`.

## Extension

```python
from scripts.sources.base import Source, SearchResult

class MySource(Source):
    @property
    def name(self) -> str:
        return "my-source"

    def search(self, query, max_results=10, **kwargs):
        # Implémenter la requête API
        ...

    def get_article(self, article_id):
        ...

    def is_available(self) -> bool:
        return True
```

## Notes BACH

> Pertinent uniquement lors d'une utilisation au sein de BACH.

```python
from scripts.agent import ResearchAgent
agent = ResearchAgent(use_bach=True)  # Intégration BACH optionnelle
```

## Journal des modifications

### 0.2.1 (2026-11-22)
- Mention linguistique corrigée.

### 0.2.0 (2026-08-22)
- Autorité du projet et du pipeline ancrée avant les scripts de recherche génériques.
- Intégration des portes en direct, règles OneDrive/verrous et pointeurs `Current`.
- Ajout des justificatifs de sources primaires/PDF, limites d'affirmation et contrôles bilingues.
- Inscription fail-closed des portes de calcul, téléversement, registre et clôture.

### 0.1.0 (2026-03-12)
- Migration depuis `MODULAR_AGENTS/ResearchAgent` vers la bibliothèque de compétences
- Sources PubMed + arXiv
- Workflows `QuickSearch` + `LiteratureReview`
