---
name: speicherbereinigung
version: 1.0.0
type: skill
author: Lukas Geiger und OpenAI Codex
created: 2026-08-04
updated: 2026-08-05
description: "Récupération d'espace Windows fondée sur des preuves, avec mode d'urgence contrôlé, mesure de l'occupation physique, criminalistique des processus et de l'origine, ainsi que des mesures réversibles contre les remplissages récurrents de stockage."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: utilities
tags: [windows, storage, cleanup, forensics, onedrive, pagefile, logs]
language: fr
status: active
visibility: public
dependencies:
  tools: [powershell]
  services: []
  protocols: []
  python: []
provenance:
  origin: custom
  origin_path: "~/.codex/skills/speicherbereinigung"
  origin_version: null
  origin_repo: null
  last_sync_from_origin: 2026-08-05
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6d44ad70bc2f7abc4086474c001d33a6727d9bb6f9793333d804ad3af4907661
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.649434+00:00"
---
<img src="banner.png" width="100%" alt="speicherbereinigung banner">

# Nettoyage de l'espace de stockage

## Objectif et résultat

Cette compétence récupère de manière contrôlée de l'espace de stockage sous Windows et empêche
que le même chemin de remplissage n'occupe à nouveau le disque immédiatement. Elle fonctionne en
trois phases : libération d'urgence, criminalistique des causes et limitation durable.

Chaque mutation suit le même protocole :

`Fund -> Entscheidung -> begrenzte Ausführung -> Readback -> Messung`

Si l'utilisateur ne nomme pas d'objectif plus élevé, la tâche n'est considérée comme terminée que
lorsque le volume système affiche à nouveau au moins 50 Go d'espace libre après la dernière
mutation. Le premier seuil d'urgence, de 10 Go supplémentaires, ne met fin qu'à l'état aigu, et
non à l'ensemble de la tâche.

## Quand l'activer

Utilise cette compétence dans les cas suivants :

- disque système presque plein ou perte d'espace récurrente ;
- journaux, caches, fichiers d'échange, archives ou builds anormalement volumineux ;
- clones en double, générations de sauvegarde ou copies cloud locales ;
- événements d'épuisement de ressources ou processus à commit fortement croissant ;
- suspicion que des planificateurs, des observateurs ou des clients de synchronisation régénèrent des données.

## Règles de sécurité

- Avant chaque mutation, détermine l'espace libre, le volume, l'état des processus, les verrous,
  les points de reparse et le chemin absolu résolu de la cible.
- Pour les actions récursives, vérifie que la cible se trouve dans la racine explicitement
  choisie. N'utilise jamais de variables ou de motifs glob comme cibles de suppression non vérifiées.
- Ne supprime aucune racine de volume, d'utilisateur, de dépôt, de cloud ou de projet.
- Conserve les sources actives, le travail non validé, les secrets, les copies de conflit, les
  verrous étrangers, `.git` et l'unique copie de restauration.
- Privilégie la corbeille, la quarantaine, la compression ou la déshydratation cloud. Une suppression
  irréversible n'est admissible que pour une découverte exactement identifiée et régénérable ;
  documente le chemin, la taille et la restauration.
- Modifie le fichier d'échange, la mise en veille prolongée, les services ou les limites système
  uniquement avec les droits nécessaires, un plan de retour arrière et une relecture complète.
  `Zugriff
  verweigert` n'est pas une mesure réussie.
- Ne supprime jamais d'objets cloud OneDrive pour libérer de l'espace local. La suppression cloud et
  la déshydratation locale sont des opérations différentes.

## Phase 1 : libération d'urgence

### 1. Référence initiale

Relève au minimum :

```powershell
Get-PSDrive -Name C | Select-Object Used, Free
Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" |
  Select-Object DeviceID, Size, FreeSpace
Get-Process | Sort-Object PrivateMemorySize64 -Descending |
  Select-Object -First 15 Name, Id, PrivateMemorySize64, WorkingSet64
```

Note l'heure, la valeur de départ et la cible. Distingue `PrivateMemory` ou
le commit de `WorkingSet` : un processus peut afficher peu de RAM dans son working set
tout en occupant fortement le fichier d'échange.

### 2. Inventaire limité

Commence par les racines locales connues et les fenêtres de modification récentes. Ne recherche pas
aveuglément et récursivement dans l'ensemble des répertoires cloud ou utilisateur. Les candidats
appropriés sont :

- les caches de modèles, de paquets et de builds clairement régénérables ;
- les anciennes sorties de build terminées ;
- les journaux d'application pouvant être rotés ;
- les générations d'archives ou de sauvegardes vérifiées ;
- les copies cloud locales entièrement synchronisées.

Pour les fichiers épars, compressés et les espaces réservés cloud, la longueur du fichier ne
correspond pas à l'occupation physique. Utilise l'allocation NTFS (`GetCompressedFileSizeW`),
`compact` ou un outil équivalent, et compare l'espace libre avant et après.

### 3. Traiter une découverte

Traite exactement une découverte par étape de mesure. Vérifie ensuite :

- les octets réellement récupérés ;
- les erreurs, les descripteurs ouverts et les verrous restants ;
- la persistance de la source protégée ;
- la possibilité de restauration ou de régénération ;
- si un processus recrée immédiatement la découverte.

Le mode d'urgence ne prend fin qu'après 10 Go supplémentaires démontrés. Ensuite, le déroulement
passe immédiatement à la criminalistique.

## Phase 2 : déterminer de manière criminalistique les processus de remplissage et l'origine

### 1. Épuisement des ressources et fichier d'échange

Lis ensemble les preuves actuelles et historiques :

```powershell
Get-CimInstance Win32_ComputerSystem |
  Select-Object AutomaticManagedPagefile
Get-CimInstance Win32_PageFileUsage |
  Select-Object Name, AllocatedBaseSize, CurrentUsage, PeakUsage
Get-WinEvent -FilterHashtable @{LogName='System'; Id=2004} -MaxEvents 20
```

L'événement 2004 du Windows Resource Exhaustion Detector contient les processus ayant le commit
le plus élevé au moment de l'événement. Associe le PID, le nom du processus, les horodatages et les
octets aux processus actuels. Une grande `pagefile.sys` ne prouve pas à elle seule que le fichier
lui-même est la cause ; ce qu'on recherche, c'est le processus qui a déclenché le commit.

### 2. Croissance des fichiers

Regroupe les fichiers nouveaux ou modifiés par :

- heure de création et de modification ;
- chemin parent et extension ;
- propriétaire ou processus créateur ;
- taux quotidien en fichiers et en octets physiquement occupés.

Examine en particulier les répertoires de journaux, de caches, de synchronisation, de sauvegarde, de
build, de téléchargement et de session. Une rétention de sept jours est inadaptée si un client écrit
plusieurs gigaoctets par jour et que le volume est petit.

### 3. Automatisations

Vérifie la fréquence, la rétention et le succès du planificateur de tâches, des services, des
observateurs et des programmes de démarrage :

```powershell
Get-ScheduledTask | Where-Object State -ne 'Disabled'
Get-ScheduledTaskInfo -TaskName '<task-name>'
```

Vérifie séparément l'action, le déclencheur, l'intervalle de répétition, le dernier code de retour
et la prochaine exécution. Une tâche existante ne prouve pas que la rétention ou la fréquence
maîtrisent la croissance réelle.

## Phase 3 : limitation durable

Choisis la mesure efficace la plus petite et réversible :

- exécuter la rotation des journaux plus souvent et y ajouter une limite de taille ;
- redémarrer de manière contrôlée un client au comportement anormal et mesurer son commit ;
- limiter le défilement du terminal ou la journalisation de débogage à une valeur raisonnable ;
- supprimer les anciens caches régénérables et observer leur régénération automatique ;
- dehydrater les contenus cloud vérifiés avec « Libérer de l'espace » ;
- aligner la fréquence et la rétention des planificateurs sur le taux quotidien empirique ;
- modifier le fichier d'échange ou la mise en veille prolongée uniquement de manière administrative,
  avec un plan de redémarrage et de retour arrière.

Pour Windows Terminal, un défilement standard limité peut par exemple ressembler à ceci :

```json
{
  "profiles": {
    "defaults": {
      "historySize": 2000
    }
  }
}
```

Conserve les paramètres existants et valide le fichier JSON après la modification.

### Contrôle spécifique à OneDrive

Avant une déshydratation, l'état de synchronisation et les envois en attente doivent être vérifiés.
Utilise un gestionnaire de fichiers compatible avec le filtre cloud ou la commande « Libérer de
l'espace » de l'Explorateur. La déshydratation ne doit pas supprimer le contenu cloud.

Examine séparément la zone de journaux locaux de OneDrive sous
`$env:LOCALAPPDATA\Microsoft\OneDrive\logs`. Si une sous-zone génère plusieurs gigaoctets par jour, combine une rétention
basée sur le temps avec une limite de taille maximale stricte et une exécution planifiée suffisamment
fréquente. Protège les fichiers très récents ou ouverts et vérifie après l'exécution à la fois l'état
de la tâche et la taille restante.

## Contrôle final et rapport

Après la dernière mutation :

1. Attends la fin des opérations cloud ou de suppression asynchrones.
2. Relis l'espace libre et le commit des processus.
3. Contrôle par relecture les configurations modifiées, les tâches et la taille des journaux.
4. Effectue un bref nouveau test : une création excessive d'espace se reproduit-elle pendant la
   fenêtre d'observation ?
5. Rapporte la valeur de départ, chaque découverte et sa décision, les octets physiquement récupérés,
   les processus de remplissage, les ajustements durables, les retours arrière, les risques résiduels
   et la valeur finale.

N'affirme ni nettoyage, ni limitation de processus, ni atteinte de l'objectif de 50 Go sans relecture
actuelle appropriée.

## Limites connues

- Sans droits administratifs, les modifications du fichier d'échange, de la mise en veille prolongée
  ou des services peuvent rester bloquées. Documente l'étape exacte restante.
- Les événements historiques de processus prouvent un ancien élément de remplissage ; la situation
  actuelle nécessite en plus des données de processus et de croissance des fichiers.
- Un concept de sauvegarde planifié n'est pas une sauvegarde. Un transfert ou une suppression exige
  l'identité actuelle de la cible, un manifeste ou un hachage, la preuve d'une restauration et un montage.
- En cas de propriété incertaine, de travaux étrangers en cours ou de cible inconnue, la décision
  applicable est `nichts`.

## Journal des modifications

### 1.0.0 (2026-08-05)

- Première version portable pour la bibliothèque centrale de compétences.
- Ajout de la criminalistique de l'épuisement des ressources, du fichier d'échange et des processus.
- Séparation claire entre l'occupation physique NTFS et la déshydratation OneDrive.
- Ajout de la rotation des journaux OneDrive avec limite de temps et de taille.
- Définition de contrôles stricts d'urgence et de clôture avec relecture.
