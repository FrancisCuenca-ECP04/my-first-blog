from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken import views

class APIAuth(APIView,ObtainAuthToken):

    def post(self,request):
        try:
            serializer = self.serializer_class(
                data=request.data,
                context={"request":request}
            )
        
            if not seriailzer.is_valid():
                self.raise_error(
                    message = "Invalid username/password.",
                    title = "Error"
                    errors = serializers.errors,
                    status = 401
                )
            user = serializer.validated_data["user"]
            token, is_created = Token.objects.get_or_create(user=user)

            response = {
                "token": token.key,
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
            }
            return self.success_response(response)
        except HumanReadableError as exc:
            return self.error_response(exc, self.error_dict, self.status)
        except Exception as exc:
            return self.server_error_response(exc)