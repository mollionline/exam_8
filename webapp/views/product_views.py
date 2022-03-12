from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from webapp.forms import ProductForm
from webapp.models import Product


class ProductCreateView(CreateView):
    template_name = 'product/create_product.html'
    form_class = ProductForm

    def get(self, request, *args, **kwargs):
        form = ProductForm()
        categories = Product.CATEGORIES
        return render(request, self.template_name,
                      context={
                          'form': form,
                          'categories': categories
                      })

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=self.request.FILES)
        categories = Product.CATEGORIES
        if form.is_valid():
            product = form.save(commit=False)
            product_user = request.user
            product.save()
            product.user.add(product_user)
            url = reverse('detail_product', kwargs={
                'pk': product.pk
            })
            return redirect(url)
        return render(request, self.template_name,
                      context={
                          'form': form,
                          'categories': categories
                      })


class ProductDetailView(DetailView):
    context_object_name = 'product'
    template_name = 'product/detail_product.html'
    model = Product

    def get_context_data(self, **kwargs):
        kwargs['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)


class ProductListView(ListView):
    template_name = 'product/list_product.html'
    model = Product
    context_object_name = 'products'


class UpdateProductView(PermissionRequiredMixin, UpdateView):
    template_name = 'product/update_product.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('detail_product', kwargs={'pk': self.get_object().pk})

    def get_context_data(self, **kwargs):
        categories = Product.CATEGORIES
        kwargs['categories'] = categories
        return super().get_context_data(**kwargs)


class ProductDeleteView(DeleteView):
    model = Product

    def get(self, request, *args, **kwargs):
        return self.delete(request=request)

    def get_success_url(self):
        return reverse('list_product')
