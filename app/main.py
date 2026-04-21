from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self._length = 8
        self._used = 0
        self._table = [None for _ in range(8)]

    def _resize_table(self) -> None:
        temp = [item for item in self._table if item]

        self._length *= 2
        self._table = [None for _ in range(self._length)]
        self._used = 0

        for item in temp:
            key, value = item["key"], item["value"]
            self.__setitem__(key, value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._used >= self._length * 2 // 3:
            self._resize_table()

        key_hash = hash(key)
        key_index = key_hash % self._length

        while self._table[key_index] is not None:
            if self._table[key_index]["key"] == key:
                self._table[key_index]["value"] = value
                return
            key_index = (key_index + 1) % self._length

        self._table[key_index] = {
            "key": key,
            "hash": key_hash,
            "value": value
        }
        self._used += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        key_index = key_hash % self._length

        temp = key_index
        while self._table[key_index] is not None:
            if self._table[key_index]["key"] == key:
                return self._table[key_index]["value"]

            key_index = (key_index + 1) % self._length

            if key_index == temp:
                break
        raise KeyError

    def __len__(self) -> int:
        return self._used

    def __str__(self) -> str:
        dict_str = "{" + ", ".join(
            f"{item['key']}: {item['value']}"
            for item in self._table
            if item
        ) + "}"
        return f"{self.__class__.__name__} {dict_str}"

    def __repr__(self) -> str:
        return self.__str__()
