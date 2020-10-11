from django.shortcuts import render


def contact_page_show(request):
    return render(request, 'contact_us/contact_us_page.html')
