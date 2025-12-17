# Open Food Facts API Guide

This guide was made by Cláudia Rodrigues for the MVP project in the Software Engineering course at Pontifícia Universidade Católica do Rio de Janeiro (PUC - Rio) using Perplexity AI and the Open Food Facts documentation, available at `https://openfoodfacts.github.io/openfoodfacts-server/api/tutorial-off-api/#scan-a-product-to-get-nutri-score`.

Here’s a clear answer based on the **official Open Food Facts API tutorial** for your development context using **openfoodfacts.net**:

***

### 1. **Environment and Base URLs**

- **Development & Staging**: Use `openfoodfacts.net`  
- **Production**: Use `openfoodfacts.org`

So for your case, **all requests should use `https://world.openfoodfacts.net/`** instead of `.org`.

***

### 2. **API Key / Authentication**

- **Reading (GET requests)**:  
  **No API key nor user account is required** for reading data from public endpoints, including product search and barcode lookup.
- **Writing (POST/changes)**:  
  Needs authentication (`user_id`, `password`).  
  As you’re only fetching product data, you do *not* need a key.

***

### 3. **Get Product By Barcode**

**Endpoint:**
```
GET https://world.openfoodfacts.net/api/v2/product/{barcode}
```
**Example:**
```
GET https://world.openfoodfacts.net/api/v2/product/3017624010701
```
**Optional fields:**
- To limit data (e.g., just name and nutrition grade):
```
GET https://world.openfoodfacts.net/api/v2/product/3017624010701?fields=product_name,nutrition_grades
```

***

### 4. **Search for a Product by Name (Full-Text Search)**

- The most robust way is to use the **v1 search endpoint**, as v2 doesn't support plain name search—only via tags/fields.
- Here’s the endpoint:
```
GET https://world.openfoodfacts.net/cgi/search.pl?search_terms={name}&search_simple=1&action=process&json=1
```
**Example:**
```
GET https://world.openfoodfacts.net/cgi/search.pl?search_terms=nutella&search_simple=1&action=process&json=1
```
- This returns a list of candidate products matching the name, with their barcodes and main data fields.

***

### 5. **Corrected Python Code Snippet (Flask)**

```python
OFF_BASE = 'https://world.openfoodfacts.net'
OFF_API_PRODUCT = OFF_BASE + '/api/v2/product/{}'
OFF_API_SEARCH = OFF_BASE + '/cgi/search.pl'

@app.route('/api/barcode/<barcode>')
def get_product_by_barcode(barcode):
    resp = requests.get(OFF_API_PRODUCT.format(barcode))
    return jsonify(resp.json())

@app.route('/api/search')
def search_products():
    query = request.args.get('q', '')
    params = {
        'search_terms': query,
        'search_simple': 1,
        'action': 'process',
        'json': 1,
    }
    resp = requests.get(OFF_API_SEARCH, params=params)
    return jsonify(resp.json())
```

***

### **Summary**


Get by barcode -> `/api/v2/product/{barcode}`
Search by name -> `/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1`                                          
| Auth required? -> **NO** for these read operations                                                                                   

***

**Doc References:**  
- [Scan a Product by Barcode](https://openfoodfacts.github.io/openfoodfacts-server/api/tutorial-off-api/#scan-a-product-to-get-nutri-score)  
- [Search by Name (search.pl endpoint)](https://wiki.openfoodfacts.org/API/Read/Search)

***

**You do NOT need an API key for search/lookup!**  
