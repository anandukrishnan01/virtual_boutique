from decimal import Decimal
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.translation import gettext_lazy as _
from .forms import TestimonialForm
from .models import  Address, Brand, Cart, CartItem, Order, Product, ProductSize, ProductAlternative, Category, Testimonial
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from register.models import Vendor
from django.contrib import messages
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


@login_required
def vendor_profile_view(request):
    user = request.user
    vendor = get_object_or_404(Vendor, user=user)
    context = {
        'vendor': vendor
    }
    return render(request, 'vendor/vendor_profile.html', context)

@login_required
def vendor(request):
    return render(request,"vendor/vendor_dashboard.html")

@login_required
def addbrand(request):
    return render(request,"vendor/brand.html")

@login_required
def displaybrand(request):
    data=Brand.objects.all()
    return render(request,"vendor/brand.html",{'data':data})

@login_required
def savedata(request):
    if request.method == "POST":
        cn = request.POST.get('cname')
        des = request.POST.get('cdesc')
        img = request.FILES['cimg']
        obj = Brand(name=cn, desc=des, image=img)
        obj.save()
        return redirect(displaybrand)

@login_required
def editbrand(request,dataid):
    data = Brand.objects.get(id=dataid)
    return render(request,"vendor/brand.html",{'data':data})

@login_required
def updatebrand(request,dataid):
    if request.method=="POST":
        cn = request.POST.get('cname')
        des = request.POST.get('cdesc')
        try:
            img = request.FILES['cimg']
            fs = FileSystemStorage()
            file = fs.save(img.name,img)
        except MultiValueDictKeyError:
            file = Brand.objects.get(id=dataid).image
        Brand.objects.filter(id=dataid).update(name=cn,desc=des,image=file)
        return redirect(displaybrand)

@login_required
def deletebrand(request,dataid):
    data = Brand.objects.filter(id=dataid)
    data.delete()
    return redirect(displaybrand)
# *********************************************************************************************************************

@login_required
def manage_categories(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    return render(request, "vendor/category.html", {'brands': brands, 'categories': categories})

@login_required
def savedata1(request):
    if request.method == "POST":
        cn_id = request.POST.get('cname')  # Get the brand ID
        brand = Brand.objects.get(id=cn_id)  # Retrieve the brand object
        bn = request.POST.get('bname')
        desc = request.POST.get('bdesc')
        img = request.FILES['bimg']
        obj = Category(brand=brand, name=bn, desc=desc, image=img)
        obj.save()
        return redirect('manage_categories')

@login_required
def updatecategory(request, dataid):
    if request.method == "POST":
        cn_id = request.POST.get('cname')
        brand = Brand.objects.get(id=cn_id)
        bn = request.POST.get('bname')
        desc = request.POST.get('bdesc')

        try:
            img = request.FILES['bimg']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = Category.objects.get(id=dataid).image

        Category.objects.filter(id=dataid).update(brand=brand, name=bn, desc=desc, image=file)
        return redirect('manage_categories')
@login_required
def deletecategory(request, dataid):
    data = Category.objects.filter(id=dataid)
    data.delete()
    return redirect('manage_categories')


# ***********************************************************************************************************************


# List Products

@login_required
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    return render(request, 'vendor/product.html', {'products': products, 'categories': categories, 'brands': brands})

# Add Product

@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        category_id = request.POST['category']
        display_price = request.POST['display_price']
        selling_price = request.POST['selling_price']
        description = request.POST['description']
        image = request.FILES['image']

        category = Category.objects.get(id=category_id)
        Product.objects.create(
            name=name,
            category=category,
            display_price=display_price,
            selling_price=selling_price,
            description=description,
            image=image,
        )
        return redirect('displayproduct')

    categories = Category.objects.all()
    brands = Brand.objects.all()
    return render(request, 'vendor/product.html', {'categories': categories, 'brands': brands})

# Edit Product

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST['name']
        category_id = request.POST['category']
        product.display_price = request.POST['display_price']
        product.selling_price = request.POST['selling_price']
        product.description = request.POST['description']
        if 'image' in request.FILES:
            product.image = request.FILES['image']

        category = Category.objects.get(id=category_id)
        product.category = category
        product.save()
        return redirect('displayproduct')

    categories = Category.objects.all()
    brands = Brand.objects.all()
    return render(request, 'vendor/product.html', {'product': product, 'categories': categories, 'brands': brands})

# AJAX view to filter categories based on the selected brand
def filter_categories(request):
    brand_id = request.GET.get('brand_id')
    categories = Category.objects.filter(brand_id=brand_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

@login_required
def deleteproduct(request, dataid):
    data = Product.objects.filter(id=dataid)
    data.delete()
    return redirect('displayproduct')

# ************************************************************************************************************************

@login_required
def manage_product_sizes(request):
    products = Product.objects.all()
    sizes = ProductSize.objects.all()
    return render(request, "vendor/product_size.html", {'products': products, 'sizes': sizes})

@login_required
def save_product_size(request):
    if request.method == "POST":
        psn = request.POST.get('size')
        pro = request.POST.get('pname')
        product = Product.objects.get(id=pro)
        
        # Check if the size already exists for this product
        if ProductSize.objects.filter(name=psn, product=product).exists():
            messages.error(request, "This size already exists for the selected product. Please add another size.")
        else:
            obj = ProductSize(name=psn, product=product)
            obj.save()
            
        return redirect('manage_product_sizes')

@login_required
def update_product_size(request, dataid):
    if request.method == "POST":
        psn = request.POST.get('size')
        pro = request.POST.get('pname')
        product = Product.objects.get(id=pro)
        ProductSize.objects.filter(id=dataid).update(name=psn, product=product)
        return redirect('manage_product_sizes')

@login_required
def delete_product_size(request, dataid):
    data = ProductSize.objects.filter(id=dataid)
    data.delete()
    return redirect('manage_product_sizes')

# ************************************************************************************************************************

@login_required
def product_alternatives(request):
    if request.method == "POST":
        # Add product alternative
        product_id = request.POST.get('product')
        selling_price = request.POST.get('selling_price')
        size_id = request.POST.get('size')
        
        stock = request.POST.get('stock')

        product = Product.objects.get(id=product_id)
        size = ProductSize.objects.get(id=size_id)

        product_alternative = ProductAlternative(
            product=product,
            selling_price=selling_price,
            sizes=size,
            stock=stock
        )
        product_alternative.save()
        return redirect('product_alternatives')
    else:
        products = Product.objects.all()
        sizes = ProductSize.objects.all()
        data = ProductAlternative.objects.all()
        return render(request, "vendor/product_alternatives.html", {'data': data, 'products': products, 'sizes': sizes})
 
@login_required
def edit_product_alternative(request, dataid):
    instance = get_object_or_404(ProductAlternative, id=dataid)
    if request.method == "POST":
        # Edit product alternative
        product_id = request.POST.get('product')
        selling_price = request.POST.get('selling_price')
        size_id = request.POST.get('size')
        stock = request.POST.get('stock')

        product = Product.objects.get(id=product_id)
        size = ProductSize.objects.get(id=size_id)

        instance.product = product
        instance.selling_price = selling_price
        instance.sizes = size
        instance.stock = stock
        instance.save()
        return redirect('product_alternatives')
    else:
        products = Product.objects.all()
        sizes = ProductSize.objects.all()
        return render(request, "vendor/product_alternatives.html", {'instance': instance, 'products': products, 'sizes': sizes})
@login_required    
def delete_product_alternative(request, dataid):
    data = ProductAlternative.objects.get(id=dataid)
    data.delete()
    return redirect('product_alternatives')

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    alternatives = ProductAlternative.objects.filter(product=product)
    testimonials = Testimonial.objects.filter(product=product, is_approved=True, is_active=True)
    existing_testimonial = Testimonial.objects.filter(product=product, added_by=request.user).first()
    
    if request.method == 'POST' and not existing_testimonial:
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.product = product
            testimonial.added_by = request.user
            testimonial.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = TestimonialForm()
        
    return render(request, 'productalt_detailed.html', {
        'product': product,
        'alternatives': alternatives,
        'testimonials': testimonials,
        'form': form,
        'existing_testimonial': existing_testimonial,
    })
    
def get_alternative_selling_price(request):
    alternative_id = request.GET.get('alternative_id')
    alternative = ProductAlternative.objects.get(id=alternative_id)
    selling_price = alternative.selling_price
    return JsonResponse({'selling_price': selling_price})

################################################################################################
###################################ADD CART#####################################################
################################################################################################



@login_required
def add_to_cart(request, product_id, dataid):
    
    product_alternative = get_object_or_404(ProductAlternative, id=dataid)
    if product_alternative.stock <= 0:
        return HttpResponse("Out of stock", status=400)

    user_cart, created = Cart.objects.get_or_create(
        user=request.user,
        status='open',
        defaults={
            'subtotal': Decimal('0.00'),
            'no_of_items': 0,
            'total': Decimal('0.00'),
            'total_tax': Decimal('0.00'),
            'grand_total': Decimal('0.00'),
            'status': 'open'
        }
    )

    

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=user_cart,
        product_alternative=product_alternative,
        defaults={'qty': 1, 'total': product_alternative.selling_price}
    )
  

    if not item_created:
        cart_item.qty += 1
        cart_item.total += product_alternative.selling_price
        cart_item.save()

    product_alternative.stock -= 1
    product_alternative.save()

    update_cart_totals(user_cart)

    return JsonResponse({'success': 'Item added to cart successfully.'})
    # return HttpResponse("Item added to cart successfully")

@login_required
def display_cart_item(request):
   
    user_cart = Cart.objects.filter(user=request.user, status='open').first()
    cart_items = CartItem.objects.filter(cart=user_cart) if user_cart else []
    addresses = Address.objects.filter(user=request.user)
    selected_address = addresses.filter(is_active=True).first()

    return render(request, "index/display_cartitem.html", {
        'cart': user_cart,
        'cart_items': cart_items,
        'addresses': addresses,
        'selected_address': selected_address
    })

def update_cart_totals(cart):
    cart_items = CartItem.objects.filter(cart=cart)
    cart.no_of_items = sum(item.qty for item in cart_items)
    cart.subtotal = sum(item.total for item in cart_items)
    cart.total_tax = cart.subtotal * Decimal('0.2') if cart.subtotal else Decimal('0.00')
    cart.total = cart.subtotal + cart.total_tax
    cart.grand_total = cart.total
    cart.save()
   


@login_required
def update_cart_item(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if action == 'increase':
        cart_item.qty += 1
        cart_item.total += cart_item.product_alternative.selling_price
    elif action == 'decrease' and cart_item.qty > 1:
        cart_item.qty -= 1
        cart_item.total -= cart_item.product_alternative.selling_price

    cart_item.save()
    update_cart_totals(cart_item.cart)

    return redirect('display_cart_item')

@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = cart_item.cart
    product_alternative = cart_item.product_alternative
    product_alternative.stock += cart_item.qty
    product_alternative.save()
    cart_item.delete()
    update_cart_totals(cart)

    return redirect('display_cart_item')



@login_required
def add_address(request):
    max_addresses = 3
    if Address.objects.filter(user=request.user).count() >= max_addresses:
        context = {
            'warning': "Only 3 addresses can be used by a person. No more addresses can be added."
        }
        return render(request, 'index/display_cartitem.html', context)
    error_messages = {}

    if request.method == 'POST':
        alternative_name = request.POST.get('alternative_name')
        house_name = request.POST.get('house_name')
        post = request.POST.get('post')
        dist = request.POST.get('dist')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        alternative_phone = request.POST.get('alternative_phone')

        if len(alternative_phone) != 10 or not alternative_phone.isdigit():
            error_messages['alternative_phone'] = _('Phone number must be a 10-digit number.')
        if not zip_code.isdigit():
            error_messages['zip_code'] = _('ZIP code must contain only numbers.')
        
        if not error_messages:
            Address.objects.create(
                user=request.user,
                alternative_name=alternative_name,
                house_name=house_name,
                post=post,
                dist=dist,
                state=state,
                zip_code=zip_code,
                alternative_phone=alternative_phone,
                is_active=True
            )
            return redirect('display_cart_item')
    print(error_messages)
    return render(request, 'index/add_or_edit_address.html',{'error_messages': error_messages})

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        address.alternative_name = request.POST.get('alternative_name')
        address.house_name = request.POST.get('house_name')
        address.post = request.POST.get('post')
        address.dist = request.POST.get('dist')
        address.state = request.POST.get('state')
        address.zip_code = request.POST.get('zip_code')
        address.alternative_phone = request.POST.get('alternative_phone')
        address.save()
        return redirect('display_cart_item')

    return render(request, 'index/add_or_edit_address.html', {'address': address})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    return redirect('display_cart_item')

@login_required
def select_address(request, address_id):
    Address.objects.filter(user=request.user).update(is_active=False)
    selected_address = get_object_or_404(Address, id=address_id, user=request.user)
    selected_address.is_active = True
    selected_address.save()
    return redirect('display_cart_item')

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def checkout_page(request):
    user_cart = Cart.objects.filter(user=request.user, status='open').first()
    address = Address.objects.filter(user=request.user, is_active=True).first()
    cart_items = CartItem.objects.filter(cart=user_cart)

    if user_cart and address:
        if request.method == 'POST':
            amount = int(user_cart.grand_total * 100)  # Amount in paisa

            razorpay_order = client.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': '1'
            })

            order = Order.objects.create(
                user=request.user,
                cart=user_cart,
                address=address,
                razorpay_order_id=razorpay_order['id'],
                amount=user_cart.grand_total
            )

            context = {
                'amount': amount,
                'api_key': settings.RAZORPAY_KEY_ID,
                'order_id': razorpay_order['id'],
                'user_email': request.user.email,
                'user_contact': request.user.phone_number,
                'address': address,
                'cart_items': cart_items,
                'cart': user_cart,
            }

            return render(request, 'index/checkout_page.html', context)

        context = {
            'cart': user_cart,
            'address': address,
            'cart_items': cart_items,
        }
        return render(request, 'index/checkout_page.html', context)
    else:
        return redirect('display_cart_item')

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        try:
            response = request.POST
            order_id = response.get('razorpay_order_id')
            if not order_id:
                messages.error(request, "Invalid request: Missing razorpay_order_id")
                return HttpResponseBadRequest("Invalid request: Missing razorpay_order_id")

            order = get_object_or_404(Order, razorpay_order_id=order_id)
            # Additional validation and security checks can be performed here

            # Update order status
            order.status = 'confirmed'
            order.save()

            # Update cart status
            cart = order.cart
            cart.status = 'confirmed'
            cart.save()

            # Provide feedback to the user
            messages.success(request, "Payment successful! Your order has been confirmed.")
            return render(request, 'index/payment_success.html', {'order': order})
        except Exception as e:
            # Handle any unexpected errors
            messages.error(request, "An error occurred while processing your payment.")
            return HttpResponseServerError("An error occurred while processing your payment.")

    messages.error(request, "Invalid request method")
    return HttpResponseBadRequest("Invalid request method")


