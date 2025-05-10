from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
import jwt
from django.conf import settings
class VulnerableJWTAuthentication(JWTAuthentication):
     def get_validated_token(self, raw_token):
        """
        Overridden to introduce a vulnerability:
        The 'none' algorithm is allowed, and algorithm checking is lax
        """
        try:
            from rest_framework_simplejwt.settings import api_settings
            
            # Convertir le token en string si nécessaire
            if isinstance(raw_token, bytes):
                raw_token = raw_token.decode('utf-8')
                
            # Vulnerability: Not enforcing algorithm validation
            # This allows for algorithm confusion attacks
            decoded_token = jwt.decode(
                raw_token,  # Changed from token to raw_token
                options={
                    "verify_signature": False,
                    "verify_exp": False
                },
                algorithms=["HS256", "none"]
            )
            
            # Return a token object that SimpleJWT expects
            from rest_framework_simplejwt.tokens import Token
            token = Token()
            token.payload = decoded_token
            
            # Debug the decoded token
            print(f"Decoded token in auth.py: {decoded_token}")
            
            return token
            
        except Exception as e:
            print(f"Error in VulnerableJWTAuthentication: {e}")
            raise InvalidToken(f'Token is invalid: {e}')