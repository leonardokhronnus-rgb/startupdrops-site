---
titulo: "Virar conector em vez de concorrente: como pequenas empresas estão ganhando distribuição dentro das grandes plataformas de IA"
linha_fina: O caso da Jusratio, que entrou na Harvey com seis meses de vida, mostra um canal de venda novo. Com o protocolo MCP, quem tem dados ou serviços de nicho pode aparecer dentro do Claude, do ChatGPT e de plataformas setoriais. O que é, por que funciona e os cuidados.
editoria: artigos
formato: playbook
data: 2026-11-25 08:35
setor: 6 min de leitura
simbolo: MCP
fonte: StartupDrops, com base em Brasil Inovador e documentação do Model Context Protocol
link_fonte: https://brasilinovador.com.br/jusratio-integra-plataforma-norte-americana-harvey-e-amplia-presenca-de-dados-juridicos-brasileiros-em-inteligencia-artificial/
empresas: [Jusratio, Harvey, Anthropic, OpenAI]
na_pratica: "Liste os dados ou serviços que só a sua empresa tem e que um assistente de IA precisaria para responder bem a uma pergunta do seu cliente. Se a lista tiver pelo menos um item forte, peça a um desenvolvedor uma estimativa para criar um conector MCP simples, só de leitura, e teste com cinco clientes que já usam Claude ou ChatGPT no trabalho. Meça quantas consultas eles fazem por semana antes de investir mais."
imagem: /static/img/drops/2026-11-25-conector-como-canal.jpg
credito_imagem: "Ilustração StartupDrops"
---
Durante muito tempo, a pergunta de toda startup diante de um gigante de tecnologia era a mesma: como competir com ele? A inteligência artificial está criando uma alternativa mais barata e, em muitos casos, mais inteligente: em vez de competir, entrar dentro dele.

A notícia de hoje sobre a Jusratio é um bom exemplo. Uma legaltech brasileira fundada em maio, com sete funcionários, virou conector oficial da Harvey, uma plataforma de IA jurídica avaliada em US$ 15,5 bilhões. Advogados que usam a Harvey agora consultam a base da Jusratio, com mais de 51 milhões de decisões e normas brasileiras, sem sair da ferramenta. Antes disso, a empresa já tinha conectores para o Claude e o ChatGPT.

Para entender por que isso funciona, e se faz sentido para a sua empresa, vale olhar como esse canal é construído.

## O que é um conector

Os assistentes de IA, como Claude e ChatGPT, são ótimos em raciocinar e escrever, mas não sabem tudo. Não têm acesso à jurisprudência atualizada de um tribunal brasileiro, ao estoque de uma distribuidora ou ao histórico de um cliente num sistema de gestão. Para isso, precisam se conectar a fontes de dados e ferramentas externas.

O MCP, sigla para Model Context Protocol, é um padrão aberto criado para essas conexões. Funciona como uma tomada universal: quem cria um conector MCP uma vez consegue ligá-lo a vários assistentes e plataformas, sem construir uma integração diferente para cada um. Foi isso que permitiu a uma empresa de sete pessoas estar em três plataformas diferentes em poucos meses.

## Por que esse canal é poderoso

**O cliente já está lá.** O advogado que usa a Harvey não precisa abrir outro site, criar outra conta ou aprender outra ferramenta. A informação aparece no meio do trabalho dele. Isso reduz drasticamente o atrito de adoção, que é o maior custo de venda de qualquer software.

**A plataforma faz o marketing.** Entrar na biblioteca oficial de conectores de uma plataforma grande funciona como uma vitrine. Cada novo cliente da plataforma vira um cliente potencial do conector.

**Você vende o que é difícil de copiar.** A Harvey pode melhorar o raciocínio do modelo todo mês, mas organizar 51 milhões de documentos de 130 tribunais brasileiros é trabalho local, chato e demorado. É exatamente o tipo de ativo que a IA valoriza e que um gigante de fora prefere comprar ou conectar a construir.

**Custa pouco para começar.** Um conector simples, só de leitura, pode ser feito em dias ou semanas por um desenvolvedor, muito menos que um produto completo com interface própria.

## Quem pode usar essa estratégia

O modelo funciona melhor para três tipos de empresa:

1. **Donos de dados de nicho.** Bases jurídicas, fiscais, regulatórias, de preços, de crédito, de imóveis, do agro. Quanto mais local e mais difícil de organizar, melhor.
2. **Donos de sistemas onde o trabalho acontece.** ERPs, CRMs, sistemas de gestão de clínicas, de escolas, de transportadoras. Um conector permite que o cliente pergunte ao assistente sobre os próprios dados.
3. **Donos de serviços que podem ser acionados.** Emissão de nota fiscal, consulta de CNPJ, cotação de frete, agendamento. O assistente pode executar a tarefa em nome do usuário.

## Os riscos e cuidados

Não é um caminho sem riscos, e vale pesar três deles:

- **Dependência da plataforma.** Se o seu principal canal é a biblioteca de um terceiro, ele controla a sua visibilidade e pode mudar as regras ou construir algo parecido. A Jusratio reduz esse risco estando em várias plataformas ao mesmo tempo, e você deveria fazer o mesmo.
- **Como cobrar.** O conector precisa estar ligado a uma conta paga na sua empresa. A Jusratio, por exemplo, exige que cada advogado vincule suas próprias credenciais e vende planos por créditos e assinaturas corporativas. Sem isso, você vira um fornecedor gratuito de dados para a plataforma.
- **Qualidade e responsabilidade.** Quando a IA usa os seus dados para responder, um erro na sua base vira um erro na resposta. Links para a fonte original, como faz a Jusratio, ajudam o usuário a conferir e protegem a sua reputação.

## Como começar

1. **Escolha um caso de uso só,** a pergunta mais frequente que os seus clientes fariam a um assistente de IA sobre o seu domínio.
2. **Crie um conector só de leitura,** que responde a essa pergunta com os seus dados e devolve o link da fonte.
3. **Teste com poucos clientes** que já usam Claude ou ChatGPT no trabalho e meça o uso real por semana.
4. **Ligue o uso a uma conta paga** desde o primeiro dia, mesmo que com um período gratuito.
5. **Só depois tente as bibliotecas oficiais** das plataformas setoriais, já com números de uso para mostrar.

A lição do caso Jusratio vai além do jurídico. Na era dos assistentes de IA, a pergunta para muitas empresas pequenas deixa de ser "como eu atraio o cliente para o meu site" e passa a ser "como eu apareço no lugar onde o cliente já está trabalhando".
