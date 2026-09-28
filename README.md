# # 🔍 LeadGenerator

> Ferramenta de terminal para prospecção de clientes através de automação do Google Maps.

O **LeadGenerator** é uma ferramenta desenvolvida em Python para encontrar potenciais clientes para serviços de criação de sites.

A aplicação automatiza pesquisas no **Google Maps** utilizando **Playwright**, coleta informações públicas das empresas encontradas e organiza os resultados em arquivos CSV.

O principal objetivo é facilitar a identificação de empresas que podem representar oportunidades comerciais, especialmente negócios que **ainda não possuem um site próprio**.

---

## 🚀 Funcionalidades

* 🔎 Pesquisa automatizada no Google Maps
* 🤖 Automação do navegador com Playwright
* 🏢 Coleta do nome das empresas
* 🌐 Identificação de empresas com ou sem site
* 📞 Extração do telefone disponível no Google Maps
* 🔗 Coleta do link da empresa no Google Maps
* 📊 Visualização dos leads diretamente no terminal
* 💾 Salvamento automático dos leads em CSV
* ♻️ Deduplicação de empresas
* 🎯 Filtro específico para empresas sem site
* 📁 Exportação de oportunidades para um CSV separado
* 🧹 Limpeza do banco de leads
* 🖥️ Interface de terminal utilizando Rich

---

## 🧠 Como funciona

O fluxo básico da ferramenta é:

```text
                    ┌─────────────────┐
                    │   LeadGenerator │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Usuário informa     │
                  │ termo de pesquisa   │
                  └─────────┬───────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │ Google Maps         │
                  │ + Playwright        │
                  └─────────┬───────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │ Empresas encontradas│
                  └─────────┬───────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │ Extração de informações    │
              │                            │
              │ • Empresa                  │
              │ • Site                     │
              │ • Telefone                 │
              │ • Link do Maps             │
              │ • Termo pesquisado         │
              └────────────┬───────────────┘
                           │
                           ▼
                  ┌─────────────────────┐
                  │ Identificação de    │
                  │ empresas sem site   │
                  └─────────┬───────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │ leads_encontrados   │
                  │ .csv                │
                  └─────────────────────┘
```

---

## 🛠️ Tecnologias

| Tecnologia  | Utilização                         |
| ----------- | ---------------------------------- |
| Python      | Linguagem principal                |
| Playwright  | Automação do navegador             |
| Chromium    | Navegador automatizado             |
| Pandas      | Manipulação e exportação dos dados |
| Rich        | Interface visual no terminal       |
| Google Maps | Fonte das informações públicas     |

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/LeadGenerator.git
cd LeadGenerator
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install pandas playwright rich
```

### 5. Instale o Chromium do Playwright

```bash
python -m playwright install chromium
```

---

## ▶️ Executando

Execute:

```bash
python leadgenerator.py
```

A aplicação apresentará um menu semelhante a:

```text
╭────────────────────────────╮
│       MENU PRINCIPAL       │
│                            │
│ [1] 🔎 Buscar leads        │
│ [2] 📋 Ver leads salvos    │
│ [3] 🌐 Filtrar leads SEM site │
│ [4] 🗑️ Limpar arquivo     │
│ [5] ❌ Sair                │
╰────────────────────────────╯
```

---

# 🔎 Buscando leads

Escolha:

```text
[1] Buscar leads
```

Depois informe um termo de pesquisa.

Exemplo:

```text
Digite o termo de busca:
academias em Nova Iguaçu
```

A ferramenta acessará o Google Maps e realizará a pesquisa automaticamente.

Você também pode definir a quantidade de rolagens:

```text
Quantas vezes rolar a página?
5
```

Quanto mais rolagens, maior será a quantidade de resultados que poderá ser carregada.

---

# 📊 Dados coletados

Para cada empresa encontrada, o LeadGenerator tenta obter:

```text
Empresa
Termo Busca
Site
Tem Site
Telefone
Link Maps
```

Exemplo:

| Empresa          | Tem Site | Telefone        | Maps |
| ---------------- | -------- | --------------- | ---- |
| Academia Alpha   | ❌        | (21) 99999-9999 | 🔗   |
| Academia Fitness | ✅        | (21) 98888-8888 | 🔗   |
| Academia Prime   | ❌        | (21) 97777-7777 | 🔗   |

---

# 🚀 Encontrando oportunidades

Uma das principais funcionalidades é identificar empresas que **não possuem site cadastrado**.

No menu:

```text
[3] 🌐 Filtrar leads SEM site
```

A ferramenta filtra automaticamente os resultados onde:

```text
Tem Site = Não
```

Isso permite criar uma lista específica de potenciais clientes para prospecção de serviços de desenvolvimento web.

---

# 💾 Arquivos gerados

Durante a utilização, o programa pode gerar:

```text
leads_encontrados.csv
```

Arquivo principal contendo todos os leads encontrados.

E:

```text
leads_sem_site.csv
```

Arquivo contendo somente os leads identificados como empresas sem site.

Exemplo:

```csv
Empresa,Termo Busca,Site,Tem Site,Telefone,Link Maps
Academia Alpha,academias em Nova Iguaçu,,Não,(21) 99999-9999,https://...
```

---

# 🧹 Gerenciamento dos leads

A opção:

```text
[2] Ver leads salvos
```

permite visualizar os leads armazenados no CSV.

Já:

```text
[4] Limpar arquivo de leads
```

remove o arquivo principal de leads após confirmação.

---

# 🎯 Exemplos de utilização

A ferramenta pode ser utilizada para diferentes nichos:

```text
academias em Nova Iguaçu
```

```text
dentistas em São Gonçalo
```

```text
pizzarias em Niterói
```

```text
advogados em Rio de Janeiro
```

```text
barbearias em Duque de Caxias
```

```text
clínicas de estética em São Paulo
```

```text
oficinas mecânicas em Campinas
```

A ideia é encontrar negócios locais e identificar quais deles apresentam oportunidades de presença digital.

---

# ⚙️ Arquitetura simplificada

O projeto atualmente utiliza uma estrutura simples, concentrada em um único arquivo Python:

```text
LeadGenerator/
│
├── leadgenerator.py
├── leads_encontrados.csv
├── leads_sem_site.csv
└── README.md
```

A simplicidade é intencional: o projeto pode ser executado sem banco de dados ou infraestrutura externa.

---

# 🔐 Privacidade e uso responsável

O LeadGenerator trabalha com informações disponibilizadas publicamente nas páginas acessadas pela automação.

Utilize a ferramenta de maneira responsável e respeite:

* termos de uso das plataformas acessadas;
* limites de requisições;
* legislação aplicável;
* privacidade e proteção de dados;
* regras relacionadas a comunicações comerciais.

A ferramenta **não deve ser utilizada para spam ou envio automatizado indiscriminado de mensagens**.

---

# ⚠️ Observações

O Google Maps pode alterar sua estrutura HTML a qualquer momento.

Como a ferramenta utiliza seletores do DOM para localizar informações, mudanças na interface do Google Maps podem exigir atualizações no código.

O funcionamento também pode variar de acordo com:

* região;
* idioma;
* disponibilidade das informações da empresa;
* alterações na interface do Google Maps;
* carregamento dos resultados;
* quantidade de resultados disponíveis.

---

# 🔮 Roadmap

Possíveis melhorias futuras:

* [ ] Sistema de pontuação de leads
* [ ] Detecção mais precisa de sites
* [ ] Extração de endereço
* [ ] Extração de categoria da empresa
* [ ] Extração de avaliação e quantidade de avaliações
* [ ] Identificação de redes sociais
* [ ] Filtros por cidade e categoria
* [ ] Busca por múltiplos termos automaticamente
* [ ] Exportação para Excel
* [ ] Banco de dados SQLite
* [ ] Histórico de pesquisas
* [ ] Dashboard web
* [ ] Sistema de CRM
* [ ] Classificação automática de oportunidades
* [ ] Verificação básica da qualidade do site
* [ ] Identificação de sites fora do ar
* [ ] Identificação de sites incompatíveis com dispositivos móveis

---

# 🤝 Contribuindo

Contribuições são bem-vindas.

Para contribuir:

```bash
git fork
git clone
git checkout -b minha-feature
```

Faça suas alterações, teste o projeto e envie um Pull Request.

---

# 📄 Licença

Este projeto pode ser distribuído sob a licença definida pelos mantenedores do repositório.

---

## 👨‍💻 Autor

Desenvolvido por **Pedro Silva**.

Projeto criado para automatizar a prospecção de clientes e facilitar a identificação de oportunidades para serviços de desenvolvimento web.

---

⭐ Se este projeto foi útil para você, considere deixar uma estrela no repositório.
