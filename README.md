# Truth Label - Backend API 🏷️

RESTful API backend for Truth Label application. Integrates with Open Food Facts to verify sustainability claims and calculate reliability scores for food products.

## 📋 About

This backend provides the core functionality for the Truth Label project, including product scanning, score calculation, database management, and API endpoints for the frontend application.

**Developed by:** Cláudia Rodrigues  
**Context:** MVP Project for Post-Graduate Software Engineering - PUC-Rio

## ✨ Features

- 🔌 **RESTful API** with OpenAPI 3.0 documentation
- 🌐 **Open Food Facts Integration** for product data
- 🧮 **Sustainability Score Calculator** (0-100 scale)
- 💾 **SQLite Database** for product history
- 📝 **Comment System** for user feedback
- 👥 **User Management** system
- 📊 **Swagger UI** for interactive API documentation
- 🔒 **CORS Enabled** for frontend integration

## 🏗️ Architecture

### Tech Stack
- **Flask 2.3.3** - Web framework
- **Flask-SQLAlchemy 3.0.5** - ORM
- **SQLite** - Database
- **Pydantic 2.5.2** - Data validation
- **Flasgger 0.9.7.1** - Swagger documentation
- **Flask-CORS 4.0.0** - CORS handling
- **Requests 2.31.0** - HTTP client for Open Food Facts

### Project Structure

```
backend/
├── model/                  # Database models
│   ├── __init__.py
│   ├── product.py         # Product model
│   ├── comment.py         # Comment model
│   └── user.py            # User model
├── routes/                 # API endpoints (Blueprints)
│   ├── __init__.py
│   ├── product_bp.py      # Product routes
│   ├── comment_bp.py      # Comment routes
│   └── user_bp.py         # User routes
├── schemas/                # Pydantic validation schemas
│   ├── __init__.py
│   ├── product_schemas.py
│   ├── comment_schemas.py
│   └── user_schemas.py
├── scripts/                # Utilities
│   ├── __init__.py
│   └── score_calculator.py
├── app.py                  # Flask application factory
├── extensions.py           # SQLAlchemy instance
├── requirements.txt        # Python dependencies
└── truthlable.db          # SQLite database (auto-generated)
```

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation Steps

1. Clone the repository:
```bash
git clone <backend-repo-url>
cd truth-label-backend
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`

### Database Initialization

The database is automatically created on first run. No manual setup required.

## 📚 API Documentation

Access the interactive Swagger documentation at:
```
http://127.0.0.1:5000/apidocs/
```

## 🔌 API Endpoints

### Products

#### **POST /product/scan**
Scans a barcode, checks local database, fetches from Open Food Facts if needed.

**Request Body:**
```json
{
  "barcode": "7891234567890"
}
```

**Response (201 Created):**
```json
{
  "message": "Product scanned and saved successfully",
  "product": {
    "id": 1,
    "name": "Eco Green Soap",
    "barcode": "7891234567890",
    "score": 85.5,
    "nova_group": 1,
    "image_url": "https://...",
    "ingredients_analysis_tags": "en:vegan,en:palm-oil-free",
    "labels_tags": "en:organic,en:fair-trade",
    "allergens_tags": "",
    "additives_tags": "",
    "date_inserted": "2025-12-20T10:30:00"
  }
}
```

#### **GET /product**
Search product in local history by ID, name, or barcode.

**Query Parameters:**
- `id` (integer): Product ID
- `name` (string): Product name (partial match)
- `barcode` (string): Barcode

**Examples:**
```
GET /product?barcode=7891234567890
GET /product?name=soap
GET /product?id=1
```

#### **GET /products-list**
List all products in history.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Eco Green Soap",
    "barcode": "7891234567890",
    "score": 85.5,
    ...
  },
  ...
]
```

#### **PATCH /product/{product_id}**
Update product name or barcode.

**Request Body:**
```json
{
  "name": "New Product Name",
  "barcode": "9876543210987"
}
```

#### **DELETE /product/delete**
Remove product from history.

**Request Body:**
```json
{
  "barcode": "7891234567890"
}
```

### Comments

#### **POST /comment**
Create a comment for a product.

**Request Body:**
```json
{
  "product_id": 1,
  "author_name": "John Doe",
  "text": "This product is truly sustainable!",
  "n_estrela": 5
}
```

#### **GET /comment**
List all comments.

#### **GET /comment/{comment_id}**
Get specific comment by ID.

#### **GET /comment/product/{product_id}**
List all comments for a specific product.

#### **DELETE /comment/{comment_id}**
Delete a comment.

### Users

#### **POST /user**
Create a new user.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com"
}
```

#### **GET /user**
List all users.

#### **GET /user/{user_id}**
Get specific user by ID.

#### **DELETE /user/{user_id}**
Delete a user.

## 🧮 Sustainability Score Algorithm

The score (0-100) is calculated based on multiple weighted criteria:

### High Priority Factors (+/- 10-20 points)

**Certifications (VIP Labels):**
- Organic certifications: `+15`
- Fair Trade: `+15`
- EU Organic: `+15`
- Rainforest Alliance: `+15`

**Ingredient Analysis:**
- Vegan: `+10`
- Palm Oil Free: `+10`
- Contains Palm Oil: `-20`

### Medium Priority Factors (+/- 5-15 points)

**NOVA Group (Processing Level):**
- NOVA 1 (Unprocessed/Minimally processed): `+10`
- NOVA 4 (Ultra-processed): `-15`

**Additives:**
- Each additive: `-2`

### Base Score
Starting point: `50` (neutral)

### Formula
```python
def calculate_score(off_data):
    score = 50  # Base neutral score
    
    # High Priority: Certifications
    for label in labels_tags:
        if label in ['en:organic', 'en:fair-trade', ...]:
            score += 15
    
    # High Priority: Ingredient Analysis
    if 'en:vegan' in analysis:
        score += 10
    if 'en:palm-oil-free' in analysis:
        score += 10
    if 'en:palm-oil' in analysis:
        score -= 20
    
    # Medium Priority: NOVA Group
    if nova_group == 1:
        score += 10
    if nova_group == 4:
        score -= 15
    
    # Medium Priority: Additives
    score -= (len(additives) * 2)
    
    # Clamp between 0-100
    return max(0, min(100, score))
```

## 🗄️ Database Models

### Product Model
```python
class Product(db.Model):
    id: int                              # Primary key
    name: str                            # Product name
    barcode: str                         # Unique barcode (EAN-13)
    image_url: str                       # Product image URL
    score: float                         # Sustainability score (0-100)
    nova_group: int                      # Processing level (1-4)
    ingredients_analysis_tags: str       # Comma-separated tags
    labels_tags: str                     # Certification tags
    allergens_tags: str                  # Allergen tags
    additives_tags: str                  # Additive tags
    date_inserted: datetime              # Scan timestamp
    comments: List[Comment]              # Related comments
```

### Comment Model
```python
class Comment(db.Model):
    id: int                    # Primary key
    text: str                  # Comment text (max 500 chars)
    author: str                # Author name
    n_estrela: int             # Rating (0-5 stars)
    date_inserted: datetime    # Creation timestamp
    product_id: int            # Foreign key to Product
```

### User Model
```python
class User(db.Model):
    id: int                    # Primary key
    username: str              # Unique username
    email: str                 # Unique email
    date_created: datetime     # Registration timestamp
```

## 🔄 Data Flow

### Product Scan Flow
```
1. Frontend sends POST /product/scan with barcode
2. Backend checks local database
   ├─ Found → Return existing product
   └─ Not found → Continue
3. Query Open Food Facts API
4. Extract relevant data
5. Calculate sustainability score
6. Save to local database
7. Return product with score to frontend
```

### Open Food Facts Integration
```python
off_url = f"https://world.openfoodfacts.net/api/v2/product/{barcode}"
response = requests.get(off_url, timeout=10)
product_data = response.json()
```

## ⚙️ Configuration

### CORS Settings
```python
CORS(app, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5500"],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### Database Configuration
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///truthlable.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

## 🧪 Testing

### Using Swagger UI
1. Navigate to `http://127.0.0.1:5000/apidocs/`
2. Select an endpoint
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"

### Using cURL
```bash
# Scan a product
curl -X POST http://127.0.0.1:5000/product/scan \
  -H "Content-Type: application/json" \
  -d '{"barcode": "7891234567890"}'

# Search by name
curl http://127.0.0.1:5000/product?name=soap

# List all products
curl http://127.0.0.1:5000/products-list
```

## 🐛 Troubleshooting

### Database Issues
```bash
# Delete and recreate database
rm truthlable.db
python app.py  # Will auto-create new database
```

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, port=5001)  # Use different port
```

### CORS Errors
Ensure frontend origin is listed in CORS configuration:
```python
"origins": ["http://127.0.0.1:5500"]
```

## 📦 Dependencies

```txt
flasgger==0.9.7.1
Flask==2.3.3
flask-cors==4.0.0
pydantic==2.5.2
requests==2.31.0
python-dotenv==1.0.0
SQLAlchemy==2.0.15
Flask-SQLAlchemy==3.0.5
Werkzeug==2.3.7
```

## 🔒 Security Considerations

- Input validation using Pydantic schemas
- SQL injection prevention via SQLAlchemy ORM
- Error handling for external API failures
- Database transactions with rollback support

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## 📝 License

This project is open-source and available under the MIT License.

## 🔗 Related Repositories

- **Frontend Repository:** [Link to frontend repo]

## 📧 Contact

**Cláudia Rodrigues**  
Post-Graduate Software Engineering Student - PUC-Rio

## 🙏 Acknowledgments

- **Open Food Facts** for the comprehensive API and database
- **Flask** community for excellent documentation
- **PUC-Rio** for academic support

---

⭐ If this project was useful to you, consider giving it a star!
