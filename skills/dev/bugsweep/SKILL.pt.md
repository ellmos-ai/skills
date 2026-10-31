---
name: bugsweep
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-06-01
updated: 2026-06-13
description: "Varredura sistemática de bugs com valor-alvo escalonado conforme o tamanho da base de código, escalonamento por duplicação, rastreamento de áreas e verificação final. Use em /bugsweep ou sempre que o usuário solicitar uma passagem sistemática de bugs."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [bugs, debugging, sweep, quality-assurance, workflow, convergence]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': ['bugfix-protocol'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/bugsweep/', 'origin_version': '1.0.0', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 72c943e5f956ae19c2e36d0478108228b95866bb77faaadf3dca77a686d9f972
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="bugsweep banner">

# /bugsweep — Workflow Sistemático de Varredura de Bugs

Busca iterativa de bugs com critério de parada convergente. Escala conforme a base de código, escalona quando há suspeita de busca superficial e evita repetição por meio do rastreamento de áreas.

## 1. Calcular a taxa base

```
LOC = produktive Quellzeilen (src/, lib/ — ohne Tests, Configs, Docs, generated)
x = max(1, ceil(LOC / 1500))
Grundrate = x * 3
```

| LOC | x | Taxa base |
|-----|---|-----------|
| ~1500 | 1 | 3 |
| ~3000 | 2 | 6 |
| ~4500 | 3 | 9 |
| ~10000 | 7 | 21 |

Informe ao usuário: "Base de código: {LOC} LOC → taxa base = {Grundrate} execuções de busca limpas."

## 2. Ciclo de busca

```
zähler = 0
ziel = Grundrate
je_bug_gefunden = False
geprüft = []  # (bereich_name, typ: code|aufgabe)

LOOP:
  bereich = wähle_neuen_bereich()  # Siehe Bereichs-Regeln
  geprüft.append(bereich)
  
  Führe gründliche Bug-Suche durch
  
  IF Bug gefunden:
    je_bug_gefunden = True
    Fix nach bugfix-protocol (Phase 4+5)
    Review: siehe Modell-Regel (neuere Modellklassen: kein externer Review nötig)
    Commit + Push
    zähler = 0  # RESET
  ELSE:
    zähler += 1
    Melde: "✓ Sauber: {bereich} — {zähler}/{ziel}"
  
  IF zähler >= ziel:
    IF NOT je_bug_gefunden:
      # Verdoppelungs-Eskalation: kein einziger Bug → zu oberflächlich?
      ziel = Grundrate * 2
      je_bug_gefunden = True  # Eskalation nur EINMAL
      Melde: "⚠ Kein Bug in {Grundrate} Läufen → Ziel verdoppelt auf {ziel}."
      CONTINUE LOOP
    ELSE:
      GOTO Abschluss-Verifikation
```

### Dicas práticas para o ciclo de busca (aprendidas em varreduras)

- **Repositórios sem Git:** Onde não existe `git` (por exemplo, pastas de projeto sincronizadas na nuvem), um **backup versionado** substitui o "commit + push": antes da primeira correção, crie `datei_<ts>.bak`. **Atenção — o backup pré-correção NÃO é a salvaguarda do trabalho:** após a última correção, faça um novo backup `_FINAL_`; caso contrário, em caso de falha na sincronização, todo o trabalho de correção será perdido.
- **Muitos bugs já conhecidos:** Se já houver N bugs conhecidos no início (por exemplo, de uma execução anterior), o ciclo "por bug: correção → revisão → commit → reset" é impraticável. Nesse caso, trate os bugs conhecidos como UM único bloco de correção (revisão conjunta no final) e conte a taxa base e o ciclo de busca a partir do primeiro bug NOVO encontrado. A lógica de reset continua válida para bugs novos encontrados durante a varredura.
- **Mesmo bug em vários locais:** Um erro encontrado (por exemplo, uma expressão regular incorreta ou uma suposição de formato quebrada) frequentemente foi copiado para outros pontos. Após cada correção, verifique por busca se o mesmo padrão aparece em outro lugar — isso constitui uma "área" própria e valiosa.

## 3. Regras de área (anti-manipulação)

Uma "área" é um **foco de código** ou uma **tarefa** (finalidade do código).

### Foco de código
- Pode ser **ampliado** (mais arquivos) ou **deslocado** (outra parte) entre execuções
- NÃO pode ser exatamente a mesma seleção de uma execução anterior
- Exemplo OK: Execução 1 = `maintenance.py`, Execução 5 = `maintenance.py + orchestrator.py` (ampliada)
- Exemplo NÃO OK: Execução 1 = `maintenance.py`, Execução 5 = `maintenance.py` (idêntica)

### Tarefa (finalidade)
- Pode ser formulada de forma **mais granular** (verificar uma subfunção) ou **mais ampla** (funções relacionadas)
- NÃO pode ser exatamente a mesma tarefa
- Exemplo OK: Execução 1 = "Thread-safety no watchdog", Execução 5 = "Thread-safety de todo o tray" (mais ampla)
- Exemplo OK: Execução 1 = "Detecção de processos", Execução 5 = "Correspondência de marcadores de store na detecção de processos" (mais granular)
- Exemplo NÃO OK: Execução 1 = "Thread-safety no watchdog", Execução 5 = "Thread-safety no watchdog" (idêntica)

### Nomenclatura
- A área DEVE ser nomeada ANTES da busca (sem atribuição posterior)
- Formato: `"{Name}" ({typ}: code|aufgabe)`

## 4. Verificação final

Depois que contador (zähler) >= alvo (ziel) E je_bug_gefunden:

**Passo A — bugfix-protocol, Fase 5:**
- [ ] Suíte de testes completa passando (`pytest`)
- [ ] **Executar REALMENTE pelo menos uma vez o caminho de execução alterado** — não apenas os testes. Testes unitários verdes sobre código que nem chama o ponto alterado são falsa segurança. Execute o caminho efetivamente alterado (dry-run, smoke test, chamada de CLI) e verifique tracebacks / erros de assinatura / de nome. `py_compile` ou apenas importar verifica SOMENTE a sintaxe — não se o caminho funciona.
- [ ] **Cada correção tem pelo menos um teste que a toca** — uma correção sem teste que realmente acione o ramo alterado é considerada não verificada (para caminhos de orquestração/rede, combine eventualmente mock + dry-run).
- [ ] Verificação de tipos (se configurada)
- [ ] Lint (se configurado)
- [ ] Casos de borda das correções da sessão verificados

**Passo B — Revisão (regra por modelo):**
- **Classes de modelo mais recentes (por exemplo, Claude 5 / classe Fable):** NÃO é necessária revisão externa por consultor/segundo modelo.
  O Passo A (testes + smoke test real) é a verificação. Opcionalmente, em caso de incerteza real:
  um subagente revisor novo — cujas conclusões, porém, devem ser verificadas empiricamente
  (teste contra o código não alterado) antes de serem tratadas como bug.
  Contexto (experiência de varredura de 2026-06-11): o revisor secundário não estava disponível, o
  subagente substituto entregou 1 achado (confiança 85), que um teste mostrou não ser um bug —
  a revisão externa não mudou o resultado.
- **Modelos mais antigos:** Discussão final com consultor (alternativa: um segundo
  modelo como revisor); o consultor confirma ou encontra lacunas.

**Em caso de bug encontrado na verificação:**
→ Correção + teste + commit
→ RESET: contador (zähler) = 0, alvo (ziel) = taxa base (nova, SEM duplicação)
→ Voltar ao ciclo de busca (lista de verificados permanece, je_bug_gefunden = True)

**Em caso de verificação limpa:**
→ CONCLUÍDO. Commit + push. Emitir o protocolo.

## 5. Protocolo (ao final)

```markdown
## Bug-Sweep Ergebnis

- **Codebasis:** {LOC} LOC
- **Grundrate:** {Grundrate} (eskaliert: {ziel})
- **Geprüfte Bereiche:** {len(geprüft)}
- **Bugs gefunden:** {anzahl}
- **Resets:** {anzahl_resets}
- **Verdoppelung ausgelöst:** ja/nein
- **Fixes:**
  - {titel} — {commit_hash}
  - ...
- **Finale Test-Suite:** {passed}/{total} grün
- **Review-Verdict:** Selbstverifikation (neuere Modellklasse) / Advisor bestätigt / Lücken benannt
```

## Quando usar este workflow

- Após o desenvolvimento de funcionalidades (garantia de qualidade)
- Antes de um release (varredura de aceitação)
- Periodicamente, como verificação de higiene
- Quando o usuário digitar `/bugsweep`

## Interação com outras skills

- **bugfix-protocol:** Procedimento de correção (fases 4+5) para cada bug encontrado
- **systematic-debugging:** Para bugs de reprodução difícil durante a varredura
- **code-review:** Pode ser usado como área de tarefa

---

## Changelog

### 1.1.0 (2026-06-13)
- Regra por modelo para o Passo B retroportada (da instalação local da skill, estado 2026-06-11): classes de modelo mais recentes verificam sozinhas por meio de testes + smoke test real, sem necessidade de revisão externa; campo "Review-Verdict" do protocolo ampliado de acordo

### 1.0.0 (2026-06-13)
- Primeira publicação na biblioteca de skills (adotada da instalação local da skill, estado 2026-06-01)
