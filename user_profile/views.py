from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import UserProfile
from permissions import IsOwnerOrAdmin
from .serializers import UserProfileSerializer


class UserProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get(self, request, pk):
        try:
            user_profile = self.queryset.get(pk=pk)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': user_profile.to_dict()
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'User does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)

    def put(self, request, pk):
        try:
            user_profile = self.queryset.get(pk=pk)
            user_profile_serializer = self.serializer_class(instance=user_profile, data=request.data,
                                                            partial=True)
            if user_profile_serializer.is_valid(raise_exception=True):
                user_profile_serializer.save()
                status_code = status.HTTP_200_OK
                response = {
                    'success': 'True',
                    'status code': status_code,
                    'message': 'User updated successfully',
                    'user': user_profile_serializer.data
                }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'User does not exists',
                'error': str(e)
            }

        return Response(response, status=status_code)

    def delete(self, request, pk):
        try:
            user_profile = self.queryset.get(pk=pk)
            user_profile.delete()
            status_code = status.HTTP_204_NO_CONTENT
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'User deleted successfully',
                'user': {}
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'User does not exists',
                'error': str(e)
            }

        return Response(response, status=status_code)
