# REST API Design

## Principles

Design APIs that are predictable, consistent, and easy to use.

## URL Naming

### Resources

Use nouns, not verbs. Plural is conventional.

```
GET    /users           # list users
POST   /users           # create a user
GET    /users/{id}      # get a user
PUT    /users/{id}      # update a user (full)
PATCH  /users/{id}      # update a user (partial)
DELETE /users/{id}      # delete a user
```

### Nested Resources

```
GET    /users/{id}/posts           # posts by a user
POST   /users/{id}/posts           # create a post for a user
GET    /users/{id}/posts/{post_id} # specific post by a user
```

### Sub-Resources

```
POST   /auth/login        # authentication action
POST   /auth/logout       # authentication action
POST   /auth/refresh      # token refresh
```

## HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|-----------|------|
| GET | Read resource | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | Yes* | No |
| DELETE | Remove resource | Yes | No |

*PATCH is idempotent if the patch operation is idempotent.

## Status Codes

### Success

- **200 OK** — successful GET, PUT, PATCH
- **201 Created** — successful POST (resource created)
- **204 No Content** — successful DELETE

### Client Errors

- **400 Bad Request** — invalid input, validation error
- **401 Unauthorized** — not authenticated
- **403 Forbidden** — authenticated but not authorized
- **404 Not Found** — resource doesn't exist
- **409 Conflict** — resource state conflict
- **422 Unprocessable Entity** — valid JSON but semantically wrong
- **429 Too Many Requests** — rate limited

### Server Errors

- **500 Internal Server Error** — unexpected error
- **502 Bad Gateway** — upstream service error
- **503 Service Unavailable** — temporarily unavailable

## Request/Response Format

### Request Body

Always use JSON for request bodies:

```json
{
    "name": "John Doe",
    "email": "john@example.com"
}
```

### Success Response

```json
{
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00Z"
}
```

### List Response with Pagination

```json
{
    "items": [...],
    "total": 100,
    "page": 1,
    "per_page": 20,
    "has_more": true
}
```

### Error Response

```json
{
    "error": {
        "code": "validation_error",
        "message": "Invalid input",
        "details": [
            {
                "field": "email",
                "message": "Invalid email format"
            }
        ]
    }
}
```

## Pagination

### Offset-Based

```
GET /users?page=1&per_page=20
GET /users?page=2&per_page=20
```

### Cursor-Based (better for large datasets)

```
GET /users?cursor=abc123&limit=20
```

## Versioning

### URL Path (recommended)

```
/api/v1/users
/api/v2/users
```

### Header

```
Accept: application/vnd.myapp.v1+json
```

## Filtering & Sorting

```
GET /users?status=active&sort=-created_at&limit=10
GET /users?search=john&fields=id,name,email
```

## Best Practices

1. **Consistent naming** — use the same conventions everywhere
2. **Pagination for lists** — never return unbounded lists
3. **Meaningful error messages** — tell users what went wrong and how to fix it
4. **Version your API** — breaking changes go in new versions
5. **Document your API** — use OpenAPI/Swagger
6. **Rate limiting** — protect your API from abuse
7. **Use HTTPS** — always, everywhere
