# Onde cada sistema guarda o log de acesso (e por quanto tempo)

A pergunta número 1 de qualquer verificação é: **quanto tempo o log dura?**
Retenção curta é a regra, não a exceção. Se há suspeita ativa, exporte primeiro,
analise depois — o rastro de ontem pode não existir amanhã.

> Os caminhos abaixo são os vigentes na data de escrita; menus mudam. Se o caminho
> não bater, procure por "auditoria", "atividade", "login history" ou "security log"
> na documentação do produto.

## Google Workspace (Gmail/Drive corporativo)

- **Onde:** Admin console → Relatórios → Auditoria e investigação → *Eventos de
  login*. Mostra IP, horário, tipo de login, sucesso/falha e desafios de 2FA.
- **Retenção:** ~6 meses para eventos de auditoria (planos variam).
- **O que olhar:** IPs de origem por usuário (sinal 1), logins "suspeitos" já
  marcados pelo Google, horários (sinal 5). Alertas administrativos podem ser
  configurados em Regras.
- **Extra:** Conta do usuário → Segurança → "Seus dispositivos" lista sessões vivas.

## Microsoft 365 / Entra ID

- **Onde:** entra.microsoft.com → Usuários → *Sign-in logs* (ou Monitoramento →
  Entrada). Mostra IP, cliente/app, localização, e se foi login interativo ou
  não-interativo (automação aparece como não-interativo).
- **Retenção:** 7 dias no plano gratuito do Entra; ~30 dias em P1/P2. **Curta — exportar.**
- **O que olhar:** logins não-interativos que você não reconhece, IPs de nuvem,
  "legacy authentication" (protocolos antigos sem 2FA — desative).

## e-CAC / serviços gov.br (o mais sensível do escritório)

- **Onde:** o e-CAC não expõe um log de acessos rico ao usuário. O ponto de
  controle real são as **procurações eletrônicas**: e-CAC → Senhas e Procurações.
  Revise QUEM tem procuração de cada cliente e com que poderes. No gov.br, a área
  "Privacidade" da conta mostra histórico de logins e aplicativos autorizados.
- **O que olhar:** procurações que ninguém lembra de ter outorgado, aplicativos
  autorizados desconhecidos, certificados digitais emitidos/renovados fora do seu
  controle. Acesso indevido aqui raramente aparece como "login estranho" — aparece
  como **poder delegado que não deveria existir**.

## ERP contábil / portal do cliente (Domínio, Omie, Conta Azul, etc.)

- **Onde:** varia. Procure "log de auditoria", "histórico de acessos" ou
  "atividades do usuário" nas configurações de administrador. Nem todos mostram IP.
- **Se não houver log acessível:** peça ao suporte o relatório de acessos da conta
  — formalize por escrito (vira evidência). Registre a lacuna no relatório; trilha
  de auditoria deve pesar na escolha do fornecedor.
- **O que olhar:** exportações/relatórios em série (sinal 4), ações administrativas
  fora de horário (sinal 5), usuários criados que ninguém reconhece.

## Apps próprios criados com IA (Supabase e similares)

Se você construiu um app com Lovable/vibe coding sobre Supabase (ou stack parecida),
você é o administrador — e tem mais visibilidade do que imagina:

- **Logs de auth:** Dashboard → Logs → Auth. Mostra cada login/renovação com IP e
  user-agent. **Retenção no plano gratuito: ~24 horas** — a mais curta desta lista.
  Suspeita ativa = exportar imediatamente.
- **Sessões persistidas:** as tabelas de sessão do próprio Postgres (`auth.sessions`,
  `auth.refresh_tokens`) sobrevivem à retenção do log — dá para ver sessões antigas,
  user-agent e cadência de renovação por conta mesmo depois do log expirar.
- **O que olhar:** `grant_type=password` repetido (sinal 2), IPs de datacenter
  (sinal 1), contas com dezenas de sessões, cadência de refresh (sinal 3 — rode o
  `cadencia.py` sobre os timestamps).
- **Cuidado:** ao conter, não delete as sessões antes de exportá-las — deletar
  sessão apaga o user-agent que estava guardado nela.

## Cloudflare (se seus domínios/apps passam por ele)

- **Onde:** dash.cloudflare.com → Analytics & Logs. No plano gratuito a análise é
  agregada; logs por requisição exigem plano pago.
- **O que olhar:** picos de tráfego de um único IP/ASN, países inesperados,
  user-agents de bot. Regras de firewall permitem **alertar ou desafiar** (CAPTCHA)
  tráfego de datacenter — útil como prevenção para rotas de login.

## WhatsApp Business / e-mail pessoal do escritório

- **WhatsApp:** Configurações → Dispositivos conectados — qualquer aparelho que
  você não reconhece é sessão de terceiro. Remova e reative o 2FA (PIN).
- **E-mail (qualquer provedor):** procure "atividade da conta" / "últimos acessos".
  E-mail comprometido é o mais grave dos comprometimentos: quem tem o e-mail
  reseta a senha de todo o resto.

## Regra transversal

Para **cada** sistema do inventário, anote no relatório: onde está o log, retenção,
se mostra IP, se foi exportado e a janela coberta. Sistema sem trilha nenhuma é um
achado por si só — entra como risco no relatório final.
