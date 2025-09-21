class Address:
    def __init__(self, domain: str, url: str):
        self.__domain = domain
        self.__url = url

    # геттер и сеттер URL
    @property
    def domain(self) -> str:
        return self.__domain
    
    @property
    def url(self) -> str:
        return self.__url

    def to_dict(self) -> dict:
        #Преобразует объект адреса в словарь
        return {
            'domain': self.__domain,
            'url': self.__url
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Address':
        #Создает объект адреса из словаря
        return cls(
            domain=data['domain'],
            url=data['url']
        )