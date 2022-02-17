from django.shortcuts import render
from django.http import HttpResponse

def products(request):
    context = {
        "shirts": [
            {
                "name": "001",
                "price": 120,
                "img": "./001/purple.jpg",  
                "size": "free"
            },
            {
                "name": "002",
                "price": 120,
                "img": "./002/gray.jpg",  
                "size": "free"
            },
            {
                "name": "003",
                "price": 120,
                "img": "./003/white.jpg",  
                "size": "free"
            },
            {
                "name": "004",
                "price": 120,
                "img": "./004/yellow.jpg",  
                "size": "free"
            },
            {
                "name": "005",
                "price": 120,
                "img": "./005/white.jpg",  
                "size": "free"
            },
            {
                "name": "006",
                "price": 120,
                "img": "./006/black.jpg",  
                "size": "free"
            }
        ]
    }

    return render(request, "products.html", context=context)

def welcome(requet):
    return HttpResponse("Welcome to the OnlineShop")
