# Relatório de verificação de acessos — [escritório/empresa]

- **Data da verificação:**
- **Responsável / autorizado por:**
- **Janela analisada:** [de — até]
- **Motivo:** [rotina preventiva | suspeita: descrever]

## 1. Escopo e limitações

| Sistema | Log disponível? | Mostra IP? | Retenção | Exportado? | Janela coberta |
|---|---|---|---|---|---|
| | | | | | |

Limitações (logs expirados, sistemas sem trilha, contas fora do escopo):

## 2. Contas verificadas

| Conta / papel | Sinal 1 (ASN) | Sinal 2 (senha) | Sinal 3 (cadência) | Sinal 4 (extração) | Sinal 5 (lote/horário) | Veredito |
|---|---|---|---|---|---|---|
| | | | | | | Limpa / Suspeita / Comprometida |

Preencher cada célula com ✅ (limpo), ⚠️ (indício, descrever) ou 🔴 (confirmado,
evidência anexa). Veredito segue a regra de decisão: 2+ sinais = Comprometida;
1 sinal sem explicação = Suspeita.

## 3. Evidências

Para cada ⚠️/🔴: o que foi observado, onde, print/export anexo, saída do
`cadencia.py` quando houver série temporal. Identificar contas, nunca acusar
pessoas.

## 4. Ações executadas (contas Comprometidas)

| # | Ação | Conta | Quando | Confirmação |
|---|---|---|---|---|
| 1 | Evidência preservada | | | |
| 2 | Senha trocada | | | |
| 3 | Sessões/tokens revogados | | | |
| 4 | 2FA ativado | | | |
| 5 | Integrações/procurações revisadas | | | |

## 5. Dano dimensionado

- Dados lidos/extraídos (avaliar dever LGPD com o jurídico):
- Ações escritas na janela (o que reverter, com registro):
- Janela real do padrão (primeira ocorrência):

## 6. Prevenção agendada

- [ ] 2FA nos papéis sensíveis
- [ ] Alerta de login de datacenter (onde o sistema permitir)
- [ ] Varredura mensal de cadência/origem agendada para: ___
- [ ] Revisão de privilégios (quem tem mais acesso do que a função exige)
- [ ] Inventário de automações internas (dono, acesso, credencial)

## 7. Risco residual

O que esta verificação NÃO cobre e por quê (sistemas sem log, janelas expiradas,
sinais não verificáveis). Nenhuma verificação prova ausência de comprometimento —
prova apenas o que foi olhado, na janela olhada.
