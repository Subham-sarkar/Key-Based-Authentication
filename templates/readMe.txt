For Authentication:
    Name    : <ANY NAME>   #doesnt matter

    Password: secret       # this is required

Once authenticated successfully a jwt token is encoded which is valid for 5 minutes is sent with a cookie and redirected to the upload API.

Without authentication one cannot access the API.

This is a simple demo of API call using JWT authentication.