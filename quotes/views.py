from django.shortcuts import render,redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

# Create your views here.

def home(request):
	import requests
	if request.method=="POST":
		ticker=request.POST['ticker']
		lst=["latestPrice","previousClose","marketCap","ytdChange","week52Low","week52High"]
		api_request=requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/quote?token=pk_74fadf1d686740de85a54d26b2e644ba")
		try:
			api=api_request.json()
		except Exception as e:
			api="error"

		return render(request, 'home.html', {'api':api,'lst':lst})
	else:
		return render(request, 'home.html', {'ticker':'please enter a ticker value'})

	

def about(request):

	return render(request, 'about.html', {})

def add_stock(request):
	if request.method=="POST":
		form=StockForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request,"Stock has been added succesfully!")
			return redirect('add_stock')
	else:
		import requests
		ticker=Stock.objects.all()
		lst=["latestPrice","previousClose","marketCap","ytdChange","week52Low","week52High"]
		output=[]
		for ticker_item in ticker:
			api_request=requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker_item.ticker +"/quote?token=pk_74fadf1d686740de85a54d26b2e644ba")
			try:
				api=api_request.json()
			except Exception as e:
				api="error"
			output.append(api)

		return render(request, 'add_stock.html', {'lst':lst,'output':output,'ticker':ticker})
		
		

		
def delete(request,stock_id):
	item=Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request,"Stock has been deleted succesfully!")
	return redirect('delete_stock')

def delete_stock(request):
	ticker=Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker':ticker})
	