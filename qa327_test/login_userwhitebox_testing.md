## Analysis:
Analysis: We used decision coverage to test each different side of the if stament in the login_user function. The four tests cover each different combination of desicions.

**backend method: login_user(email , password)**

| Test 	| user(condition) 	| check_password_hash(condition) 	|  Output 	|
|------	|-----------------	|--------------------------------	|---------	|
| T1   	| TRUE            	| TRUE                           	| User    	|
| T2   	| TRUE            	| FALSE                          	| None    	|
| T3   	| FALSE           	| TRUE                           	| None    	|
| T4   	| FALSE           	| FALSE                          	| None    	|                                                                                                                                                      
