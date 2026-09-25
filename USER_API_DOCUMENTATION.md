# User API Documentation

## 1. Get All Users (List)

url : (http://192.168.1.59:8000/api/users)
method : GET

*(Also supports http://192.168.1.59:8000/api/users/list and http://192.168.1.59:8000/api/user/list)*

params :- 

- search: (Optional) Search text matching user's full name, email, phone number, or username
- role: (Optional) Filter by role (e.g. user or admin)
- is_active: (Optional) Filter by active status (true or false)
- limit: (Optional) Integer to limit number of records
- offset: (Optional) Integer to offset results for pagination

response :- 

{
  "count": 12,
  "users": [
    {
      "id": 1,
      "username": null,
      "full_name": "Test User",
      "email": "test88190241@example.com",
      "phone_number": "15558819024",
      "role": "user",
      "is_active": true,
      "created_at": "2026-09-09T04:43:59.992396",
      "updated_at": "2026-09-09T04:43:59.992405"
    },
    {
      "id": 6,
      "username": "admin",
      "full_name": "System Administrator",
      "email": "admin@power.solution",
      "phone_number": "0000000000",
      "role": "admin",
      "is_active": true,
      "created_at": "2026-09-09T05:19:42.523953",
      "updated_at": "2026-09-09T05:19:42.523959"
    }
  ],
  "results": [
    {
      "id": 1,
      "username": null,
      "full_name": "Test User",
      "email": "test88190241@example.com",
      "phone_number": "15558819024",
      "role": "user",
      "is_active": true,
      "created_at": "2026-09-09T04:43:59.992396",
      "updated_at": "2026-09-09T04:43:59.992405"
    },
    {
      "id": 6,
      "username": "admin",
      "full_name": "System Administrator",
      "email": "admin@power.solution",
      "phone_number": "0000000000",
      "role": "admin",
      "is_active": true,
      "created_at": "2026-09-09T05:19:42.523953",
      "updated_at": "2026-09-09T05:19:42.523959"
    }
  ]
}

---

## 2. Get User Details By ID

url : (http://192.168.1.59:8000/api/users/6)
method : GET

*(Also supports http://192.168.1.59:8000/api/user/6)*

params :- 

(None)

response :- 

{
  "message": "User details fetched successfully",
  "user": {
    "id": 6,
    "username": "admin",
    "full_name": "System Administrator",
    "email": "admin@power.solution",
    "phone_number": "0000000000",
    "role": "admin",
    "is_active": true,
    "created_at": "2026-09-09T05:19:42.523953",
    "updated_at": "2026-09-09T05:19:42.523959"
  }
}
