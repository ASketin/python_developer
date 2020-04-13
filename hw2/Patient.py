from abc import ABC, abstractmethod
from dateutil.parser import parse
import regex as re
import logging

# лучше вместо глобальных констант, создать структуры с интерфейсом
# обновления элементов и форматов
OPERATORS_CODE = {900, 901, 902, 903, 904, 905, 906, 908, 909, 910,
                  911, 912, 913, 914, 915, 916, 917, 918, 919, 920,
                  921, 922, 923, 924, 925, 926, 927, 928, 929, 930,
                  931, 932, 933, 934, 936, 937, 938, 939, 941, 950,
                  951, 952, 953, 954, 955, 956, 958, 960, 961, 962,
                  963, 964, 965, 966, 967, 968, 969, 970, 971, 977,
                  978, 980, 981, 982, 983, 984, 985, 986, 987, 988,
                  989, 991, 992, 993, 994, 995, 996, 997, 999}

DOC_TYPE = {"паспорт"}
INAPROPRIATE_SYMBOLS = r"[a-zA-Z\u0400-\u04FF.!@?#$%&:;*\,\/;\=[\\\]\^_{|}<>]"

logger_info = logging.getLogger("Patient")
logger_info.setLevel(logging.INFO)

handler = logging.FileHandler('status.txt', 'w', 'utf-8')
formatter = logging.Formatter("%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s")
handler.setFormatter(formatter)
logger_info.addHandler(handler)


class BaseDescriptor(ABC):
    """
        Базовый дескриптор реализует запись в
        лог исключений и магический метод set
    """

    def __set_name__(self, owner, name):
        self.name = name
        self.value = None

    def log_except(self):
        pass

    @abstractmethod
    def __get__(self, instance, owner):
        pass

    @abstractmethod
    def __set__(self, instance, value):
        pass


class StringDescriptor(BaseDescriptor):
    """
        Дескриптор данных для first_name, last_name.
        В случае некорректного формата данных выбрасвает
        ошибку ValueError, все ошибки логгируются в exceptions.

        Формат имени предполагает отсутствие цифр и небуквенных
        символов, количество уникальнх символов > 2
    """

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if self.check_name(value):
            if self.name not in instance.__dict__:
                instance.__dict__[self.name] = value
            else:
                raise ValueError("Changes Forbidden")
        else:
            raise ValueError("Incorrect Name/Surname")

    @staticmethod
    def check_name(value):
        if not isinstance(value, str):
            return False
        if len(set(value)) < 2:
            return False
        if not value.isalpha():
            return False
        return True


class DateDescriptor(BaseDescriptor):
    """
       Дата должна иметь тип datetime.
       Принимает входные данные в формате дд.мм.гггг.
       Исключения логгируем в exceptions
    """

    def __set__(self, instance, value):
        if self.check_date(value):
            tmp = parse(value)
            instance.__dict__[self.name] = tmp.date()
            logger_info.info("Date was changed")
        else:
            raise ValueError("input not str type")

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    @staticmethod
    def check_date(value):
        if not isinstance(value, str):
            return False
        return True


class PhoneDescriptor(BaseDescriptor):
    """
        Проверяет значение на соответствие формату.
        Исключения логгируем в exceptions
    """

    def __set__(self, instance, value):
        number, status = self.check_phone(value)
        if status:
            instance.__dict__[self.name] = number
            logger_info.info("Phone was changed")
        else:
            raise ValueError("Invalid number")

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    @staticmethod
    def check_phone(number):

        if not isinstance(number, str):
            return None, False
        parsed_num = re.findall(r"\d+", number)
        res = "8"
        res += ''.join(parsed_num)[1:]
        if len(res) != 11:
            return None, False
        if int(res[1:4]) not in OPERATORS_CODE:
            return None, False
        if re.search(INAPROPRIATE_SYMBOLS, number) is not None:
            return None, False
        return res, True


class DocDescriptor(BaseDescriptor):

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if self.name == "document_id":
            res, status = self.check_id(value)
            if status:
                instance.__dict__[self.name] = res
            else:
                raise ValueError("Invalid ID")
        elif self.name == "document_type":
            if self.check_doc(value):
                instance.__dict__[self.name] = value
            else:
                raise ValueError("Invalid document")

    @staticmethod
    def check_id(number):
        if not isinstance(number, str):
            return None, False
        parsed_num = re.findall(r"\d+", number)
        res = ''.join(parsed_num)
        if len(res) != 10:
            return None, False
        if re.search(INAPROPRIATE_SYMBOLS, number) is not None:
            return None, False
        return res, True

    @staticmethod
    def check_doc(doc_type):
        if not isinstance(doc_type, str):
            return False
        if str.lower(doc_type) not in DOC_TYPE:
            return False
        return True


class Patient:
    """
        Объект хранит информацию о пациенте
        : имя(string) - должно состоять из букв
        : фамилия(string) - должно состоять из букв
        : дата рождения(string) - будем хранить в формате
            dd.mm.yyyy
        : номер телефона(string) - соответствие формату,хранение в
            виде 8xxxxxxxxxxx
        : тип документа(string) - ограниченный набор(паспорт,
            удостоверения, прочее), надо реализовать метод
            добавления нового документа карантинного пропуска к
            примеру
        : номер документа(string) - проверять на соответствие
            номера формату документа

        Создание, изменние, сохранение объекта записываем
            в лог changes
        Исключения, случившиеся при работе,
            в лог exceptions

        Хранить пациента нужно в csv, у класса
        есть метод save для дозаписи в файл
    """
    first_name = StringDescriptor()
    last_name = StringDescriptor()
    birth_date = DateDescriptor()
    phone = PhoneDescriptor()
    document_type = DocDescriptor()
    document_id = DocDescriptor()

    def __init__(self, first_name: str, last_name: str,
                 birth_date: str, phone: str, document_type: str,
                 document_id):
        logger_info.info("Patient was written")
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.phone = phone
        self.document_type = document_type
        self.document_id = document_id


    @classmethod
    def create(cls, first_name, last_name, birth_date, phone,
               document_type, document_id):
        logger_info.info("Patient was created")
        return cls(first_name, last_name, birth_date, phone,
                   document_type, document_id)

    def save(self):
        pass


class PatientCollection:
    pass
