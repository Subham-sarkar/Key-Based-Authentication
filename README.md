# Key-Based-Authentication
A flask API along with a simple interface to upload images and using JSON WEB TOKEN (JWT) for accessing the API functionality with a throttle for API call rate, let’s say 5 minutes.

For Authentication:
    Name    : <ANY NAME>   #doesnt matter

    Password: secret       # this is required

Once authenticated successfully a JWT token is encoded which is valid for 5 minutes is sent with a cookie and redirected to the upload API.

Without authentication one cannot access the API.

This is a simple demo of API call using JWT authentication.
