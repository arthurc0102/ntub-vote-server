from itertools import chain

from import_export import resources

from .models import Student, Group


class StudentResources(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('std_no', 'groups')
        import_id_fields = ('std_no',)
        clean_model_instances = True
        widgets = {
            'groups': {'field': 'name'},
        }

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        groups = set(chain(*[d.split(',') for d in dataset['groups']]))
        exist_groups = set(Group.objects.values_list('name', flat=True))
        non_exist_groups = groups - exist_groups
        Group.objects.bulk_create([Group(name=g) for g in non_exist_groups])
