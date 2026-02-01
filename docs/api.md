# Elavid API Documentation

Base URL: `http://localhost:8000/api/v1`

Swagger UI: `http://localhost:8000/docs`

---

## Authentication

All protected endpoints require a Firebase ID token in the `Authorization` header:

```
Authorization: Bearer <firebase_id_token>
```

The token is obtained from Firebase on the frontend after login/signup.

---

## Users

### POST `/users/me`

Get or create the current user. Extracts uid, email, and name from the Firebase token. If the user doesn't exist in the database, a new record is created.

**Auth:** Required

**Request:** No body needed. User data is extracted from the Firebase token.

**Response:** `200 OK`
```json
{
  "id": "firebase_uid_string",
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2026-01-31T12:00:00Z"
}
```

**Errors:**
- `400` - Firebase token missing uid or email
- `401` - Invalid or expired token
- `500` - Database error

---

## Products

### GET `/products/`

Get all products. No authentication required.

**Auth:** None

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Rose Petal Balm",
    "description": "Organic lip balm with rose extract",
    "price": 18.00,
    "stock": 50,
    "image_url": "https://example.com/image.jpg",
    "created_at": "2026-01-31T12:00:00Z"
  }
]
```

---

### GET `/products/{product_id}`

Get a single product by its ID.

**Auth:** None

**Parameters:**
| Parameter | Type | Location | Description |
|-----------|------|----------|-------------|
| product_id | int | path | The product ID |

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Rose Petal Balm",
  "description": "Organic lip balm with rose extract",
  "price": 18.00,
  "stock": 50,
  "image_url": "https://example.com/image.jpg",
  "created_at": "2026-01-31T12:00:00Z"
}
```

**Errors:**
- `404` - Product not found

---

### POST `/products/`

Create a new product. Admin only.

**Auth:** Required (Admin)

**Request Body:**
```json
{
  "name": "Rose Petal Balm",
  "description": "Organic lip balm with rose extract",
  "price": 18.00,
  "stock": 50,
  "image_url": "https://example.com/image.jpg"
}
```

| Field | Type | Required | Default |
|-------|------|----------|---------|
| name | string | Yes | - |
| description | string | No | null |
| price | float | Yes | - |
| stock | int | No | 0 |
| image_url | string | No | null |

**Response:** `200 OK` - Returns the created product.

**Errors:**
- `401` - Not authenticated
- `403` - Admin access required
- `500` - Database error

---

### PUT `/products/{product_id}`

Update an existing product. Only provided fields will be changed. Admin only.

**Auth:** Required (Admin)

**Parameters:**
| Parameter | Type | Location | Description |
|-----------|------|----------|-------------|
| product_id | int | path | The product ID |

**Request Body:** (all fields optional)
```json
{
  "name": "Updated Name",
  "price": 25.00
}
```

**Response:** `200 OK` - Returns the updated product.

**Errors:**
- `401` - Not authenticated
- `403` - Admin access required
- `404` - Product not found
- `500` - Database error

---

### DELETE `/products/{product_id}`

Delete a product. Admin only.

**Auth:** Required (Admin)

**Parameters:**
| Parameter | Type | Location | Description |
|-----------|------|----------|-------------|
| product_id | int | path | The product ID |

**Response:** `200 OK`
```json
{
  "message": "Product deleted successfully"
}
```

**Errors:**
- `401` - Not authenticated
- `403` - Admin access required
- `404` - Product not found
- `500` - Database error

---

## Cart

All cart endpoints require authentication. The user is identified by their Firebase UID from the token.

### GET `/cart/`

Get all items in the user's cart with product details.

**Auth:** Required

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "product_id": 3,
    "quantity": 2,
    "product_name": "Rose Petal Balm",
    "product_price": 18.00,
    "product_image": "https://example.com/image.jpg"
  }
]
```

---

### POST `/cart/add`

Add a product to the cart. If the product is already in the cart, the quantity is increased.

**Auth:** Required

**Request Body:**
```json
{
  "product_id": 3,
  "quantity": 1
}
```

| Field | Type | Required | Default |
|-------|------|----------|---------|
| product_id | int | Yes | - |
| quantity | int | No | 1 |

**Response:** `200 OK` - Returns the cart item with product details.

**Errors:**
- `401` - Not authenticated
- `404` - Product not found
- `500` - Database error

---

### PUT `/cart/update?product_id={id}`

Update the quantity of a product in the cart. Use this when the user clicks +/- buttons.

**Auth:** Required

**Parameters:**
| Parameter | Type | Location | Description |
|-----------|------|----------|-------------|
| product_id | int | query | The product ID to update |

**Request Body:**
```json
{
  "quantity": 3
}
```

**Response:** `200 OK` - Returns the updated cart item with product details.

**Errors:**
- `401` - Not authenticated
- `404` - Item not found in cart
- `500` - Database error

---

### DELETE `/cart/remove?product_id={id}`

Remove a product from the cart.

**Auth:** Required

**Parameters:**
| Parameter | Type | Location | Description |
|-----------|------|----------|-------------|
| product_id | int | query | The product ID to remove |

**Response:** `200 OK`
```json
{
  "message": "Item removed from cart"
}
```

**Errors:**
- `401` - Not authenticated
- `404` - Item not found in cart
- `500` - Database error

---

## Orders

*Endpoints not yet implemented.*

---

## Payments

*Endpoints not yet implemented.*
