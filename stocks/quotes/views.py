from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.conf import settings
from .models import Stock
from .forms import StockForm
from django.contrib import messages
import json
import os

# Create your views here.
def home(request):
    import requests
    # import json


    if request.method == 'POST':
        ticker = request.POST['ticker']
        # url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey=QFX39C38SS9D090O"
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=QFX39C38SS9D090O"
        api_request = requests.get(url)
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error ..."
        return render(request, 'Home.html', {'api' : api})
    else:
        return render(request, 'Home.html', {'ticker':"Enter Ticker Information"})

def about(request):
    return render(request, 'About.html', {})

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'Delete_stock.html', {'ticker' : ticker})

def add_stock(request):
    import requests
    # import json
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request,("Stock Has been Added successfully"))
            return redirect('Add Stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={str(ticker_item)}&apikey=QFX39C38SS9D090O"
            api_request = requests.get(url)
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error ..."
        return render(request, 'Add_stock.html', {'ticker' : ticker, 'output' : output})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request,("Stock deleted successfully"))
    # return redirect('Add Stock')
    return redirect('Delete Stock')

def thirukkural(request):
    # data={"kural": [
    # {
    #   "Number": 1,
    #   "Line1": "அகர முதல எழுத்தெல்லாம் ஆதி",
    #   "Line2": "பகவன் முதற்றே உலகு.",
    #   "Translation": "'A' leads letters; the Ancient Lord Leads and lords the entire world",
    #   "mv": "எழுத்துக்கள் எல்லாம் அகரத்தை அடிப்படையாக கொண்டிருக்கின்றன. அதுபோல உலகம் கடவுளை அடிப்படையாக கொண்டிருக்கிறது.",
    #   "sp": "எழுத்துக்கள் எல்லாம் அகரத்தில் தொடங்குகின்றன; (அது போல) உலகம் கடவுளில் தொடங்குகிறது.",
    #   "mk": "அகரம் எழுத்துக்களுக்கு முதன்மை; ஆதிபகவன், உலகில் வாழும் உயிர்களுக்கு முதன்மை",
    #   "explanation": "As the letter A is the first of all letters, so the eternal God is first in the world",
    #   "couplet": "A, as its first of letters, every speech maintains;The \"Primal Deity\" is first through all the world's domains",
    #   "transliteration1": "Akara Mudhala Ezhuththellaam Aadhi",
    #   "transliteration2": "Pakavan Mudhatre Ulaku"
    # }]}
     # Path to your JSON file
    # import json
    # json_file_path = '/stocks/quotes/templates/thirukkural.json'
    json_file_path = os.path.join(settings.BASE_DIR, 'thirukkural.json')
    try:
        # Open and load the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Optionally, you can render this data in a template if you want to display it in HTML
        return render(request, 'Thirukkural.html', {'data': data})

    except FileNotFoundError:
        e_message = f"File not found: {json_file_path}"
        print(e_message)
        return JsonResponse({'error': e_message}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error decoding JSON'}, status=400)
    # return render(request, 'Thirukkural.html', {'data': data})

def show_stock_data(request):
    data = {'Meta Data': {'1. Information': 'Intraday (5min) open, high, low, close prices and volume', '2. Symbol': 'IBM', '3. Last Refreshed': '2024-12-12 19:55:00', '4. Interval': '5min', '5. Output Size': 'Compact', '6. Time Zone': 'US/Eastern'}, 'Time Series (5min)': {'2024-12-12 19:55:00': {'1. open': '232.6500', '2. high': '232.6500', '3. low': '232.2833', '4. close': '232.2833', '5. volume': '31'}, '2024-12-12 19:50:00': {'1. open': '232.7000', '2. high': '232.7000', '3. low': '232.5000', '4. close': '232.5000', '5. volume': '1634'}, '2024-12-12 19:40:00': {'1. open': '232.7000', '2. high': '232.7000', '3. low': '232.7000', '4. close': '232.7000', '5. volume': '1'}, '2024-12-12 19:35:00': {'1. open': '232.5700', '2. high': '232.7000', '3. low': '232.5700', '4. close': '232.7000', '5. volume': '250'}, '2024-12-12 19:25:00': {'1. open': '232.5100', '2. high': '232.5800', '3. low': '232.5000', '4. close': '232.5800', '5. volume': '67'}, '2024-12-12 19:20:00': {'1. open': '232.2500', '2. high': '232.2500', '3. low': '232.2500', '4. close': '232.2500', '5. volume': '2'}, '2024-12-12 19:15:00': {'1. open': '232.4900', '2. high': '232.5700', '3. low': '232.4900', '4. close': '232.5700', '5. volume': '97'}, '2024-12-12 19:10:00': {'1. open': '232.2600', '2. high': '232.2600', '3. low': '232.2600', '4. close': '232.2600', '5. volume': '10'}, '2024-12-12 19:05:00': {'1. open': '232.5800', '2. high': '232.5800', '3. low': '232.5800', '4. close': '232.5800', '5. volume': '15'}, '2024-12-12 19:00:00': {'1. open': '232.2600', '2. high': '232.2600', '3. low': '232.2500', '4. close': '232.2500', '5. volume': '1424744'}, '2024-12-12 18:50:00': {'1. open': '232.2500', '2. high': '232.5800', '3. low': '232.2500', '4. close': '232.5800', '5. volume': '14'}, '2024-12-12 18:45:00': {'1. open': '232.2900', '2. high': '232.2900', '3. low': '232.2600', '4. close': '232.2600', '5. volume': '50'}, '2024-12-12 18:40:00': {'1. open': '232.5500', '2. high': '232.5500', '3. low': '232.5500', '4. close': '232.5500', '5. volume': '100'}, '2024-12-12 18:30:00': {'1. open': '232.2600', '2. high': '232.2600', '3. low': '232.2600', '4. close': '232.2600', '5. volume': '1424722'}, '2024-12-12 18:25:00': {'1. open': '232.3700', '2. high': '232.3700', '3. low': '232.3700', '4. close': '232.3700', '5. volume': '25'}, '2024-12-12 18:15:00': {'1. open': '232.5800', '2. high': '232.5800', '3. low': '232.5800', '4. close': '232.5800', '5. volume': '2'}, '2024-12-12 18:10:00': {'1. open': '232.2600', '2. high': '232.2600', '3. low': '232.2600', '4. close': '232.2600', '5. volume': '2684'}, '2024-12-12 18:05:00': {'1. open': '232.0100', '2. high': '232.0100', '3. low': '232.0100', '4. close': '232.0100', '5. volume': '5'}, '2024-12-12 17:55:00': {'1. open': '232.5700', '2. high': '232.5700', '3. low': '232.5700', '4. close': '232.5700', '5. volume': '6'}, '2024-12-12 17:50:00': {'1. open': '232.2100', '2. high': '232.3400', '3. low': '232.0100', '4. close': '232.0100', '5. volume': '120'}, '2024-12-12 17:45:00': {'1. open': '232.5700', '2. high': '232.5800', '3. low': '232.5700', '4. close': '232.5800', '5. volume': '21'}, '2024-12-12 17:35:00': {'1. open': '232.5788', '2. high': '232.5788', '3. low': '232.5788', '4. close': '232.5788', '5. volume': '1'}, '2024-12-12 17:30:00': {'1. open': '232.5800', '2. high': '232.5800', '3. low': '232.5800', '4. close': '232.5800', '5. volume': '2'}, '2024-12-12 17:25:00': {'1. open': '232.5700', '2. high': '232.5700', '3. low': '232.0100', '4. close': '232.0100', '5. volume': '31'}, '2024-12-12 17:20:00': {'1. open': '232.5300', '2. high': '232.5800', '3. low': '232.5300', '4. close': '232.5300', '5. volume': '28'}, '2024-12-12 17:15:00': {'1. open': '232.6400', '2. high': '232.6400', '3. low': '232.0000', '4. close': '232.0000', '5. volume': '14'}, '2024-12-12 17:10:00': {'1. open': '231.9880', '2. high': '231.9880', '3. low': '231.9880', '4. close': '231.9880', '5. volume': '20'}, '2024-12-12 17:05:00': {'1. open': '232.3000', '2. high': '232.6000', '3. low': '232.3000', '4. close': '232.6000', '5. volume': '8'}, '2024-12-12 17:00:00': {'1. open': '232.2600', '2. high': '232.2600', '3. low': '232.2600', '4. close': '232.2600', '5. volume': '17'}, '2024-12-12 16:55:00': {'1. open': '232.8000', '2. high': '232.8000', '3. low': '232.8000', '4. close': '232.8000', '5. volume': '7'}, '2024-12-12 16:50:00': {'1. open': '232.2600', '2. high': '232.2600', '3. low': '232.2600', '4. close': '232.2600', '5. volume': '386'}, '2024-12-12 16:40:00': {'1. open': '232.2000', '2. high': '232.2800', '3. low': '232.0300', '4. close': '232.2600', '5. volume': '375'}, '2024-12-12 16:35:00': {'1. open': '232.4500', '2. high': '232.4500', '3. low': '232.4500', '4. close': '232.4500', '5. volume': '30'}, '2024-12-12 16:25:00': {'1. open': '232.2700', '2. high': '232.2700', '3. low': '232.2700', '4. close': '232.2700', '5. volume': '12'}, '2024-12-12 16:20:00': {'1. open': '232.2600', '2. high': '232.6000', '3. low': '232.2600', '4. close': '232.6000', '5. volume': '590'}, '2024-12-12 16:15:00': {'1. open': '232.2600', '2. high': '232.8000', '3. low': '232.2600', '4. close': '232.7800', '5. volume': '71'}, '2024-12-12 16:10:00': {'1. open': '232.2600', '2. high': '233.0000', '3. low': '232.2600', '4. close': '232.2600', '5. volume': '1426323'}, '2024-12-12 16:05:00': {'1. open': '232.2600', '2. high': '233.5983', '3. low': '232.2600', '4. close': '232.2700', '5. volume': '3508'}, '2024-12-12 16:00:00': {'1. open': '232.2600', '2. high': '232.3400', '3. low': '222.9700', '4. close': '232.2600', '5. volume': '3068168'}, '2024-12-12 15:55:00': {'1. open': '232.8100', '2. high': '232.8800', '3. low': '232.2300', '4. close': '232.2600', '5. volume': '315777'}, '2024-12-12 15:50:00': {'1. open': '233.0700', '2. high': '233.0750', '3. low': '232.6900', '4. close': '232.8250', '5. volume': '103880'}, '2024-12-12 15:45:00': {'1. open': '233.0300', '2. high': '233.2400', '3. low': '232.9200', '4. close': '233.1100', '5. volume': '77681'}, '2024-12-12 15:40:00': {'1. open': '233.0850', '2. high': '233.0850', '3. low': '232.7800', '4. close': '233.0200', '5. volume': '53310'}, '2024-12-12 15:35:00': {'1. open': '233.4532', '2. high': '233.5100', '3. low': '233.0800', '4. close': '233.1100', '5. volume': '31827'}, '2024-12-12 15:30:00': {'1. open': '233.1450', '2. high': '233.4838', '3. low': '233.0700', '4. close': '233.4838', '5. volume': '32736'}, '2024-12-12 15:25:00': {'1. open': '233.4000', '2. high': '233.4500', '3. low': '233.1300', '4. close': '233.1300', '5. volume': '29006'}, '2024-12-12 15:20:00': {'1. open': '233.3800', '2. high': '233.5000', '3. low': '233.2900', '4. close': '233.3550', '5. volume': '32539'}, '2024-12-12 15:15:00': {'1. open': '233.2800', '2. high': '233.5700', '3. low': '233.2800', '4. close': '233.4787', '5. volume': '31688'}, '2024-12-12 15:10:00': {'1. open': '233.3700', '2. high': '233.4400', '3. low': '233.1100', '4. close': '233.2200', '5. volume': '25125'}, '2024-12-12 15:05:00': {'1. open': '233.0800', '2. high': '233.4994', '3. low': '233.0800', '4. close': '233.3450', '5. volume': '31303'}, '2024-12-12 15:00:00': {'1. open': '232.5400', '2. high': '233.2850', '3. low': '232.5400', '4. close': '233.0900', '5. volume': '66776'}, '2024-12-12 14:55:00': {'1. open': '232.3650', '2. high': '232.5400', '3. low': '232.3000', '4. close': '232.5400', '5. volume': '23468'}, '2024-12-12 14:50:00': {'1. open': '232.6600', '2. high': '232.6600', '3. low': '232.3000', '4. close': '232.3850', '5. volume': '21865'}, '2024-12-12 14:45:00': {'1. open': '232.8170', '2. high': '232.8999', '3. low': '232.6300', '4. close': '232.6400', '5. volume': '16356'}, '2024-12-12 14:40:00': {'1. open': '232.7300', '2. high': '232.8289', '3. low': '232.6400', '4. close': '232.8100', '5. volume': '17901'}, '2024-12-12 14:35:00': {'1. open': '232.5800', '2. high': '232.8500', '3. low': '232.5200', '4. close': '232.7750', '5. volume': '15366'}, '2024-12-12 14:30:00': {'1. open': '232.3800', '2. high': '232.6500', '3. low': '232.3100', '4. close': '232.5850', '5. volume': '15722'}, '2024-12-12 14:25:00': {'1. open': '232.5300', '2. high': '232.5600', '3. low': '232.3020', '4. close': '232.3020', '5. volume': '13867'}, '2024-12-12 14:20:00': {'1. open': '232.6600', '2. high': '232.6700', '3. low': '232.4100', '4. close': '232.5500', '5. volume': '14810'}, '2024-12-12 14:15:00': {'1. open': '232.6700', '2. high': '232.6900', '3. low': '232.5400', '4. close': '232.6600', '5. volume': '17195'}, '2024-12-12 14:10:00': {'1. open': '232.8900', '2. high': '232.8900', '3. low': '232.6601', '4. close': '232.7050', '5. volume': '17728'}, '2024-12-12 14:05:00': {'1. open': '233.1700', '2. high': '233.2200', '3. low': '232.8767', '4. close': '232.8767', '5. volume': '11371'}, '2024-12-12 14:00:00': {'1. open': '233.2250', '2. high': '233.2250', '3. low': '233.0500', '4. close': '233.1400', '5. volume': '17207'}, '2024-12-12 13:55:00': {'1. open': '233.1525', '2. high': '233.2950', '3. low': '233.1401', '4. close': '233.2200', '5. volume': '20685'}, '2024-12-12 13:50:00': {'1. open': '233.0700', '2. high': '233.1900', '3. low': '233.0350', '4. close': '233.1300', '5. volume': '21435'}, '2024-12-12 13:45:00': {'1. open': '233.1200', '2. high': '233.1500', '3. low': '232.9500', '4. close': '233.0500', '5. volume': '23367'}, '2024-12-12 13:40:00': {'1. open': '233.0550', '2. high': '233.1700', '3. low': '233.0300', '4. close': '233.1100', '5. volume': '16679'}, '2024-12-12 13:35:00': {'1. open': '233.2650', '2. high': '233.3000', '3. low': '232.9850', '4. close': '233.0550', '5. volume': '19905'}, '2024-12-12 13:30:00': {'1. open': '233.5500', '2. high': '233.5550', '3. low': '233.2600', '4. close': '233.2650', '5. volume': '17439'}, '2024-12-12 13:25:00': {'1. open': '233.8652', '2. high': '233.8900', '3. low': '233.5100', '4. close': '233.5350', '5. volume': '22382'}, '2024-12-12 13:20:00': {'1. open': '233.7000', '2. high': '233.8872', '3. low': '233.6700', '4. close': '233.8872', '5. volume': '16580'}, '2024-12-12 13:15:00': {'1. open': '233.1300', '2. high': '233.7600', '3. low': '233.1200', '4. close': '233.6475', '5. volume': '429755'}, '2024-12-12 13:10:00': {'1. open': '233.2000', '2. high': '233.2200', '3. low': '233.1200', '4. close': '233.1650', '5. volume': '11478'}, '2024-12-12 13:05:00': {'1. open': '232.8600', '2. high': '233.1900', '3. low': '232.8400', '4. close': '233.1800', '5. volume': '11111'}, '2024-12-12 13:00:00': {'1. open': '233.1200', '2. high': '233.1500', '3. low': '232.8000', '4. close': '232.8400', '5. volume': '14849'}, '2024-12-12 12:55:00': {'1. open': '232.7800', '2. high': '233.2356', '3. low': '232.7800', '4. close': '233.1500', '5. volume': '15979'}, '2024-12-12 12:50:00': {'1. open': '232.8550', '2. high': '232.9400', '3. low': '232.6800', '4. close': '232.7700', '5. volume': '19187'}, '2024-12-12 12:45:00': {'1. open': '232.7500', '2. high': '232.9026', '3. low': '232.7450', '4. close': '232.8700', '5. volume': '39223'}, '2024-12-12 12:40:00': {'1. open': '232.9800', '2. high': '233.0099', '3. low': '232.7300', '4. close': '232.7850', '5. volume': '15356'}, '2024-12-12 12:35:00': {'1. open': '232.7550', '2. high': '233.1200', '3. low': '232.6600', '4. close': '233.0400', '5. volume': '14495'}, '2024-12-12 12:30:00': {'1. open': '232.7700', '2. high': '232.8102', '3. low': '232.6700', '4. close': '232.7150', '5. volume': '13447'}, '2024-12-12 12:25:00': {'1. open': '232.5300', '2. high': '232.7700', '3. low': '232.5000', '4. close': '232.7700', '5. volume': '12382'}, '2024-12-12 12:20:00': {'1. open': '232.6000', '2. high': '232.6018', '3. low': '232.4200', '4. close': '232.5300', '5. volume': '12793'}, '2024-12-12 12:15:00': {'1. open': '232.3550', '2. high': '232.6360', '3. low': '232.3550', '4. close': '232.6333', '5. volume': '9359'}, '2024-12-12 12:10:00': {'1. open': '232.4100', '2. high': '232.4900', '3. low': '232.3100', '4. close': '232.3300', '5. volume': '12506'}, '2024-12-12 12:05:00': {'1. open': '232.4350', '2. high': '232.6000', '3. low': '232.3500', '4. close': '232.4400', '5. volume': '16388'}, '2024-12-12 12:00:00': {'1. open': '232.3500', '2. high': '232.4650', '3. low': '232.3201', '4. close': '232.4500', '5. volume': '9553'}, '2024-12-12 11:55:00': {'1. open': '232.6600', '2. high': '232.6700', '3. low': '232.3400', '4. close': '232.3400', '5. volume': '18984'}, '2024-12-12 11:50:00': {'1. open': '232.6700', '2. high': '232.7900', '3. low': '232.5900', '4. close': '232.6500', '5. volume': '18221'}, '2024-12-12 11:45:00': {'1. open': '232.6750', '2. high': '232.6900', '3. low': '232.5238', '4. close': '232.6210', '5. volume': '14827'}, '2024-12-12 11:40:00': {'1. open': '232.7300', '2. high': '232.7800', '3. low': '232.6100', '4. close': '232.6800', '5. volume': '12131'}, '2024-12-12 11:35:00': {'1. open': '232.6200', '2. high': '232.8350', '3. low': '232.5900', '4. close': '232.6600', '5. volume': '14853'}, '2024-12-12 11:30:00': {'1. open': '233.1450', '2. high': '233.1663', '3. low': '232.5900', '4. close': '232.6150', '5. volume': '130711'}, '2024-12-12 11:25:00': {'1. open': '233.3000', '2. high': '233.3700', '3. low': '233.1800', '4. close': '233.2000', '5. volume': '15341'}, '2024-12-12 11:20:00': {'1. open': '233.0974', '2. high': '233.3700', '3. low': '232.9101', '4. close': '233.3480', '5. volume': '24283'}, '2024-12-12 11:15:00': {'1. open': '232.6860', '2. high': '233.2200', '3. low': '232.5800', '4. close': '233.1050', '5. volume': '28236'}, '2024-12-12 11:10:00': {'1. open': '232.6750', '2. high': '232.9400', '3. low': '232.6400', '4. close': '232.7000', '5. volume': '24354'}, '2024-12-12 11:05:00': {'1. open': '232.8700', '2. high': '233.1050', '3. low': '232.7400', '4. close': '232.7400', '5. volume': '28132'}, '2024-12-12 11:00:00': {'1. open': '232.2700', '2. high': '232.9600', '3. low': '232.2300', '4. close': '232.8300', '5. volume': '22206'}, '2024-12-12 10:55:00': {'1. open': '232.1450', '2. high': '232.4800', '3. low': '232.1302', '4. close': '232.3187', '5. volume': '24647'}}}
    
    return render(request, 'Stock_data.html', {'data': data})