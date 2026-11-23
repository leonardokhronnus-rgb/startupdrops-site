# Modelo de drop

Cada drop é um arquivo `.md` dentro da pasta `content/`, com nome `AAAA-MM-DD-assunto.md`.
O cabeçalho fica entre as linhas `---`. Depois dele vem o texto, em Markdown.

```
---
titulo: Título do drop
linha_fina: Uma ou duas frases que resumem e dão contexto.
editoria: rodadas          # rodadas | modelos | economia | artigos
formato: coluna            # só em artigos: coluna | leitura | playbook | dados
data: 2026-11-11 09:00
autor: Leonardo Brasil     # opcional (padrão: Redação StartupDrops)
setor: Fintech             # opcional: só use quando acrescentar informação (setor da rodada, tema do artigo)
imagem: /static/img/2026-11-11-assunto.jpg   # opcional; sem imagem, o site mostra o bloco com o símbolo
simbolo: 2,7×              # opcional: texto curto do bloco visual (ex.: YC↗, 13,75%, R$30M)
credito_imagem: Ilustração StartupDrops      # opcional
fonte: Pipeline Valor      # quem apurou
link_fonte: https://...    # link para o original
valor: R$ 30 milhões       # rodadas: valor da rodada ou da transação
valuation: R$ 150 milhões  # rodadas: valuation, se divulgado ou estimado
deal_da_semana: true       # marca o Deal da Semana (aparece em destaque na home)
leitura_valuation: Texto da leitura de valuation do deal.
empresas: [Empresa A, Fundo B]
destaque: true             # coloca o drop como manchete da home
na_pratica: O que muda para o fundador e o que ele pode fazer.
posicao: manchete         # opcional: manchete | lateral-1 | lateral-2 | card-1 ... card-9
rascunho: true             # opcional: não publica enquanto estiver true
---
A notícia: o que aconteceu, quem, quanto e quando. Dois ou três parágrafos curtos.

## Por que importa?
O que esse fato diz sobre o mercado e por que o fundador deveria se importar.
```

## Estrutura das matérias (Deals, Tendências, Economia)

Toda matéria segue a mesma ordem na página:

1. **A notícia**: o texto logo depois do cabeçalho.
2. **Por que importa**: a seção `## Por que importa?`.
3. **Insight**: o campo `na_pratica`, que aparece na faixa destacada com o título INSIGHT.
4. **Fonte**: os campos `fonte` e `link_fonte`, que aparecem no fim como "Com informações de ...".

O site não publica uma matéria dessas editorias se faltar qualquer uma das quatro partes. No Deal da Semana, a leitura de valuation entra entre "Por que importa" e "Insight".

Artigos (colunas, leituras, playbooks) têm estrutura livre.
