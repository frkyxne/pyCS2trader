from config import ItemsAnalyzer


class CsItem:
    def __init__(self, hash_name: str, error: str = None, buff_url: str = None, buff_price: float = None,
                 market_price: float = None):
        self.__hash_name = hash_name
        self.__buff_url = buff_url
        self.__buff_price = buff_price
        self.__market_price = market_price

        self.processing_error = error

    def __repr__(self):
        """
        Packs all properties into multiple lines representation.
        :return: multiple lines string.
        """
        representation = 'Cs item representation.\n\n'
        representation += f'Hash name: {self.__hash_name}\n'

        if self.processing_error is not None:
            representation += f'Processing error: {self.processing_error}\n'

        if self.buff_cost_price is not None:
            representation += f'Buff cost price: {self.buff_cost_price}₽\n'

        if self.__market_cost_price() is not None:
            representation += f'Market cost price: {self.__market_cost_price()}₽\n'

        if self.profit_rub is not None and self.profit_percent is not None:
            representation += f'Profit: {self.profit_rub}₽ ({self.profit_percent}%)\n'

        if self.__buff_url is not None:
            representation += f'Buff url: {self.__buff_url}\n'
            representation += f'Market url: {self.__market_url()}'

        return representation

    @property
    def hash_name(self):
        return self.__hash_name

    @property
    def profit_rub(self):
        if self.__market_cost_price() is None or self.__buff_price is None:
            return None

        return self.__market_cost_price() - self.buff_cost_price

    @property
    def profit_percent(self):
        if self.profit_rub is None or self.buff_cost_price is None:
            return None

        return round(self.profit_rub / self.buff_cost_price, 2) * 100

    @property
    def buff_cost_price(self):
        """
        How much you need to deposit to buff, to afford this item.
        :return: int of rubbles.
        """
        if self.__buff_price is None:
            return None

        return round(self.__buff_price * ItemsAnalyzer.RUB_TO_CNY / ItemsAnalyzer.BUFF_DEPOSIT_MODIFIER)

    @property
    def short_repr(self) -> str:
        """
        Short representation that fits two lines.
        :return: hash name \n profit (rub) profit (%)
        """
        return f'{self.__hash_name}\nProfit: {self.profit_rub}₽ ({self.profit_percent}%)'

    @property
    def properties_array(self) -> []:
        """
        Packs all properties in array.
        :return: [hash_name, cost_price, profit_rub, profit_percent]
        """
        return [self.__hash_name, self.buff_cost_price, self.profit_rub, self.profit_percent]

    def __market_cost_price(self):
        """
        How much can you get if you offer it at the lowest price.
        :return: int of rubbles.
        """
        if self.__market_price is None:
            return None

        return round(self.__market_price * ItemsAnalyzer.MARKET_WITHDRAW_MODIFIER)

    def __market_url(self):
        return f'https://market.csgo.com/en/{self.__hash_name.replace(" ", "")}'


class LackOfData(Exception):
    pass
