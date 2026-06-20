"""Views for browsing and filtering catalog products."""

from django.db.models import Q
from django.shortcuts import render

from .models import Category, Product, Tag


def _clean_tag_filters(raw_tag_slugs):
    """Normalize repeated tag query parameters into a unique, non-empty slug list."""
    seen = set()
    cleaned_slugs = []

    for raw_slug in raw_tag_slugs:
        slug = raw_slug.strip()
        if not slug or slug in seen:
            continue
        seen.add(slug)
        cleaned_slugs.append(slug)
    return cleaned_slugs


def _highlight_parts(text, search_query):
    if not search_query:
        return [[text, False]]

    parts = []
    start = 0
    search_query_lower = search_query.lower()
    text_lower = text.lower()
    query_length = len(search_query)

    while True:
        match_start = text_lower.find(search_query_lower, start)
        if match_start == -1:
            if start < len(text):
                parts.append([text[start:], False])
            break

        if match_start > start:
            parts.append([text[start:match_start], False])

        match_end = match_start + query_length
        parts.append([text[match_start:match_end], True])
        start = match_end

    return parts


def product_list(request):
    """List active products with optional `q`, `category`, and repeated `tags` filters."""
    search_query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()
    selected_tags = _clean_tag_filters(request.GET.getlist("tags"))

    categories = Category.objects.all()
    tags = Tag.objects.all()

    products = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related("tags")
    )

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    if selected_category:
        products = products.filter(category__slug=selected_category)

    if selected_tags:
        # Multiple tag joins can duplicate rows, so the result set is de-duplicated.
        products = products.filter(tags__slug__in=selected_tags).distinct()

    names = list()
    descriptions = list()
    
    for product in products:

        name = product.name
        description = product.description

        names.append(_highlight_parts(name, search_query))
        descriptions.append(_highlight_parts(description, search_query))

    products_zipped = zip(products, names, descriptions)

    context = {
        "products": products_zipped,
        "categories": categories,
        "tags": tags,
        "search_query": search_query,
        "selected_category": selected_category,
        "selected_tags": selected_tags,
        "result_count": products.count(),
    }
    return render(request, "catalog/product_list.html", context)
