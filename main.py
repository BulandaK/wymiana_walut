import xml.etree.ElementTree as ET
import requests

class Currency:
    def __init__(self, name, code, rate):
        self.__name = name
        self.__code = code
        self.__rate = rate

    def getRate(self):
        return self.__rate

    def getName(self):
        return self.__name

    def getCode(self):
        return self.__code


class CurrencyCollection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrencyCollection, cls).__new__(cls)
            cls._instance._currencies = []
        return cls._instance

    def addCurrency(self, currency):
        """Dodaje nową walutę do kolekcji"""
        self._currencies.append(currency)

    def getCurrencies(self):
        """Zwraca listę wszystkich walut"""
        return self._currencies

    def getCurrencyByCode(self, code):
        """Znajduje walutę na podstawie jej kodu"""
        for currency in self._currencies:
            if currency.getCode() == code:
                return currency
        return None


class DataParser:
    def getRawData(self, url):
        response = requests.get(url)
        return response

    def parseApiData(self, rawData):
        data = rawData.json()
        for i in data[0]['rates']:
            name = i['currency']
            code = i['code']
            rate = i['mid']
            newCurrency = Currency(name, code, rate)
            collection = CurrencyCollection()
            collection.addCurrency(newCurrency)


class Exchange:
    def exchangeCurrency(self, amount, baseCode, targetCode):
        allCurrencies = CurrencyCollection()
        targetCurr = allCurrencies.getCurrencyByCode(targetCode)
        baseCurr = allCurrencies.getCurrencyByCode(baseCode)
        newMoney = amount * (baseCurr.getRate() / targetCurr.getRate())
        return newMoney


class UserInterface:
    def start(self):
        while True:
            amountOfBaseCurrency = None
            baseCurrency = None
            targetCurrency = None
            collection = CurrencyCollection()

            while baseCurrency is None:
                baseCurrency = collection.getCurrencyByCode(input('Podaj kod waluty bazowej:').upper())
                if baseCurrency is None:
                    print('Nie ma waluty o takim kodzie')

            while amountOfBaseCurrency is None:
                try:
                    amountOfBaseCurrency = float(input('Podaj ilość bazowej waluty: '))
                except ValueError:
                    print('Można podać tylko liczbę.')

            while targetCurrency is None:
                targetCurrency = collection.getCurrencyByCode(input('Podaj kod waluty docelowej:').upper())
                if targetCurrency is None:
                    print('Nie ma waluty o takim kodzie')

            myCantor = Exchange()
            exchangedMoney = myCantor.exchangeCurrency(
                amountOfBaseCurrency, baseCurrency.getCode(), targetCurrency.getCode())

            print(f'Z waluty {baseCurrency.getName()} o ilości {amountOfBaseCurrency} '
                  f'do waluty {targetCurrency.getName()} wyszło: {exchangedMoney}')
            print('\n\n\n')


# Parsowanie danych i uruchamianie interfejsu
myDataParser = DataParser()
response = myDataParser.getRawData("https://api.nbp.pl/api/exchangerates/tables/a/")

if response.status_code != 200:
    print('Niestety nie udało się pobrać danych, problem z siecią')
else:
    myDataParser.parseApiData(response)
    # Dodajemy polski złoty
    myCollection = CurrencyCollection()
    polskiZloty = Currency("polski złoty", "PLN", 1.0)
    myCollection.addCurrency(polskiZloty)
    UserInterface().start()
