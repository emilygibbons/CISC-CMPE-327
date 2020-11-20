## Analysis: 
We used exhaustive testing to cover all the cases since there is not many. The test cases take all possible input and then show the resulting ouput.

| backend method: login_user(email , password) |                  |                     |        |
|----------------------------------------------|------------------|---------------------|--------|
| Partition                                    | Input 1: 'email' | Input 2: 'password' | Output |
| P1                                           | null             | null                | None   |
| P2                                           | null             | password(valid)     | None   |
| P3                                           | email (valid)    | null                | None   |
| P4                                           | email (valid)    | password(valid)     | User   |
| P5                                           | email(invalid)   | password(valid)     | None   |
| P6                                           | email (valid)    | password(invalid)   | None   |
| P7                                           | email(invalid)   | null                | None   |
| P8                                           | null             | password (invalid)  | None   |
