# Anti-Green-Washing

# Anti Green Washing

Sustainability verification API that combats misleading green marketing practices. The system allows users to scan product barcodes and receive an objective analysis based on real certifications, not just marketing claims.

The project exposes REST endpoints that consume Open Food Facts data, process environmental certification information (organic, fair trade, carbon neutral, etc.) and return a calculated score indicating the product's actual environmental commitment versus what the brand advertises.

## Technologies

**Backend:**
- Flask for REST API construction
- Python for data processing and business logic
- SQLite for data storage

**Integrations:**
- Open Food Facts API for product data and certifications
- Barcode scanning system 

**Core Features:**
- Product lookup via barcode
- Comparative analysis between marketing claims and actual certifications
- Sustainability score generation based on objective criteria
- User scan history tracking

