from currency_converter import CurrencyConverter
import schedule

EU_X_REF_URL = 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip'


class Currency:
    Converter: CurrencyConverter

    @staticmethod
    def convert(amount: float, from_currency: str, to_currency: str):
        return round(
            Currency.Converter.convert(amount or 0.0, from_currency, to_currency), 2
        )

    @staticmethod
    def crawl():
        Currency.Converter = CurrencyConverter(EU_X_REF_URL)


schedule.every(8).hours.do(Currency.crawl)
schedule.run_pending()

Currency.crawl()
