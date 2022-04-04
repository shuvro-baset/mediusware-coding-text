from django.views import generic
from django.shortcuts import render, redirect
from product.models import Variant, ProductVariantPrice, ProductVariant
from django.core.paginator import Paginator


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        print()
        context['variants'] = list(variants.all())
        return context


# showing products and filter products
class ProductsView(generic.TemplateView):
    template_name = 'products/list.html'

    def get(self, request):
        # getting products data from ProductVariantPrice model
        products = ProductVariantPrice.objects.all()
        # getting variants
        variants = ProductVariant.objects.all()
        colors = []
        sizes = []
        styles = []
        for v in variants:
            if v.variant_id == 1:
                color = v.variant_title
                if color not in colors:
                    colors.append(color)
            if v.variant_id == 2:
                size = v.variant_title
                if size not in sizes:
                    sizes.append(size)
            if v.variant_id == 3:
                style = v.variant_title
                if style not in styles:
                    styles.append(style)
        print("variants: ", colors)
        # todo: pagination start
        paginator = Paginator(products, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        # todo: pagination end
        context = {
            # 'products': products,
            "page_obj": page_obj,
            "colors": colors,
            "sizes": sizes,
            "styles": styles,
        }
        return render(request, self.template_name, context=context)
