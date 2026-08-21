# Os 5 sinais de acesso automatizado

Cada sinal abaixo vem de casos reais de contas operadas por automação não
autorizada. Nenhum depende de ferramenta cara: todos podem ser verificados com o
log de acesso do próprio sistema e um navegador.

---

## Sinal 1 — Origem de datacenter (o pivô mais forte)

**O que é:** o IP de onde o login veio pertence a um provedor de nuvem/datacenter
— não a uma operadora residencial ou móvel.

**Por que funciona:** o user-agent (o "navegador" que aparece no log) é um texto
que o cliente escolhe enviar. Um script se apresenta como
`Chrome/151.0 (X11; Linux x86_64)` sem ser Chrome nem ter tela. Já o IP de origem
é infraestrutura: pessoa física loga da Vivo, Claro, Oi, TIM, de fibra local ou do
4G/5G. Script roda em servidor — AWS, Hetzner, OVH, Google Cloud, Azure,
DigitalOcean, Vultr, Contabo, Linode.

**Como verificar:**

1. Pegue os IPs dos últimos logins da conta no log de acesso do sistema.
2. Consulte o dono do IP: `whois <ip>` no terminal, ou bgp.he.net / ipinfo.io no
   navegador. O campo que interessa é a **organização/ASN** (ex.: "AS16509
   Amazon.com, Inc." = datacenter; "AS26599 Telefônica Brasil" = residencial).
3. Classifique cada IP: residencial/móvel · corporativo conhecido · datacenter.

**Falsos positivos conhecidos:**

- **VPN corporativa** — se o escritório usa VPN que sai por nuvem, todo login
  legítimo parece datacenter. Pergunte antes de concluir.
- **Internet via satélite (Starlink)** — as faixas da SpaceX parecem exóticas mas
  são acesso residencial legítimo, não datacenter operado por bot.
- **iCloud Private Relay / proxies de privacidade** — usuários de iPhone/Safari
  podem sair por IPs da Apple/Cloudflare.

Por isso: origem de datacenter **isolada** = Suspeita. Cruzada com cadência ou
tipo de login = confirmação.

---

## Sinal 2 — Senha em claro na automação

**O que é:** logins repetidos com **usuário e senha** (não renovação de token, não
SSO) em intervalos regulares.

**Por que importa:** sistemas modernos autenticam uma vez por senha e depois
renovam a sessão por token. Se o log mostra autenticação por senha a cada 10, 30,
60 minutos, o cliente não está "lembrando" a sessão — está **relogando com a senha
digitada em código**. Ou seja: quem opera a automação **possui a senha em claro**.

**Consequência prática (a mais ignorada):** derrubar a sessão não contém nada.
O script reloga no minuto seguinte. A contenção real é **trocar a senha** — e só
depois revogar sessões e tokens (ordem no playbook).

**Como verificar:** no log de auth, distinga o tipo de evento — "login com senha" /
"password grant" vs. "token renovado" / "refresh". Senha repetida em cadência =
sinal confirmado.

---

## Sinal 3 — Cadência robótica (metrônomo)

**O que é:** eventos de login/renovação em intervalo cravado — por exemplo, a cada
58 minutos, com desvio de segundos — mantidos por **muitas horas contínuas**,
madrugadas incluídas.

**Por que funciona:** humano é irregular. Fecha o laptop, almoça, pega trânsito,
troca do desktop pro celular, dorme. Máquina agenda `sleep(3600)` e cumpre.
A assinatura estatística é **desvio-padrão baixo em série longa**.

**Como verificar:**

1. Exporte os timestamps dos eventos da conta (um por linha, qualquer formato de
   data razoável).
2. Rode `python scripts/cadencia.py arquivo.txt`.
3. O script mede intervalo médio, desvio e continuidade, e dá o veredito.

**Calibração importante (aprendida em caso real):** o limiar precisa ser **dezenas
de eventos contínuos** (o script usa 36 — aproximadamente um dia e meio no ritmo de
1/hora). Limiar baixo (ex.: 10 eventos) marca qualquer aba de navegador aberta
durante o expediente — falso positivo em massa. Aba aberta renova bonitinho das 9h
às 18h e **para**; bot atravessa a madrugada.

---

## Sinal 4 — Extração em massa

**O que é:** a mesma conta lendo coleções inteiras de dados — lista completa de
clientes, todos os documentos, todas as conversas — repetidas vezes, em sequência.

**Por que importa:** mesmo sem alterar nada, é scraping: alguém está **copiando a
sua base** para fora (dados de clientes = responsabilidade LGPD do escritório).
Leitura não deixa "estrago" visível, então passa despercebida por meses.

**Como verificar:** procure no log de atividade acessos em série às mesmas telas de
listagem/relatório/exportação, com paginação sistemática, volume muito acima do
uso de trabalho, repetido dia após dia. Cruze com o sinal 1 e 3: scraper quase
sempre vem de datacenter e opera em cadência.

---

## Sinal 5 — Ação fora de horário / em lote

**O que é:** escritas — aprovações, envios, alterações — em rajadas de segundos,
de madrugada ou fim de semana, sem expediente que explique.

**Por que importa:** é o sinal de que a automação **age** em nome da conta, não só
lê. Aprovar 15 itens em 40 segundos às 3h da manhã não é gente.

**Cuidado com o falso positivo:** lote às 14h de terça pode ser trabalho humano
legítimo em série (revisão acumulada). O que denuncia a máquina é a **combinação**:
rajada + horário morto + regularidade + (frequentemente) origem de datacenter.

---

## Regra de decisão

| Evidência | Veredito |
|---|---|
| Nenhum sinal | Limpa |
| 1 sinal, com explicação plausível pendente | Suspeita — investigar antes de agir |
| 2+ sinais na mesma conta | Comprometida — aplicar o playbook |
| 1 sinal + ação que o titular nega | Comprometida — aplicar o playbook |

O achado é sempre sobre a **conta**, nunca acusação a pessoa: o titular pode ser a
maior vítima (senha vazada) — ou pode ter plugado a automação ele mesmo. Autoria é
questão jurídica; a evidência técnica prova automação, não intenção.
