# middleware/supabase_auth.py

import jwt
import requests
from django.conf import settings
from django.http import JsonResponse

SUPABASE_JWKS_URL = f"https://{settings.SUPABASE_PROJECT_ID}.supabase.co/auth/v1/keys"

class SupabaseJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwks = None

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                decoded_token = self.verify_token(token)
                request.supabase_user = decoded_token  # attach to request
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=401)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=401)
        else:
            request.supabase_user = None  # anonymous request

        return self.get_response(request)

    def verify_token(self, token):
        if not self.jwks:
            response = requests.get(SUPABASE_JWKS_URL)
            self.jwks = response.json()["keys"]

        unverified_header = jwt.get_unverified_header(token)
        for key in self.jwks:
            if key["kid"] == unverified_header["kid"]:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                return jwt.decode(
                    token,
                    public_key,
                    algorithms=["RS256"],
                    audience=settings.SUPABASE_PROJECT_ID,
                    issuer=f"https://{settings.SUPABASE_PROJECT_ID}.supabase.co/auth/v1",
                )

        raise jwt.InvalidTokenError("Public key not found.")
