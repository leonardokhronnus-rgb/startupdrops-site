# StartupDrops

O que um fundador precisa ler: rodadas, modelos de negócio, economia e as melhores ideias do mundo, com a leitura de quem vive o mercado.

Tudo passa por curadoria. Não há robô publicando sozinho.

## Como funciona

- Cada drop é um arquivo `.md` em `content/` (formato em `MODELO.md`).
- A cada alteração no repositório, o GitHub monta o site (`build.py`) e publica no GitHub Pages em 1 a 2 minutos.
- Se algum drop tiver erro no cabeçalho, a publicação para e o erro aparece na aba Actions, sem derrubar o site no ar.

## Editorias

| Editoria | O que entra |
|---|---|
| Deals | Rodadas e aquisições com sinal. Uma por semana vira o **Deal da Semana**, com leitura de valuation. |
| Tendências | Como as empresas estão ganhando dinheiro, teses de fundos e estratégia das big techs. |
| Economia | Juros, crédito, impostos e regulação, sempre com o "Na prática, para você". |
| Artigos | Coluna, Leitura da semana, Playbook e Dados (campo `formato`). |

## Imagens

Coloque a ilustração em `static/img/` e informe o caminho no campo `imagem`. Sem imagem, o site mostra um bloco tipográfico na cor da editoria com o texto do campo `simbolo` (ex.: YC↗, 13,75%, R$30M).

## Patrocinadores

Edite `PATROCINADORES` em `config.py`. Com a lista vazia, a home mostra o convite "Seja patrocinador".

## Colocar no ar (uma vez)

1. Suba estes arquivos no repositório `startupdrops`.
2. Em *Settings → Pages → Source*, escolha **GitHub Actions**.
3. Pronto: cada novo drop publicado no repositório vai ao ar sozinho.

## Educação

Os drops de educação ficam em `content/educacao.json` (módulos e dicas). A home mostra 3 dicas que mudam todo dia.

## Conteúdo patrocinado

Use `patrocinado: true`, `patrocinador:`, `aviso:` (conflito de interesse, quando houver), `link_cta:` e `texto_cta:` no cabeçalho do drop. O site identifica a matéria como publicidade em todos os lugares onde ela aparece.

## Antes de lançar

- `config.py`: preencha `contato_email` (página de privacidade) e um dos campos de `ANALYTICS`.
- `content/2026-11-11-startuphero-patrocinado.md`: preencha `link_cta` com o site da StartupHero.

## Painel de edição

O site tem um painel visual pelo Pages CMS (grátis, sem servidor):

1. Entre em https://app.pagescms.org com a sua conta do GitHub.
2. Autorize o acesso ao repositório `startupdrops`.
3. Em **Matérias e artigos** você cria, edita e apaga drops. Em **Conteúdo patrocinado**, os patrocinados.
4. O campo **Posição na home** decide o que vai na manchete, nos dois cards laterais e nos primeiros cards. Vale também para patrocinados.
5. Ao salvar, o GitHub publica o site sozinho em cerca de 1 minuto.

A configuração do painel fica em `.pages.yml`.

## Audiência

O site está pronto para o Umami (grátis até 100 mil eventos por mês, sem cookies):

1. Crie a conta em https://cloud.umami.is e adicione o site `startupdrops.com.br`.
2. Copie o **Website ID** e cole em `config.py`, no campo `umami_website_id`.

O Umami mostra visitantes, páginas vistas, de onde veio o tráfego e os cliques marcados no site: botões dos patrocinados (`cta-patrocinado`), links para a fonte original (`fonte-original`), "Quero anunciar" (`anuncie-home`) e o formulário da newsletter (`newsletter-home`).
