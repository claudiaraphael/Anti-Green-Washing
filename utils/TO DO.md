# 📋 Lista de Tarefas - MVP Anti Green Washing

## 🎯 Ordem de Prioridade

### 1. Documentação e Setup Inicial

- [x] **Corrigir erro do Swagger no `app.py`**
  - Alterar: `from flask_openapi3 import OpenAPI`
  - Para: `from flask_openapi3.openapi import OpenAPI`
  - Verificar acesso em `http://127.0.0.1:5000/openapi/swagger` ou `/docs`

- [x] **Validar estrutura de pastas do projeto**
  - Confirmar organização: `model/`, `routes/`, `schemas/`, `utils/`
  - Verificar `requirements.txt` com todas as dependências

### 2. Script.js e Lógica Frontend

- [ ] **Corrigir URLs das rotas no `script.js`**
  - Alterar de `/produtos` e `/produto` para `/api/product`
  - Ajustar parâmetros de `quantidade` e `valor` para `name`, `barcode`, `eco_score`

- [ ] **Implementar função `getProduct()` no `script.js`**
  - Capturar valor do `userInput` (barcode ou nome)
  - Fazer requisição `GET` para `/api/scan/<barcode_or_name>`
  - Processar resposta JSON e popular seção `resultadoProduto`

- [ ] **Remover chamada direta à API OFF do JavaScript**
  - A integração com Open Food Facts deve ser feita no backend (Flask)
  - Frontend apenas envia dados para a API Flask e recebe respostas

- [ ] **Atualizar funções CRUD no `script.js`**
  - Ajustar `getList()`, `postItem()`, `deleteItem()` para usar campos corretos
  - Garantir compatibilidade com schemas Pydantic do backend

### 3. Frontend (HTML)

- [ ] **Validar estrutura do `index.html`**
  - Verificar campos de pesquisa (input para barcode/nome)
  - Confirmar seção de resultados (`resultadoProduto`)
  - Validar seção de histórico de produtos

- [ ] **Conectar eventos do HTML com funções do `script.js`**
  - Botão de busca deve chamar `getProduct()`
  - Garantir que formulários chamem funções corretas

### 4. Rotas e Backend (Flask)

- [ ] **Criar arquivo `utils/off_api.py`**
  - Implementar função `fetch_product_by_barcode(barcode)`
  - Usar endpoint: `https://world.openfoodfacts.net/api/v2/product/{barcode}`
  - Adicionar tratamento de erros para produtos não encontrados
  - (Opcional) Implementar `search_product_by_name(name)`

- [ ] **Refatorar rota de busca principal**
  - Criar/corrigir rota: `GET /api/scan/<barcode_or_name>`
  - Implementar fluxo: Buscar no DB local → Se não existe, buscar na OFF → Calcular eco_score → Salvar no DB → Retornar JSON

- [ ] **Corrigir rota `GET /api/product/<str:name>/<str:barcode>`**
  - Ajustar uso incorreto de `Product.query.get_or_404(name, barcode)`
  - Implementar busca correta usando filtros do SQLAlchemy

- [ ] **Implementar lógica de negócio (`eco_score`)**
  - Definir critérios de cálculo baseados em dados da OFF
  - Considerar: selos/rótulos, Nutri-Score, ingredientes sustentáveis
  - Integrar cálculo na rota de busca antes de salvar no DB

- [ ] **Validar rotas CRUD existentes**
  - `GET /api/product` - listar todos os produtos
  - `POST /api/product` - criar produto (já implementado com Pydantic)
  - `DELETE /api/product/<int:product_id>` - deletar produto
  - Garantir que todas usam `db.session` corretamente

- [ ] **Testar transações do banco de dados**
  - Verificar `db.session.add()`, `db.session.commit()`, `db.session.rollback()`
  - Confirmar persistência de dados no SQLite

### 5. Elaboração do Vídeo

- [ ] **Planejar estrutura do vídeo de apresentação**
  - Introdução ao problema do greenwashing
  - Demonstração do MVP funcionando
  - Explicação da arquitetura (Frontend + Backend + API OFF)

- [ ] **Preparar demonstração prática**
  - Escanear produto por código de barras
  - Mostrar cálculo do eco_score
  - Exibir histórico de produtos consultados

- [ ] **Gravar e editar vídeo**
  - Duração recomendada: 3-5 minutos
  - Incluir capturas de tela da aplicação funcionando
  - Adicionar narração explicativa

- [ ] **Preparar materiais de apoio**
  - Slides ou roteiro do vídeo
  - Screenshots da documentação Swagger
  - Diagrama de fluxo de dados (Frontend → Flask → OFF API → DB)

---

## 📌 Notas Importantes

- **Prioridade Máxima**: Corrigir Swagger e criar integração OFF no backend
- **Boa Prática**: Manter lógica de negócio (eco_score) no backend, não no frontend
- **Segurança**: Backend faz chamadas à OFF (evita problemas de CORS)
- **Schemas Pydantic**: Já estão bem implementados, contribuem para documentação automática