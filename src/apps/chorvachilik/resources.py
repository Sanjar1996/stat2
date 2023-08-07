from import_export import resources
from . models import Animal


class AnimalResource(resources.ModelResource):
    class Meta:
        model = Animal
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'name', 'category', 'status')
