from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_genre(request, genre_pk):
    request.user.survey_genre_id = genre_pk
    request.user.save()
    print(type(request.user))
    return Response({'message': '성공적으로 제출되었습니다.'})
