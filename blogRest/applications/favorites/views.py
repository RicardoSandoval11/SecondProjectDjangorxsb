from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import Trim
from django.db.models import CharField

# thir party apps
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
import jwt


# local apps
from applications.entries.models import Entry
from applications.users.models import User
from .models import Favorite
from .serializers import FavoritesSerializers, FavoriteSerializer, FavoritesPaginationSerializer

class ListMostLikedFavoritesView(APIView):

    def get(self, request):

        query = Favorite.objects.values('entry').annotate(
            likes=Count('entry'), 
            title=Trim('entry__title',output_field=CharField()),
            summary=Trim('entry__summary', output_field=CharField())
        ).order_by('-likes')[:4]
        
        serializer = FavoritesSerializers(query, many=True, context={'request':request})

        return Response({'ok':'true','data':serializer.data})

class AddEntryToFavorites(APIView):

    permission_classes = [IsAuthenticated, ]

    def post(self, request):

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)

        if response is not None:
            user, token = response

            entry_id = request.data.get('entryId')

            entry = Entry.objects.get(id=entry_id)

            try:
                favorite, created = Favorite.objects.get_or_create(
                    user = user,
                    entry = entry,
                    defaults={
                        'user':user,
                        'entry':entry
                    }
                )
                if not created:
                    return Response({'ok':'false', 'msg':'You already added this entry to your favorites'}, status=status.HTTP_409_CONFLICT)
                else:
                    return Response({'ok':'true', 'msg':'The '+entry.title+' was added to your Favorites successfully!'}, status=status.HTTP_200_OK)
            except jwt.exceptions.DecodeError:
                return Response({'ok':'false','msg':'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)

class ShowMyFavorites(ListAPIView):

    permission_classes = [IsAuthenticated,]
    serializer_class = FavoriteSerializer
    pagination_class = FavoritesPaginationSerializer

    def get_queryset(self):

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(self.request)

        if response is not None:
            user, token = response

            print(user)

            favorites = Favorite.objects.get_favorites_per_user(user)

            return favorites
        
        else:
            return Response({
                'ok': False,
                'msg': 'Invalid Token'
            })

class RemoveEntryFromFavorites(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self, request):

        jwt_authenticator = JWTAuthentication()
        response = jwt_authenticator.authenticate(request)

        if response is not None:
            user, token = response

            favoriteId = request.data.get('favoriteId')

            favorite = Favorite.objects.get(id=favoriteId)

            if favorite.user.id == user.id:

                Favorite.objects.filter(id=favoriteId).delete()
                
                return Response({
                    'ok': True,
                    'msg': 'Favorite removed successfully'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'ok': False,
                    'msg': 'You do not have permissions to remove this register'
                }, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({
                'ok': False,
                'msg': 'Invalid Token'
            }, status=status.HTTP_401_UNAUTHORIZED)