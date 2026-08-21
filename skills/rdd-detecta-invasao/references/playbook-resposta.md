# Playbook de resposta — conta comprometida

A ordem importa. Cada passo existe por causa de um erro que alguém já cometeu.

## Passo 0 — NÃO faça isto primeiro

- **Não troque a senha antes de preservar a evidência.** Ações de contenção podem
  apagar rastros (sessões deletadas levam junto o user-agent; logs continuam
  expirando enquanto você age).
- **Não confronte o suspeito antes de conter.** Se a automação for de alguém com
  acesso, o aviso antecipado dá tempo de apagar rastro.
- **Não delete nada.** Contenção é revogar e bloquear — nunca apagar.

## Passo 1 — Preservar evidência (minutos, não horas)

1. Exporte o log de acesso de cada sistema afetado (CSV, PDF, prints datados).
2. Capture: IPs de origem, resultado do whois/ASN de cada um, user-agents,
   timestamps dos eventos, e a saída do `cadencia.py` se houver série temporal.
3. Liste o que a conta **fez** na janela suspeita: leituras em massa, escritas,
   aprovações, exportações — com data e hora.
4. Guarde tudo fora do sistema afetado (se o invasor tem acesso, tem acesso ao
   que você salvar lá dentro).
5. Anote a retenção de cada log e o que já pode ter sido perdido.

## Passo 2 — Trocar a senha (antes de revogar sessões)

Se há sinal de login por senha em cadência (sinal 2), a automação **tem a senha**.
Revogar sessões primeiro é enxugar gelo: o script reloga em minutos. A ordem é:

1. **Trocar a senha** da conta comprometida (forte, única, nunca reutilizada).
2. **Depois** revogar todas as sessões e tokens ativos.
3. Confirmar, no log, que novas tentativas da origem suspeita passam a **falhar** —
   essa falha registrada também é evidência.

## Passo 3 — Revogar o resto

- Sessões ativas e dispositivos conectados (todos — o legítimo reloga).
- Tokens de API, chaves de integração e "app passwords" emitidos pela conta.
- Aplicativos de terceiros autorizados (OAuth) que ninguém reconhece.
- Procurações e delegações (crítico no e-CAC: revogar procuração indevida).

## Passo 4 — Fechar a porta de entrada

1. **Ativar 2FA** na conta afetada — e nos papéis sensíveis todos, já que a
   investigação está aberta.
2. Verificar se a mesma senha era usada em outros sistemas (reutilização é a
   regra, infelizmente) — trocar em todos.
3. Se o e-mail da pessoa também mostra sinal: tratar o e-mail PRIMEIRO (quem tem o
   e-mail reseta o resto).
4. Revisar contas de recuperação, telefones e e-mails secundários cadastrados —
   invasor persistente troca o canal de recuperação para voltar depois.

## Passo 5 — Dimensionar o dano

Com a evidência do Passo 1, responder:

- **O que foi lido?** Se dados de clientes saíram (sinal 4), há potencial dever de
  comunicação à ANPD e aos titulares (LGPD, art. 48) — prazo e obrigação dependem
  do risco; envolva o jurídico.
- **O que foi escrito/aprovado/enviado?** Listar cada ação da janela para decidir
  o que reverter — com registro, não silenciosamente.
- **Desde quando?** A primeira ocorrência do padrão define a janela real (pode ser
  bem anterior à descoberta).

## Passo 6 — Enquadramento (com o jurídico)

- A evidência técnica prova **automação operando com aquela credencial** — não
  prova quem operou nem intenção.
- Se a credencial era de funcionário/prestador e o uso violou a política: o
  enquadramento é **"acesso não autorizado"** / violação contratual — não
  "invasão criminosa por terceiro". A diferença muda a peça jurídica inteira.
- Se o titular nega e há indício de terceiro: registre boletim/notifique com a
  evidência preservada, sem afirmar autoria.
- Formalize por escrito com quem for da conta: rescisão, notificação ou
  regularização (se era automação interna sem autorização, ver abaixo).

## Caso especial — a automação era "da casa"

Se o titular reconhece ("é um robô que eu configurei pra puxar os relatórios"):

1. Não é invasão — é automação fora de política, com um risco real: a senha
   pessoal embutida num script.
2. Migrar para credencial própria de integração: API key ou conta de serviço,
   com **menor privilégio** (só o que o robô precisa) e revogável sem afetar a pessoa.
3. Registrar a automação num inventário: dono, o que acessa, com que credencial.
4. Trocar a senha pessoal que estava no script (ela circulou por código, logs,
   repositórios — considere-a vazada).

## Depois do incidente

- Rodar a verificação completa (os 5 sinais) nas demais contas sensíveis — quem
  compromete uma conta costuma testar outras.
- Agendar a varredura mensal de cadência/origem nas contas sensíveis.
- Repassar o inventário de sistemas: qual não tem log? qual não tem 2FA? qual
  tem privilégio além do necessário? Cada "sim" é a próxima porta.
