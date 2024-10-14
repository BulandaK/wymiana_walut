import xml.etree.ElementTree as ET

class Currency():
    def __init__(self,name,factor,code,rate):
        self.__name = name
        self.__factor = factor
        self.__code = code
        self.__rate = rate
    def getRate(self):
        return self.__rate
    def getName(self):
        return self.__name
    def getCode(self):
        return self.__code
    def getFactor(self):
        return  self.__factor

class CurrencyCollection():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrencyCollection, cls).__new__(cls)
            cls._instance._currencies = []  # Inicjalizacja listy walut
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
        return None  # Zwraca None, jeśli waluta nie została znaleziona

class DataParser():
    # Parsowanie pliku XML
    def parseData(self,path):
        tree = ET.parse(path)
        root = tree.getroot()

        # Wyciągnięcie danych z pliku

        for pozycja in root.findall('pozycja'):
            nazwa_waluty = pozycja.find('nazwa_waluty').text
            przelicznik = pozycja.find('przelicznik').text
            kod_waluty = pozycja.find('kod_waluty').text
            kurs_sredni = pozycja.find('kurs_sredni').text
            newCurrency = Currency(nazwa_waluty,przelicznik,kod_waluty,kurs_sredni)
            collection = CurrencyCollection()
            collection.addCurrency(newCurrency)

class Exchange():
    def exchangeCurrency(self,amount,baseCode,targetCode):

        allCurrencies = CurrencyCollection()

        targetCurr = allCurrencies.getCurrencyByCode(targetCode)
        baseCurr = allCurrencies.getCurrencyByCode(baseCode)

        targetRate = float(targetCurr.getRate().replace(',','.'))
        targetFactor = float(targetCurr.getFactor())

        baseRate = float(baseCurr.getRate().replace(',','.'))
        baseFactor = float(baseCurr.getFactor())


        newMoney = amount * ((baseRate / baseFactor) / (targetRate / targetFactor))

        return newMoney

class UserInterface():
    def start(self):
        while True:
            amountOfBaseCurrency = None
            baseCurrency = None
            targetCurrency = None
            collection = CurrencyCollection()

            while baseCurrency == None:
                baseCurrency = collection.getCurrencyByCode(input('podaj kod waluty bazowej:').upper())
                if (baseCurrency == None):
                    print('nie ma waluty o takim kodzie')

            while amountOfBaseCurrency is None:
                try:
                    amountOfBaseCurrency = float(input('Podaj ilość bazowej waluty: '))
                except ValueError:
                    print('Można podać tylko liczbę.')


            while targetCurrency == None:
                targetCurrency = collection.getCurrencyByCode(input('podaj kod waluty docelowej:').upper())
                if (targetCurrency == None):
                    print('nie ma waluty o takim kodzie')

            myCantor = Exchange()
            exchangedMoney = myCantor.exchangeCurrency(amountOfBaseCurrency, baseCurrency.getCode(),
                                                       targetCurrency.getCode())
            print(f'Z waluty {baseCurrency.getName()} o ilości {amountOfBaseCurrency} do waluty {targetCurrency.getName()} wyszło: {exchangedMoney}')
            print('\n\n\n')



myDataParser = DataParser()
myDataParser.parseData('waluty.xml')

myCollection = CurrencyCollection()

polskiZloty = Currency("polski złoty",'1.0',"PLN",'1.0')

myCollection.addCurrency(polskiZloty)

UserInterface().start()
