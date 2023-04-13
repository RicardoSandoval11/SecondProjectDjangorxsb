from rest_framework import serializers, pagination

from .models import Favorite
from applications.entries.models import Entry
from applications.entries.serializers import EntrySerializer, EntryHomeSerializer

class FavoritesPaginationSerializer(pagination.PageNumberPagination):
    page_size = 6
    max_page_size = 6

class FavoriteSerializer(serializers.ModelSerializer):

    entry = EntrySerializer()

    class Meta:
        model = Favorite
        fields = ('id', 'entry')

class FavoritesSerializers(serializers.ModelSerializer):


    entry = serializers.IntegerField()
    likes = serializers.IntegerField()
    title = serializers.CharField()
    summary = serializers.CharField()
    image = serializers.SerializerMethodField()

    def get_image(self, object):
        entry_model = Entry.objects.get(id=object['entry'])
        serializer = EntryHomeSerializer(entry_model)
        image = serializer.data.get('image')
        request = self.context.get('request')
        image = request.build_absolute_uri(image)

        return image
    
    class Meta:
        model = Favorite
        fields = ('entry','likes','title','summary','image')
    
