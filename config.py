"""Configuração do StartupDrops."""

SITE = {
    "name": "StartupDrops",
    "slogan": "O essencial do ecossistema, todo dia",
    "tagline": "O que um fundador precisa ler: rodadas, modelos de negócio, economia e as melhores ideias do mundo, com a leitura de quem vive o mercado.",
    "url": "https://startupdrops.com.br",   # troque quando o domínio estiver apontado
    "linkedin": "",
    "instagram": "",
    "newsletter_action": "https://buttondown.com/api/emails/embed-subscribe/startupdrops",  # vazio esconde o bloco
    "per_page": 20,
    "contato_email": "contato@startupdrops.com.br",
    "whatsapp": "5521959257362",
    "whatsapp_exibir": "(21) 95925-7362",
    "responsavel": "Elevu Design",
    "cnpj": "28.810.456/0001-36",
    "endereco": "Av. Ataulfo de Paiva, 1235, Sala 303/365, Leblon Office Tower, Leblon, Rio de Janeiro, RJ, 22440-034",
}

# Medição de audiência sem cookies (não exige aviso de cookies). Preencha UM dos dois.
ANALYTICS = {
    # Umami (recomendado): visitantes, páginas, origem do tráfego e cliques, sem cookies.
    # Crie a conta grátis em cloud.umami.is, adicione o site e cole aqui o "Website ID".
    "umami_website_id": "",
    "cloudflare_token": "",   # Cloudflare Web Analytics (grátis): token do snippet
    "plausible_domain": "",   # Plausible: ex. startupdrops.com.br
}

# Editorias. A cor também é usada nas capas automáticas (quando o drop não tem imagem).
EDITORIAS = {
    "rodadas": {
        "nome": "Deals",
        "cor": "#c0392b",
        "descricao": "Captações, aquisições e fusões: quem levantou dinheiro, quem comprou quem e o que isso sinaliza.",
    },
    "modelos": {
        "nome": "Tendências",
        "cor": "#6d28d9",
        "descricao": "Como as empresas estão ganhando dinheiro agora e para onde vão o capital e a tecnologia.",
    },
    "economia": {
        "nome": "Economia",
        "cor": "#b45309",
        "descricao": "Juros, crédito, câmbio, impostos e regulação: o que muda no caixa e no valuation da sua empresa.",
    },
    "artigos": {
        "nome": "Artigos",
        "cor": "#1d4ed8",
        "descricao": "A coluna da semana, os melhores ensaios do mundo comentados e playbooks para aplicar.",
    },
}

# Formatos dentro de Artigos (campo "formato" do drop)
FORMATOS = {
    "coluna": "Coluna",
    "leitura": "Leitura da semana",
    "playbook": "Playbook",
    "dados": "Dados",
}

# Patrocinadores (faixa de logos na home). Deixe a lista vazia para mostrar o convite "Seja patrocinador".
# Exemplo: {"nome": "Empresa X", "url": "https://...", "logo": "/static/img/patrocinadores/x.svg"}
PATROCINADORES = []

AUTOR_PADRAO = "Redação StartupDrops"
