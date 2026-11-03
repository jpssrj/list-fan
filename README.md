# ⚡ TASK // BOARD - Neobrutalism To-Do List

Aplicação full-stack moderna de lista de tarefas desenvolvida com identidade visual marcante no estilo **Neobrutalismo**, unindo alta velocidade, engenharia limpa e arquitetura otimizada para implantação *serverless* na **Vercel** com persistência em nuvem via **Neon PostgreSQL**.

---

## 🎨 Identidade Visual (Neobrutalismo)

O visual foi construído sobre os princípios do Neobrutalismo digital:
* **Bordas Pesadas:** Contornos sólidos em preto puro de 3px (`border-3 border-[#121212]`).
* **Sombras Duras Offset:** Projeções de sombra sem desfoque (`4px 4px 0px 0px #121212`).
* **Física Tátil de Interação:** Botões e cartões reagem ao cursor físico com translações táteis (`translate(2px, 2px)` no hover e `translate(4px, 4px)` com sombra achatada no clique ativo).
* **Paleta de Alto Contraste:** Fundo pergaminho quente suave (`#FFFDF5`), superfícies de cartão brancas, acentos vibrantes em amarelo neon (`#FFE600`), menta para conclusões (`#00F0A8`) e coral para exclusões (`#FF5C5C`).
* **Tipografia Expressiva:** Fonte *Space Grotesk* com pesos ultra-bold e rótulos em caixa alta.

---

## 🚀 Funcionalidades

1. **Adicionar Tarefas:** Digitação rápida com foco automático, validação contra strings vazias e proteção contra submissões duplicadas durante *cold starts*.
2. **Marcar Tarefas como Concluídas:** Alternância instantânea através de checkbox neobrutalista com atualização otimista na interface e estilo tachado.
3. **Remover Tarefas:** Exclusão com um clique através de botão coral dedicado, com reversão automática caso a requisição falhe.
4. **Filtros em Tempo Real:** Segmentação dinâmica entre **Todas**, **Pendentes** e **Concluídas** com contadores reativos em memória (sem roundtrips de rede adicionais).

---

## 🛠️ Stack Tecnológica

* **Frontend:**
  * [Vue 3](https://vuejs.org/) (Composition API com `<script setup lang="ts">`)
  * [TypeScript](https://www.typescriptlang.org/)
  * [Pinia](https://pinia.vuejs.org/) (Gerenciamento de estado com mutações otimistas e rollback de erro)
  * [Tailwind CSS](https://tailwindcss.com/) (Extensões customizadas para design tokens neobrutalistas)
  * [Vite](https://vitejs.dev/)
* **Backend:**
  * [Python 3](https://www.python.org/)
  * [FastAPI](https://fastapi.tiangolo.com/) (API REST moderna e assíncrona)
  * [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (com `NullPool` para compatibilidade serverless)
  * [Pydantic v2](https://docs.pydantic.dev/) (Validação e serialização de dados)
* **Banco de Dados & Deploy:**
  * [Neon PostgreSQL](https://neon.tech/) (Banco relacional serverless com connection pooling e SSL)
  * [Vercel](https://vercel.com/) (Monorepo com rewrites de rotas estáticas e funções serverless ASGI)

---

## 📁 Estrutura do Projeto

```
.
├── api/                      # Backend FastAPI (Função Serverless Vercel)
│   ├── config.py             # Configurações e variáveis de ambiente
│   ├── database.py           # Engine SQLAlchemy (NullPool para serverless)
│   ├── index.py              # Ponto de entrada ASGI da aplicação FastAPI
│   ├── models.py             # Modelo relacional 'Task'
│   ├── schemas.py            # Schemas Pydantic v2
│   └── routers/
│       └── tasks.py          # Endpoints REST (/api/tasks)
├── scripts/
│   └── init_db.py            # Script out-of-band para provisionamento da tabela
├── src/                      # Frontend Vue 3 SPA
│   ├── assets/
│   │   └── main.css          # Diretivas do Tailwind e classes de física tátil
│   ├── components/
│   │   ├── BrutalButton.vue  # Botão primitivo reutilizável com variantes
│   │   ├── TaskFilter.vue    # Abas de filtro com contadores
│   │   ├── TaskInput.vue     # Barra de criação de tarefas
│   │   └── TaskItem.vue      # Card individual com checkbox nativa acessível
│   ├── services/
│   │   └── taskApi.ts        # Cliente HTTP tipado com tratamento de erros
│   ├── stores/
│   │   └── taskStore.ts      # Store Pinia com atualizações otimistas
│   ├── types/
│   │   └── task.ts           # Interfaces TypeScript compartilhadas
│   ├── App.vue               # Layout principal e montagem dos componentes
│   └── main.ts               # Inicialização da aplicação Vue
├── docs/designs/             # Documentação técnica e relatórios de arquitetura
├── index.html                # Documento HTML principal com Space Grotesk
├── package.json              # Dependências e scripts do frontend
├── requirements.txt          # Dependências do backend Python
├── tailwind.config.js        # Design tokens do Neobrutalismo
├── tsconfig.json             # Configuração do TypeScript
├── vercel.json               # Roteamento unificado da Vercel (rewrites)
└── vite.config.ts            # Configuração do Vite com proxy local para /api
```

---

## 💻 Como Executar Localmente

### Pré-requisitos
* Node.js (v18+) e npm
* Python (3.10+)

### 1. Clonar o repositório
```bash
git clone https://github.com/esjun/list-fan.git
cd list-fan
```

### 2. Configurar o Backend
Crie e ative um ambiente virtual Python:
```bash
python -m venv venv

# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# No Linux/macOS:
source venv/bin/activate
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

Provisione a tabela do banco de dados (por padrão cria um arquivo local `tasks_dev.db` caso `DATABASE_URL` não esteja definido no `.env`):
```bash
python scripts/init_db.py
```

Inicie o servidor de desenvolvimento FastAPI:
```bash
uvicorn api.index:app --reload --port 8000
```
*Acesse a documentação Swagger interativa em: `http://localhost:8000/api/docs`*

### 3. Configurar o Frontend
Em outro terminal, instale os pacotes e inicie o Vite:
```bash
npm install
npm run dev
```
*Acesse a interface neobrutalista em: `http://localhost:5173`*

---

## ☁️ Implantação na Vercel

1. **Crie um banco de dados no [Neon](https://neon.tech/)** e copie a string de conexão pooled (`DATABASE_URL`).
2. **Execute o script de inicialização** apontando para o seu banco da Neon:
   ```bash
   DATABASE_URL="sua-connection-string-neon" python scripts/init_db.py
   ```
3. **Faça o Deploy na Vercel:**
   * Conecte o repositório no dashboard da [Vercel](https://vercel.com).
   * Nas configurações do projeto (**Settings > Environment Variables**), adicione:
     * `DATABASE_URL`: URL de conexão do Neon PostgreSQL (com `sslmode=require`).
   * A Vercel executará automaticamente a build do Vite e o deploy da função serverless Python em `/api/index.py` conforme especificado no `vercel.json`.

---

## 🧪 Testes

Para executar a suíte de testes de integração da API:
```bash
python -m unittest tests/test_api.py
```

Para validar a compilação do TypeScript e do Vue:
```bash
npm run build
```

---

## 📄 Licença

Distribuído sob a licença MIT.
