# Ассемблер и интерпретатор для виртуальной машины
 
Этот репозиторий содержит ассемблер и интерпретатор для простой виртуальной машины (VM). Ассемблер переводит текстовый код в машинный, а интерпретатор выполняет машинный код и управляет виртуальной памятью.

## Возможности
Ассемблер: Конвертирует команды в машинный код.

Интерпретатор: Исполняет машинный код с использованием виртуальной памяти.

###Поддерживаемые команды:###
loadc a b: Загружает константу b в аккумулятор.

read a: Читает значение из памяти по адресу в аккумуляторе.

write a b: Записывает значение из аккумулятора в адрес памяти b.

bswap a: Меняет порядок байт в аккумуляторе.
