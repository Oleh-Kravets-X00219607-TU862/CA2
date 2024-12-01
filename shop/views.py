from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Order, Recommendation
from django.core.paginator import Paginator, EmptyPage, InvalidPage
#import pandas as pd
#from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth.decorators import login_required

def prod_list(request, category_id=None):
    category = None
    products = Product.objects.filter(available=True)

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, available=True)
    
    paginator = Paginator(products, 6)
    try: 
        page = int(request.GET.get('page', '1'))
    except: 
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop/category.html', {'category': category, 'prods': products})

def product_detail(request, category_id, product_id):
    product = get_object_or_404(Product, category_id=category_id, id=product_id)
    return render(request, 'shop/product.html', {'product': product})

# def update_recommendations():
#     orders = Order.objects.all().values('user_id', 'product_id')
#     df = pd.DataFrame(list(orders))

#     # Create User-Product Matrix
#     user_product_matrix = df.pivot_table(index='user_id', columns='product_id', aggfunc='size', fill_value=0)

#     # Compute Similarity
#     similarity_matrix = cosine_similarity(user_product_matrix)

#     # Save Recommendations
#     Recommendation.objects.all().delete()  # Clear old recommendations
#     for user_idx, user_id in enumerate(user_product_matrix.index):
#         similarity_scores = similarity_matrix[user_idx]
#         similar_users = similarity_scores.argsort()[-6:-1][::-1]

#         recommended_products = set()
#         for similar_user in similar_users:
#             user_products = user_product_matrix.iloc[similar_user].nonzero()[0]
#             recommended_products.update(user_product_matrix.columns[user_products])

#         for product_id in recommended_products:
#             if product_id not in user_product_matrix.columns[user_idx]:
#                 Recommendation.objects.create(user_id=user_id, product_id=product_id, score=similarity_scores[user_idx])


# @login_required
# def recommended_products(request):
#     user = request.user
#     recommendations = Recommendation.objects.filter(user=user)[:6]
#     return render(request, 'shop/recommendations.html', {'recommendations': recommendations})
