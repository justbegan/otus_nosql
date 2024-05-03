1. docker-compose up -d --build
2. db.createCollection("users")
   db.users.insertMany([
    {
        "name": "Alice",
        "age": 25,
        "status": "inactive"
    },
    {
        "name": "Bob",
        "age": 35,
        "status": "active"
    }
])
