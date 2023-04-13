
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (ListAPIView,RetrieveAPIView, UpdateAPIView)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
import jwt

#
from applications.users.models import  User
from .models import Entry, Category, Tag
from .serializers import (
    EntrySerializer,
    EntryPaginationSerializer,
    EntryDetailSerializer,
    EntryUpdateSerializer,
    EntryCreateSerializer,
    CategorySerializerHome,
    EntryHomeSerializer,
    CategorySerializer,
    CategoryPaginationSerializer,
    TagSerializer
)

""" ENTRIES' VIEWS """

class ListEntriesApiView(ListAPIView):
    serializer_class = EntrySerializer
    pagination_class = EntryPaginationSerializer

    def get_queryset(self):
        return Entry.objects.filter_public_entries()

class EntryDetailView(RetrieveAPIView):

    serializer_class = EntryDetailSerializer

    queryset = Entry.objects.all()

class ListEntriesFilteredByTag(ListAPIView):
    serializer_class = EntrySerializer
    pagination_class = EntryPaginationSerializer

    def get_queryset(self):
        tag_pk = self.kwargs['pk']
        return Entry.objects.filter_entries_by_tag(tag_pk)

class ListMostRecentEntriesHomePage(ListAPIView):
    
    serializer_class = EntryHomeSerializer

    def get_queryset(self):
        return Entry.objects.get_most_recent_entries()

class EntriesByInterstsView(ListAPIView):

    permission_classes = [IsAuthenticated, ]


    def get(self, request):

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)

        if response is not None:
            user, token = response

            try:
                user_id = user.id
                user = User.objects.get(id=user_id)
                entries = Entry.objects.get_entries_by_user_interests(user)
                serializer = EntryHomeSerializer(entries, many=True,context={'request':request})
                return Response({'ok':'true','data': serializer.data})
            except jwt.exceptions.DecodeError:
                return Response({'ok':'false','msg':'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({
                'ok':'false',
                'msg':'Authorization header required'}, status=status.HTTP_401_UNAUTHORIZED)

class ListEntriesByCategory(ListAPIView):

    serializer_class = EntrySerializer
    pagination_class = EntryPaginationSerializer

    def get_queryset(self):
        categoryId = self.kwargs['pk']
        return Entry.objects.get_entries_by_category(categoryId=categoryId)

class ListAllFilteredEntries(ListAPIView):

    serializer_class = EntrySerializer
    pagination_class = EntryPaginationSerializer

    def get_queryset(self):
        title = self.request.query_params.get('kword1','')
        content = self.request.query_params.get('kword2','')
        categoryId = self.request.query_params.get('categoryid',None)
        interest = self.request.query_params.get('interestid',None)
        tag = self.request.query_params.get('tagid',None)
        start_date = self.request.query_params.get('startdate',None)
        end_date = self.request.query_params.get('enddate',None)

        return Entry.objects.get_all_filtered_entries(title, content, categoryId, interest, tag, start_date, end_date)

class ListMyEntries(ListAPIView):

    pagination_class = EntryPaginationSerializer
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(self.request)

        if response is not None:
            user, token = response
            return Entry.objects.get_entries_by_user(user)
        else:
            return Response({
                'ok':False,
                'msg':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class ListMyEntriesUserDashboard(ListAPIView):

    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(self.request)

        if response is not None:
            user, token = response
            return Entry.objects.get_entries_by_user(user).order_by('-created')[:6]
        else:
            return Response({
                'ok':False,
                'msg':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class DeleteEntryView(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self, request):

        jwt_authenticator = JWTAuthentication()

        response = jwt_authenticator.authenticate(request)

        if response is not None:
            user, token = response
            entryId = request.data.get('entryId')

            entry = Entry.objects.get(id=entryId)

            if (user.id == entry.user.id):
                try:
                    Entry.objects.filter(id=entryId).delete()
                    return Response({
                        'ok': True,
                        'msg': 'The entry '+entry.title+' has been removed successfully'
                    }, status=status.HTTP_200_OK)
                except:
                    return Response({
                        'ok': False,
                        'msg': 'An error ocurred'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'ok': False,
                    'msg': 'You cannot remove this register'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                    'ok': False,
                    'msg': 'Invalid Token'
                }, status=status.HTTP_401_UNAUTHORIZED)

class GetEntryToUpdateView(APIView):

    permission_classes = [IsAuthenticated,]

    def get(self, request):

        jwt_authenticator = JWTAuthentication()

        response = jwt_authenticator.authenticate(request)

        if response is not None:
            user, token = response
            entryId = request.query_params.get('entryId')

            entry = Entry.objects.get(id=entryId)

            if (user.id == entry.user.id):
                try:
                    # verify the entry exists
                    try:
                        entry = Entry.objects.get(id=entryId)
                    except:
                        return Response({
                            'ok': False,
                            'msg': 'Entry does not exist'
                        },status=status.HTTP_404_NOT_FOUND)
                     
                    serialized_data = EntryDetailSerializer(entry,context={'request':request})
                    return Response({
                        'ok':True,
                        'data':serialized_data.data
                    },status=status.HTTP_200_OK)
                except:
                    return Response({
                        'ok': False,
                        'msg': 'An error ocurred'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'ok': False,
                    'msg': 'You cannot update this register'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                    'ok': False,
                    'msg': 'Invalid Token'
                }, status=status.HTTP_401_UNAUTHORIZED)

class CreateEntryView(APIView):

    permission_classes = [IsAuthenticated,]

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        
        serializer = EntryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'ok': True,
                'msg': 'Entry Created Successfully'
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'ok':False,
                'msg': 'An error happened while trying to create the new Entry',
                'errors':serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)

class UpdateEntryView(UpdateAPIView):

    permission_classes = [IsAuthenticated,]

    parser_classes = [MultiPartParser, FormParser]

    serializer_class = EntryUpdateSerializer

    queryset = Entry.objects.all()

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)  # llamada al método .is_valid()
        self.perform_update(serializer)
        return Response(serializer.data)


""" CATEGORIES' VIEWS """

class List20CategoriesHomePage(ListAPIView):
    serializer_class = CategorySerializerHome

    def get_queryset(self):
        return Category.objects.get_last_categories()

class SimpleListcategoriesView(ListAPIView):
    serializer_class = CategorySerializerHome

    def get_queryset(self):
        return Category.objects.all()

class ListAllCategories(ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = CategoryPaginationSerializer

    def get_queryset(self):
        kword = self.request.query_params.get('kword', None)
        return Category.objects.get_categoris_by_kword(kword)

""" TAGS' VIEWS """

class ListAllTags(ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


