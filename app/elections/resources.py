from import_export import resources

from .models import Vote


class VoteResources(resources.ModelResource):
    class Meta:
        model = Vote
        fields = ('candidate__pool__name', 'std_no',)
