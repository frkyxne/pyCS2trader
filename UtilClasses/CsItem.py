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
        representation = f'{"-"*23}\nCs item representation.\n\n'
        representation += f'Hash name: {self.__hash_name}\n'

        if self.processing_error is not None:
            representation += f'Processing error: {self.processing_error}\n\n'

        if self.__buff_price is not None:
            representation += f'Buff price: {self.__buff_price}¥\n'

        if self.__market_price is not None:
            representation += f'Market price: {self.__market_price}₽\n\n'

        if self.buff_rub_price is not None:
            representation += f'Buff cost price: {self.buff_rub_price}₽\n'

        if self.__market_withdraw_price() is not None:
            representation += f'Market withdraw price: {self.__market_withdraw_price()}₽\n'

        if self.profit_rub is not None and self.profit_percent is not None:
            representation += f'Profit: {self.profit_rub}₽ ({self.profit_percent}%)\n\n'

        if self.__buff_url is not None:
            representation += f'Buff url: {self.__buff_url}\n'

        representation += '-' * len(representation.split('\n')[-2])
        return representation

    @property
    def hash_name(self):
        return self.__hash_name

    @property
    def profit_rub(self):
        if self.__market_withdraw_price() is None or self.__buff_price is None:
            return None

        return self.__market_withdraw_price() - self.buff_rub_price

    @property
    def profit_percent(self):
        if self.profit_rub is None or self.buff_rub_price is None:
            return None

        return round(self.profit_rub / self.buff_rub_price, 2) * 100

    @property
    def buff_rub_price(self):
        """
        How much you need to deposit to buff, to afford this item.
        :return: int of rubbles.
        """
        if self.__buff_price is None:
            return None

        return round(self.__buff_price * ItemsAnalyzer.DEPOSIT_RUB_TO_CNY)

    @property
    def rub_to_cny_ratio(self):
        """
        Market price / buff price.
        :return: float of ratio
        """
        if self.__market_price is None or self.__buff_price is None:
            return None

        return round(self.__market_price / self.__buff_price, 2)

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
        :return: [hash_name, buff_price,  buff_rub_price, market_price,rub_to_cny_ratio, profit_rub, profit_percent]
        """
        return [self.__hash_name, self.__buff_price, self.buff_rub_price, self.__market_price,self.rub_to_cny_ratio,
                self.profit_rub, self.profit_percent]

    def __market_withdraw_price(self):
        """
        How much can you get if you offer it at the lowest price.
        :return: int of rubbles.
        """
        if self.__market_price is None:
            return None

        return round(self.__market_price * ItemsAnalyzer.MARKET_WITHDRAW_MODIFIER)
