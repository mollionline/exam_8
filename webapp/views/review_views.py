from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from webapp.forms import ReviewForm
from webapp.models import Review, Product


class ReviewsListView(ListView):
    template_name = 'review/list_review.html'
    model = Review
    context_object_name = 'reviews'


class UpdateReviewView(PermissionRequiredMixin, UpdateView):
    model = Review
    template_name = 'review/edit_review.html'
    form_class = ReviewForm
    permission_required = 'webapp.change_review'

    def get_success_url(self):
        return reverse('detail_product', kwargs={'pk': self.object.product.pk})


class ReviewDeleteView(DeleteView):
    model = Review

    def get(self, request, *args, **kwargs):
        return self.delete(request=request)

    def get_success_url(self):
        return reverse('detail_product', kwargs={'pk': self.object.product.pk})


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review/detail_review.html'
    context_object_name = 'review'


class NewAddReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'product/detail_product.html'

    def get_success_url(self):
        return reverse('detail_product', kwargs={'pk': self.kwargs.get('pk')})

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        form = self.form_class(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.author = self.request.user
            review.save()
            return redirect(self.get_success_url())
        return render(request, self.template_name,
                      context={
                          'form': form,
                          'product': product
                      })
