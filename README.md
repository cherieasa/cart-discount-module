# cart-discount-module

## Set up

### 1. Create a Virtual Environment, Activate it, and Install Requirements

```bash
# Create venv called .venv
python3 -m venv .venv

# Activate venv
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate

# Install requirements
cd cart_discount_module_app
pip install -r requirements.txt
```

### 2.  Apply Migrations and Create a Superuser

```bash
# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py init_super_user
```

### 3. Run the Development Server and Log in to the Admin Interface

```bash
# Run the development server
python manage.py runserver
```

- Head to http://localhost:8000/admin/ in your browser.
- Log in using the superuser credentials created earlier (this can be found in settings.py file).

### 4. Set User Points, Create Products and Categories, and Create Discount Type Objects

- In the admin interface, navigate to the Users section to set points for the desired user(s).
- Navigate to the Product Manager section to create product categories and products.
- Navigate to the Discount Manager section to create discount type objects (e.g., CouponDiscount, OnTopDiscount, SeasonalDiscount).
- Head to the shopping cart to see the totals depending on the discounts and products added.
- ***Note: For On Top points discount, do not create a OnTopDiscount object, simply enter how many points you want to use in the cart***
