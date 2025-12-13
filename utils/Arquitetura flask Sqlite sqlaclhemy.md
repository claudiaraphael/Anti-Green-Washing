"""
ARQUITETURA SUGERIDA PARA UM PROJETO FLASK COM FLASK-OPENAPI3

app.py: Cria a aplicação e registra os Blueprints.

extensions.py: Inicializa extensões como db e OpenAPI.

model/: Contém OS modelos SQLAlchemy (product.py, user.py etc.).

schemas/: Contém os schemas Pydantic para validação e documentação dos dados.

routes/ (ou api/): Contém os Blueprints (as rotas) onde a lógica de negócio acontece.

.env: Variáveis de ambiente para configuração.

"""
# Referencias

# self

https://github.com/claudiaraphael/Anti-Green-Washing/blob/main/app.py

# Arquiteturas

https://www.google.com/search/criteria-for-measuring-how-sus-CbeRYsBVQ.qlycvArDnz8g
https://www.perplexity.ai/search/criteria-for-measuring-how-sus-CbeRYsBVQ.qlycvArDnz8g
https://github.com/wmfariadev/python-flask-api/blob/main/app.py

## Formulario com Flask

[text](https://github.com/VILHALVA/FORMULARIO-COM-FLASK)

# Exemplo bom de SQLAlchemy, mas com PostgreeSQL

https://github.com/wmfariadev/python-flask-api/blob/main/app.py

# Documentacao Open Food Facts

https://openfoodfacts.github.io/openfoodfacts-server/api/ref-v2/#get-/api/v2/product/-barcode-

# SDK

https://github.com/openfoodfacts/openfoodfacts-python

# Código do Professor

https://github.com/dipucriodigital/desenvolvimento-full-stack/blob/main/desenvolvimento-full-stack-basico/aula-3/meu_app_api/schemas/__init__.py

# achar configuração sqlalchemy com extensions.py