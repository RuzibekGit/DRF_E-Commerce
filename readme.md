

## This project has not been completed yet...


### User authentication
##### users/register/
``` json
//  
{
  "paylaod": {

		"first_name": "",
		"last_name": "",
		"username": "",
		"email": "",
		"password": "",
		"confirm_password": ""
	},
		
  "response": {  
    
		"status": True,
		"message": "Successfully registered, code sent to you email",
		"access_token": "token",
		"auth_status": "NEW"
	}
}
```

``` json
// users/verify/
		// paylaod 
    {
			"code": ""
		}
		
		// response  
    {
			"status": True,
			"access_token": "token",
			"auth_status": "VERIFIED"
		}
// -------------------------------------------------------------------------------
// users/login/
		// paylaod
     {
			"username": "",
			"password": ""
		}
		// response 
    {
			"status": True,
			"access_token": "token",
			"refresh_token": "token"
		}
// -------------------------------------------------------------------------------

// users/resend/code/
		// response  
    {
			"status": True,
			"message": "Code send successfully",
			"auth_status": "NEW"
		}


// -------------------------------------------------------------------------------
// users/password/forget/
		// paylaod 
    {
			"email": ""
		}
		// response  
    {
			"status": True,
			"message": "Code send to email"
		}

// -------------------------------------------------------------------------------
// users/password/update/
		// paylaod 
    {
			"password": "",
			"conform_password": ""
		}
		// response {
			"status": True,
			"message": "Password changed"
		}
```

### Product 
``` json
// products/add/
		// paylaod  
    {
			"name": "",
			"price": "",
			"photo": "",
			"decription": "",
			"quantity": ""
		}
		// response  
    {
			"status": True,
			"message": "added",
			"data": {
					"product details"
			}
		}
// -------------------------------------------------------------------------------
// products/update/ -> put and patch
// 		paylaod 
    {
			"name": "",
			"price": "",
			"photo": "",
			"decription": "",
			"quantity": ""
		}
		// response  
    {
			"status": True,
			"message": "Updated",
			"data": {
					"product details"
			}
		}
	
	// -------------------------------------------------------------------------------
	// products/<int:pk/>delete/
		// response  
    {
			"status": True,
			"message": "Deleted"
		}
	// -----------------------------------------------------------------------------
		// products/<int:pk/>detail/
			// response  
      {
				"id": "",
				"name": "",
				"price": "",
				"photo": "",
				"decription": "",
				"quantity": ""
			}
```