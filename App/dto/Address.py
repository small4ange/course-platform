#--------- класс для хранения адреса платформы (url и домен)
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
