class UserOwnedQuerySetMixin:
    @property
    def model(self):
        return self.serializer_class.Meta.model
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)