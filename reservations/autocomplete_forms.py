from dal import autocomplete

from .models import Customer


class CustomerAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return Customer.objects.none()

        qs = Customer.objects.all()
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs