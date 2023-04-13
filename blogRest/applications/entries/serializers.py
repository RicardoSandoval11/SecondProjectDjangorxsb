from django.conf import settings
#
from rest_framework import serializers, pagination
#
from .models import Entry, Tag, Category
from applications.users.serializers import UserSerializer, InterestsSerializer


""" tags' serializers """

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')

""" Categories' serializers """

class CategoryPaginationSerializer(pagination.PageNumberPagination):
    page_size = 6
    max_page_size = 6

class CategorySerializerHome(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id','name')

class CategorySerializer(serializers.ModelSerializer):

    number_of_entries = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'number_of_entries')

    def get_number_of_entries(self, obj):
        return Entry.objects.filter(
            category=obj.id
        ).count()
    
""" List all entries serializer """

class EntrySerializer(serializers.ModelSerializer):

    user = UserSerializer()
    created  = serializers.DateTimeField(format=settings.DATETIME_FORMAT, input_formats=None)

    class Meta:
        model = Entry
        fields = (
            'id',
            'user',
            'created',
            'title',
            'summary',
            'public',
            'image'
        )

class EntryPaginationSerializer(pagination.PageNumberPagination):
    page_size = 6
    max_page_size = 6

""" Show details of entries serializer """

class EntryDetailSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    tags = TagSerializer(many=True)
    interests = InterestsSerializer(many=True)
    category = CategorySerializerHome()
    created  = serializers.DateTimeField(format=settings.DATETIME_FORMAT, input_formats=None)
    modified = serializers.DateTimeField(format=settings.DATETIME_FORMAT, input_formats=None)

    class Meta:
        model = Entry
        fields = ('__all__')

""" Serializer for entries displayed in Home view """

class EntryHomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = (
            'id',
            'title',
            'image',
            'summary'
        )

""" Serializer to display entries filtered by users' intersts """

class EntryInterstsSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    def get_image(self, object):
        entry_model = Entry.objects.get(id=object['id'])
        serializer = EntryHomeSerializer(entry_model)
        image = serializer.data.get('image')
        request = self.context.get('request')
        image = request.build_absolute_uri(image)

        return image
    
    class Meta:
        model = Entry
        fields = (
            'id',
            'title',
            'image'
        )

""" Serializer to update entries """

class EntryUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = (
            'category',
            'title',
            'summary',
            'content',
            'public',
            'image'
        )
    
    def update(self, instance, validated_data):

        # verify if another file was submitted
        image = validated_data.get('image', None)
        if image:
            instance.image = image
        
        # update other fields
        instance.category = validated_data.get('category', instance.category)
        instance.title = validated_data.get('title', instance.title)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.content = validated_data.get('content', instance.content)
        instance.public = validated_data.get('public', instance.public)
        # save changes
        instance.save()
        return instance

class EntryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = (
            'user',
            'category',
            'title',
            'tags',
            'summary',
            'content',
            'public',
            'image',
            'interests'
        )
