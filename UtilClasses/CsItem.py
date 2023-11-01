class CsItem:
    def __init__(self, hash_name: str, error: str = None, buff_price: float = None,
                 market_price: float = None, rub_to_cny: float = None):
        self.__hash_name = hash_name
        self.__buff_price = buff_price
        self.__market_price = market_price
        self.__rub_to_cny = rub_to_cny
        self.processing_error = error

    def __repr__(self):
        """
        Packs all properties into multiple lines representation.
        :return: multiple lines string.
        """
        representation = f'{"-"*23}\nCs item representation.\n\n'
        representation += f'Hash name: {self.__hash_name}\n'

        if self.processing_error is not None:
            representation += f'Processing error: {self.processing_error}\n'
        else:
            representation += f'Buff price: {self.__buff_price}¥ ({self.buff_rub_price}₽)\n'
            representation += f'Market price: {self.__market_price}₽\n'
            representation += f'Profit percent: {self.profit_percent}%\n'

        representation += '-' * len(representation.split('\n')[-2])
        return representation

    @property
    def hash_name(self):
        return self.__hash_name

    @property
    def buff_rub_price(self):
        """
        How much you need to deposit to buff, to afford this item.
        :return: int of rubbles.
        """
        if self.__buff_price is None:
            return None

        return round(self.__buff_price * self.__rub_to_cny)

    @property
    def rub_to_cny(self):
        """
        Market price / buff price.
        :return: float of ratio
        """
        if self.__market_price is None or self.__buff_price is None:
            return None

        return round(self.__market_price / self.__buff_price, 2)

    @property
    def profit_percent(self):
        """
        Delta between item rub to cny and deposit rub to cny.
        :return: int - %.
        """
        if self.rub_to_cny is None:
            return None

        return round((self.rub_to_cny / self.__rub_to_cny), 2)

    @property
    def properties_array(self) -> []:
        """
        Packs all properties in array.
        :return: [hash_name, buff_price,  buff_rub_price, market_price, rub_to_cny_ratio, profit_percent]
        """
        return [self.__hash_name, self.__buff_price, self.buff_rub_price, self.__market_price, self.rub_to_cny,
                self.profit_percent]
