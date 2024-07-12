

## This project has not been completed yet...


### User authentication

#### users/register/
paylaod
``` json
{
	"first_name": "",
	"last_name": "",
	"username": "",
	"email": "",
	"password": "",
	"confirm_password": ""
}
```
response
``` json	
{  
  
	"status": True,
	"message": "Successfully registered, code sent to you email",
	"access_token": "token",
	"auth_status": "NEW"
}
}
```
#### users/verify/
paylaod
``` json

{
	"code": ""
}
```
response  
``` json		
{
	"status": True,
	"access_token": "token",
	"auth_status": "VERIFIED"
}
```
#### users/login/ 
paylaod
```json
{
	"username": "",
	"password": ""
}
```
response
```json 
    {
			"status": True,
			"access_token": "token",
			"refresh_token": "token"
		}
```
#### users/resend/code/
response 
```json  
{
	"status": True,
	"message": "Code send successfully",
	"auth_status": "NEW"
}
```
#### users/password/forget/
paylaod 
```json 
{
	"email": ""
}
```
response 
```json 
{
	"status": True,
	"message": "Code send to email"
}
```
#### users/password/update/
paylaod 
```json 
{
	"password": "",
	"conform_password": ""
}
```
response 
```json 
{
	"status": True,
	"message": "Password changed"
}
```

### Product 
#### products/add/
paylaod  
``` json
{
	"name": "",
	"price": "",
	"photo": "",
	"decription": "",
	"quantity": ""
}
```
response  
``` json
{
	"status": True,
	"message": "added",
	"data": {
			"product details"
	}
}
```
#### products/update/ -> put and patch
paylaod 
``` json
{
	"name": "",
	"price": "",
	"photo": "",
	"decription": "",
	"quantity": ""
}
```
response  
``` json
{
	"status": True,
	"message": "Updated",
	"data": {
			"product details"
	}
}
```
#### products/\<int:pk>/delete/
response  
```json
{
	"status": True,
	"message": "Deleted"
}
```
#### products/\<int:pk>/detail/
response  
```json
{
	"id": "",
	"name": "",
	"price": "",
	"photo": "",
	"decription": "",
	"quantity": ""
}
```