---
name: rdd-detecta-invasao
description: "Orienta contadores e gestores a detectar se uma conta dos seus sistemas (ERP contábil, portal do cliente, e-CAC/procurações, Google Workspace, Microsoft 365, Cloudflare, apps próprios com Supabase) está sendo operada por automação não autorizada ou por terceiro — e a responder na ordem certa. Use quando o usuário suspeitar de conta comprometida, acesso estranho, ações que ninguém do time fez, quiser auditar logs de login, verificar sinais de bot/scraper, preservar evidência ou montar o playbook de resposta a incidente de acesso."
---

# Detecte invasão na sua conta

Automação não autorizada raramente se anuncia. Ela loga como um usuário legítimo,
com um navegador que parece legítimo, e trabalha em silêncio — lendo seus dados ou
agindo em nome de alguém do seu time. Esta skill ensina a encontrá-la pelos sinais
que ela **não consegue esconder**: de onde vem, com que ritmo opera e o que faz.

## Quick start

Ao ser acionado, **a primeira resposta deve estabelecer escopo e autorização**:

> Quais sistemas você quer verificar (ERP, portal do cliente, e-mail corporativo,
> e-CAC, app próprio)? Confirme que os sistemas são do seu escritório/empresa, ou
> que você tem autorização explícita do responsável para auditar os acessos.

Depois:

1. Inventariar os sistemas e onde cada um guarda log de acesso ([references/onde-olhar-logs.md](references/onde-olhar-logs.md)).
2. **Verificar a retenção dos logs ANTES de qualquer outra coisa** — muitos expiram em horas ou dias. Se há suspeita ativa, exportar evidência primeiro, analisar depois.
3. Varrer os 5 sinais de automação, na ordem ([references/sinais-de-automacao.md](references/sinais-de-automacao.md)).
4. Para cadência: coletar timestamps de login/renovação e rodar `scripts/cadencia.py` — o veredito sai com número, não impressão.
5. Classificar cada conta: **Limpa · Suspeita · Comprometida** (sempre com a evidência que sustenta).
6. Se houver conta comprometida: executar o playbook de resposta **na ordem** ([references/playbook-resposta.md](references/playbook-resposta.md)).
7. Entregar o relatório usando [assets/relatorio-verificacao-template.md](assets/relatorio-verificacao-template.md).

## Quando usar / Quando não usar

### Usar

- Sistemas do próprio escritório/empresa do usuário, ou com autorização explícita do responsável.
- Suspeita de conta comprometida: ações que ninguém do time reconhece, cliente relatando dado que não deveria circular, alerta de login estranho.
- Auditoria preventiva periódica dos acessos (recomendado: mensal para papéis sensíveis).
- Montagem de alertas e rotina de prevenção.

### Não usar

- Para investigar sistemas de terceiros sem autorização explícita do responsável.
- Para vigiar pessoas (a skill audita **contas e acessos**, não conteúdo pessoal de colaboradores).
- Para contra-atacar, derrubar ou invadir a origem do acesso suspeito — resposta é contenção e evidência, nunca retaliação.

Se a autorização não for confirmada, não investigar o alvo: oferecer apenas a
explicação dos sinais e o checklist de prevenção genérico.

## Os 5 sinais (resumo — detalhe em [references/sinais-de-automacao.md](references/sinais-de-automacao.md))

| # | Sinal | Por que funciona |
|---|---|---|
| 1 | **Origem de datacenter (ASN)** | User-agent é forjável — bot se apresenta como Chrome. O IP de origem não mente: pessoa física loga de operadora residencial/móvel; script roda em AWS, Hetzner, OVH, GCP, Azure, DigitalOcean, Vultr, Contabo. Olhe o **ASN** do IP, não o "navegador". |
| 2 | **Senha em claro na automação** | Login com usuário+senha repetido a cada N minutos significa que o script **tem a senha** — não um token emprestado. Derrubar a sessão não resolve: ele reloga. |
| 3 | **Cadência robótica (metrônomo)** | Renovação/login em intervalo cravado (desvio-padrão baixo) por muitas horas contínuas é máquina. Humano fecha o laptop, almoça, alterna dispositivo e rede. Use `scripts/cadencia.py`. |
| 4 | **Extração em massa** | A mesma conta lendo listas inteiras (todos os clientes, todos os documentos) repetidas vezes é scraping — mesmo sem nenhuma escrita. |
| 5 | **Ação fora de horário / em lote** | Escritas ou aprovações em rajadas de segundos, de madrugada ou em fim de semana, sem expediente que as explique. |

Um sinal isolado é suspeita; **dois ou mais sinais na mesma conta** é quase sempre
confirmação. E atenção aos falsos positivos conhecidos: internet via satélite
(Starlink) não é datacenter; um lote de aprovações às 14h pode ser trabalho humano
em série; uma aba aberta o dia inteiro renova token com regularidade — por isso o
limiar de metrônomo exige **muitas horas contínuas**, não meia tarde.

## Procedimento

### 1. Gate de autorização e escopo

Confirmar propriedade/autorização, listar os sistemas em escopo e registrar data,
escopo e limitações no relatório.

### 2. Retenção primeiro

Para cada sistema, descobrir por quanto tempo o log de acesso fica disponível
([references/onde-olhar-logs.md](references/onde-olhar-logs.md)). Se a suspeita é
ativa, **exportar agora** (CSV/print/download) tudo que cobre a janela suspeita.
Evidência que expira vale mais do que análise elegante.

### 3. Varredura dos 5 sinais

Para cada conta com papel sensível (sócio, admin, quem aprova, quem tem procuração):

1. Levantar os IPs de origem dos últimos logins e consultar o ASN de cada um
   (whois, bgp.he.net, ipinfo.io — manual, no navegador).
2. Verificar o **tipo** de login: senha, token renovado, SSO, app específico.
3. Coletar timestamps de login/renovação num arquivo de texto (um por linha) e rodar:

   ```bash
   python skills/rdd-detecta-invasao/scripts/cadencia.py acessos.txt
   ```

4. Olhar volume de leitura: relatórios/exportações/consultas em série na mesma conta.
5. Olhar escritas fora de horário: quem fez, quando, em que ritmo.

### 4. Veredito por conta

- **Limpa** — padrões humanos, origens residenciais/móveis coerentes com o time.
- **Suspeita** — 1 sinal presente, sem confirmação (ex.: 1 login de datacenter isolado
  pode ser VPN corporativa — perguntar antes de concluir).
- **Comprometida** — 2+ sinais, ou 1 sinal + ação que o titular nega ter feito.

Nunca elevar suspeita a confirmação sem evidência; nunca acusar pessoa — o achado é
sobre a **conta** (o titular pode ser vítima, não autor).

### 5. Resposta (só para contas Comprometidas)

Seguir [references/playbook-resposta.md](references/playbook-resposta.md) **na ordem**:
preservar evidência → trocar senha → revogar sessões/tokens → 2FA → revisar
integrações → comunicar. A ordem importa: trocar a senha antes de preservar o log
pode apagar exatamente o rastro que você precisa.

### 6. Prevenção (para todos)

- **2FA obrigatório** para papéis sensíveis — mata o valor da senha vazada.
- **Alerta de login de datacenter**: onde o sistema permitir, alertar (não bloquear
  às cegas — VPN corporativa legítima existe) quando papel sensível logar de ASN de datacenter.
- **Rotina de cadência**: revisar mensalmente os acessos das contas sensíveis com o
  mesmo script.
- **Menor privilégio**: nenhum flag único ("ativo", "admin") deve dar acesso total a
  tudo. Quem aprova não precisa exportar; quem exporta não precisa aprovar.
- **Rotação de senha** ao menor sinal — e nunca reutilizada entre sistemas.

## Validações antes de entregar o relatório

- [ ] Autorização e escopo confirmados na primeira interação.
- [ ] Retenção de cada log verificada; evidência da janela suspeita exportada.
- [ ] Os 5 sinais foram checados por conta sensível (ou o motivo de pular está registrado).
- [ ] Cadência medida por script, não por impressão.
- [ ] Cada veredito tem a evidência que o sustenta.
- [ ] Nenhuma acusação a pessoa; achados são sobre contas.
- [ ] Contas comprometidas têm o playbook aplicado na ordem.
- [ ] Relatório segue o template e registra limitações e risco residual.

## Tratamento de exceções

### O log já expirou

Registrar a janela perdida como limitação. Verificar se o sistema tem trilha
persistida (relatórios de auditoria, histórico de ações) que sobreviva à retenção
do log de acesso — muitas vezes a **ação** fica registrada mesmo quando o login some.

### O sistema não mostra IP/log de acesso

Escalar para o suporte/administrador do sistema pedindo o relatório de acessos da
conta. Registrar a lacuna. Considerar migrar funções sensíveis para sistemas que
deem trilha de auditoria.

### O titular da conta reconhece a automação

Então não é invasão — é **automação não autorizada por política**: alguém do time
plugou um robô/integração com a própria senha. Ainda assim: substituir senha
pessoal por credencial de integração própria (API key/conta de serviço com menor
privilégio), para que a automação não carregue a chave da conta de uma pessoa.

### Suspeita recai sobre funcionário ou ex-funcionário

Preservar evidência, conter a conta, e tratar o enquadramento com cautela: a
evidência técnica prova **automação com aquela credencial** — não prova quem a
operou nem intenção. O termo correto é "acesso não autorizado"; a autoria é questão
jurídica, não técnica. Ver a seção de enquadramento no playbook.

## Examples

### Exemplo 1 — início obrigatório

**Usuário:** "Acho que mexeram no meu ERP."

**Resposta da skill:** perguntar quais sistemas estão em escopo e confirmar
autorização — e, confirmada a suspeita ativa, orientar exportar os logs ANTES de
qualquer análise ou mudança de senha.

### Exemplo 2 — datacenter vs. VPN

**Contexto:** sócia com logins diários de um IP cujo ASN é de nuvem.

**Comportamento esperado:** não concluir comprometimento; perguntar se o escritório
usa VPN corporativa. Se usar, o IP de nuvem é esperado. Se não usar, subir para
Suspeita e cruzar com cadência e tipo de login.

### Exemplo 3 — metrônomo

**Contexto:** conta com renovação de acesso a cada 60 minutos, desvio de segundos,
por 3 dias seguidos — madrugadas incluídas.

**Comportamento esperado:** rodar `cadencia.py`, anexar a saída como evidência,
classificar Comprometida (cadência + continuidade impossível para humano) e aplicar
o playbook na ordem.

## Recursos

- [references/sinais-de-automacao.md](references/sinais-de-automacao.md) — os 5 sinais em profundidade, com "como verificar".
- [references/onde-olhar-logs.md](references/onde-olhar-logs.md) — onde cada sistema guarda o log de acesso e por quanto tempo.
- [references/playbook-resposta.md](references/playbook-resposta.md) — contenção na ordem certa, evidência e enquadramento.
- [assets/relatorio-verificacao-template.md](assets/relatorio-verificacao-template.md) — estrutura do relatório final.
- `scripts/cadencia.py` — detector determinístico de cadência robótica.

## Skill irmã

Esta skill detecta **quem está operando** suas contas. Para descobrir **o que ficou
exposto** num app que você construiu com IA, use a
[rdd-appsec-mentor](https://github.com/robertodiasduarte/rdd-appsec-mentor).
