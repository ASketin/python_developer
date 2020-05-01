from hw2.homework.config import PHONE_FORMAT, DRIVER_LICENSE_TYPE, DRIVER_LICENSE_FORMAT, PASSPORT_TYPE

GOOD_PARAMS = ("Кондрат", "Коловрат", "1978-01-31", PHONE_FORMAT, DRIVER_LICENSE_TYPE, DRIVER_LICENSE_FORMAT)
OTHER_GOOD_PARAMS = ("Нурсултан", "Назарбаев", "1900-01-01", "+7-916-111-11-11", PASSPORT_TYPE, "1111 111111")
WRONG_PARAMS = ("098098", "56876576558", "ABCDEF", "sdfsdfsdf", "sdfsdfsdfs", "sdflsdfiuh")
PATIENT_FIELDS = ("first_name", "last_name", "birth_date", "phone", "document_type", "document_id")