# Detecte invasão na sua conta

Skill de detecção de conta comprometida e acesso automatizado não autorizado — para
os sistemas que um escritório de contabilidade realmente usa: ERP contábil, portal
do cliente, e-CAC e procurações, Google Workspace, Microsoft 365, Cloudflare e os
apps que você mesmo criou com IA (Lovable, Supabase e afins).

Automação não autorizada raramente se anuncia: ela loga como um usuário legítimo,
com user-agent de Chrome, e trabalha em silêncio. Esta skill ensina a encontrá-la
pelos sinais que ela **não consegue esconder** — de onde vem, com que ritmo opera e
o que faz — e a responder na ordem certa quando encontrar.

## O que ela faz

- **Exige autorização antes de tudo.** A primeira resposta confirma que os sistemas
  são seus (ou que você tem autorização explícita do responsável). Sem isso, a
  skill não investiga — só explica os sinais e o checklist de prevenção.
- **Evidência antes de análise.** Logs de acesso expiram rápido (há sistemas que
  guardam ~24h). Com suspeita ativa, a skill manda exportar primeiro e analisar depois.
- **Ensina os 5 sinais de automação**, todos verificáveis com o log do próprio sistema:
  1. **Origem de datacenter (ASN)** — user-agent é forjável; o IP de origem não mente.
  2. **Senha em claro na automação** — login por senha repetido em cadência = o script tem a senha; derrubar sessão não contém.
  3. **Cadência robótica** — intervalo cravado por muitas horas contínuas é máquina; humano fecha o laptop.
  4. **Extração em massa** — a mesma conta lendo listas inteiras repetidas vezes é scraping, mesmo sem escrever nada.
  5. **Ação fora de horário / em lote** — rajadas de segundos, de madrugada.
- **Mede, não acha.** `scripts/cadencia.py` transforma timestamps de login em
  veredito estatístico de metrônomo — calibrado para **não** marcar a aba de
  navegador aberta no expediente como bot.
- **Playbook de resposta na ordem certa:** preservar evidência → **trocar a senha**
  (antes de revogar sessões — senha vazada reloga) → revogar tokens/integrações →
  2FA → dimensionar dano → enquadramento correto ("acesso não autorizado" ≠
  "invasão criminosa": a evidência prova automação, não autoria).
- **Veredito sobre contas, nunca acusação a pessoas.** O titular pode ser a maior
  vítima.

## O que ela não faz

Não investiga sistemas de terceiros sem autorização. Não vigia pessoas nem conteúdo
pessoal de colaboradores. Não ensina contra-ataque, retaliação ou qualquer técnica
ofensiva — resposta é contenção, evidência e enquadramento.

## Instalação

Baixe o `.zip` da [última Release](../../releases/latest).

- **Claude (claude.ai):** Configurações → Capacidades → Skills → upload do `.zip` **sem descompactar**.
- **ChatGPT:** Configurações → Habilidades (`chatgpt.com/admin/skills`) → **+** → arraste o `.zip`. Sem acesso à administração? Crie um Projeto, envie os arquivos e instrua: *"Siga o SKILL.md que está nos arquivos deste projeto."*
- **Claude Code · Codex CLI · Cursor:** descompacte e copie a pasta `rdd-detecta-invasao/` para `~/.claude/skills/` (ou `.claude/skills/` dentro de um projeto).

Depois acione pelo nome: *"Use a skill rdd-detecta-invasao. Quero verificar se há acesso estranho nos meus sistemas."*

## O que vem dentro

| Caminho | Conteúdo |
|---|---|
| `SKILL.md` | O método completo: gate de autorização, retenção primeiro, os 5 sinais, veredito por conta, resposta e prevenção |
| `references/sinais-de-automacao.md` | Cada sinal em profundidade, com "como verificar" e falsos positivos conhecidos |
| `references/onde-olhar-logs.md` | Onde cada sistema guarda o log de acesso e por quanto tempo |
| `references/playbook-resposta.md` | Contenção na ordem certa, preservação de evidência, enquadramento |
| `scripts/cadencia.py` | Detector determinístico de cadência robótica (stdlib, sem rede) |
| `assets/relatorio-verificacao-template.md` | Modelo do relatório de verificação |

## Skill irmã

Esta skill detecta **quem está operando** as suas contas. Para descobrir **o que
ficou exposto** num app que você construiu com IA, use a
[rdd-appsec-mentor](https://github.com/robertodiasduarte/rdd-appsec-mentor) —
diagnóstico de segurança com plano de correção priorizado.

## Licença

MIT — veja [LICENSE](LICENSE).

---

<details>
<summary><strong>English</strong></summary>

# Detect an intrusion in your account

A compromised-account / unauthorized-automation detection skill for the systems an
accounting firm actually runs: ERP, client portal, government tax portals, Google
Workspace, Microsoft 365, Cloudflare, and the apps you built with AI (Lovable,
Supabase and the like).

Unauthorized automation rarely announces itself: it logs in as a legitimate user,
with a Chrome-looking user-agent, and works in silence. This skill teaches you to
find it through the signals it **cannot hide** — where it comes from, the rhythm it
operates at, and what it does — and to respond in the right order when you do.

## What it does

- **Requires authorization first.** It only audits systems you own or are
  explicitly authorized to audit.
- **Evidence before analysis.** Access logs expire fast (some retain ~24h). With an
  active suspicion, export first, analyze later.
- **Teaches the 5 automation signals:** datacenter origin (ASN — the user-agent
  lies, the source IP doesn't), password-in-the-clear automation (password logins
  on a schedule mean the script *has* the password — killing sessions won't contain
  it), robotic cadence (a metronome across the night is a machine; humans close the
  laptop), mass extraction (scraping reads, no writes), and out-of-hours batch actions.
- **Measures instead of guessing:** `scripts/cadencia.py` turns login timestamps
  into a statistical metronome verdict — calibrated so an office-hours browser tab
  is *not* flagged as a bot.
- **Response playbook in the right order:** preserve evidence → **change the
  password** (before revoking sessions) → revoke tokens/integrations → 2FA →
  assess damage → correct framing ("unauthorized access" ≠ "criminal intrusion":
  evidence proves automation, not authorship).
- **Verdicts are about accounts, never accusations against people.**

## What it does not do

No third-party systems without authorization. No monitoring of people or their
personal content. No counter-attack or offensive techniques — response means
containment, evidence and framing.

## Installation

Download the `.zip` from the [latest Release](../../releases/latest).

- **Claude (claude.ai):** Settings → Capabilities → Skills → upload the `.zip` **without unzipping**.
- **ChatGPT:** Settings → Skills (`chatgpt.com/admin/skills`) → **+** → drop the `.zip` in.
- **Claude Code · Codex CLI · Cursor:** unzip and copy `rdd-detecta-invasao/` into `~/.claude/skills/` (or a project's `.claude/skills/`).

## Sister skill

This skill detects **who is operating** your accounts. To find out **what was left
exposed** in an app you built with AI, use
[rdd-appsec-mentor](https://github.com/robertodiasduarte/rdd-appsec-mentor).

## License

MIT — see [LICENSE](LICENSE).

</details>
