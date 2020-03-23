from array import array
from abc import ABC, abstractmethod


class ArrayListIterator(ABC):
    """
        В реализации итератора мы должны отслеживать состояние обхода,
        текущую позицию и количество оставшихся элементов
    """

    def __init__(self, collection):
        self._collection = collection

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def has_more(self):
        pass


class ForwardIterator(ArrayListIterator):
    """ Обыкновенный итератор """

    def __init__(self, collection):
        super().__init__(collection)
        self._current = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self.has_more():
            self._current += 1
            return self._collection[self._current]

        raise StopIteration()

    def has_more(self):
        status = True if self._current < len(self._collection) - 1 \
            else False
        return status


class BackwardIterator(ArrayListIterator):
    """ Итератор в обратную сторону """

    def __init__(self, collection):
        super().__init__(collection)
        self._current = len(self._collection)

    def __iter__(self):
        return self

    def __next__(self):
        if self.has_more():
            self._current -= 1
            return self._collection[self._current]

        raise StopIteration()

    def has_more(self):
        status = True if self._current > 0 \
            else False
        return status


class ArrayList:
    """
    Класс должен реализовывать протокол MutableSequence
    """
    dictionary = {"i": int, "f": float, "u": str}

    def __init__(self, element_type, elmnts=None):
        """
        Список должен быть типизированым
        Внутреннее хранение должно быть реализовано
        на array.array
        """
        self.container = array(element_type) if elmnts is None \
            else array(element_type, elmnts)
        self.type = self.dictionary[element_type]
        self.iterator = ForwardIterator(self.container)

    def __getitem__(self, index):
        return self.container[index]

    def __setitem__(self, key: int, value):
        self.container[key] = value

    def __delitem__(self, key: int):
        del self.container[key]

    def __len__(self):
        return len(self.container)

    def __contains__(self, item):
        if type(item) == self.type:
            for x in self:
                if item == x:
                    return True
        return False

    def __iter__(self):
        return ForwardIterator(self.container)

    def __reversed__(self):
        return BackwardIterator(self.container)

    def index(self, item):
        if type(item) == self.type:
            for idx, x in enumerate(self):
                if x == item:
                    return idx
        return None

    def count(self, item):
        cnt = 0
        if type(item) == self.type:
            for x in self:
                if x == item:
                    cnt += 1
            return cnt
        else:
            return None

    def insert(self, idx, item):
        if type(item) == self.type:
            self.container = array(self.container.typecode,
                                   [*self.container[:idx], item,
                                    *self.container[idx:]])


    def __iadd__(self, other):
        self.container += other.container
        return self

    def remove(self, item):
        """Элемент, который требуется удалить из списка. Если элемент отсутствует
        в списке, возбуждается ValueError"""
        idx = self.index(item)
        if idx is None:
            raise ValueError
        else:
            self.container = self[:idx].__iadd__(self[idx + 1:])

    def pop(self, idx):
        tmp = self.container[idx]
        self.container = self[:idx].__iadd__(self[idx + 1:])
        return tmp

    def reverse(self):
        self.container = self.container[::-1]

    def extend(self, item):
        if type(item[0]) == self.type:
            self.container += item.container

    def append(self, item):
        if type(item) == self.type:
            self.container = array(self.container.typecode,
                                   [*self.container, item])
