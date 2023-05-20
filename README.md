# Генератор простых чисел
Генератор простых чисел для курсовой работы за 4 курс

Основа: теорема Диемитко

Автор: Чиркин Александр, КБ-401

## Запуск
```bash
./app.sh
```
Генератор запсукается на порте 8000

## Доступные эндпоинты
* */* (перенаправляет на */generator*) - открывает статистику генератора:
  * сколько он выпустил серификатов
  * последний сертификат
  * наибольшее сертифицированное число
  * сколько чисел было сертифицировано при помощи a, не равного 2
* */generator/list* - формирует файл со всеми сертификатами (может занять много времени)
* */generator/check* - проверить число на простоту