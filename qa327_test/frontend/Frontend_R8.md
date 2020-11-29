# Test Case R8
Test data:
```
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)
```
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='test_ticket_yo',
    quantity=10,
    price=10,
    date='20200901'
)
```
### Test Case R8.1 - For any other requests except the ones above, the system should return a 404 error
Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /somethingthatdoesntexist
- validate that the current page contains the element `#Error-message`showing `'Error: 404. Page does not exist.'`
