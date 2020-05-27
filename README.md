## Скрипт для предобработки текстовых датасетов
Приводит датасет в файл вида
```
Заголовок 1|Текст 1
Заголовок 2|Текст 2
и т.д.
```
И чистит от мусора

### Поддерживает:
- большинство источников c [Taiga Сorpus](https://tatianashavrina.github.io/taiga_site/)
- [Lenta dataset](https://github.com/yutkin/Lenta.Ru-News-Dataset)
- Парсинг https://meduza.io/
- Парсинг https://habr.com/

### Не поддеривает
- [Rossiya Segodnya](https://github.com/RossiyaSegodnya/ria_news_dataset)

## Использование
1) Поместить датасет в папку source_data
2) возможно переименовать newmetadata.csv в metatable.csv
3) Запустить `python preprocess.py -d dataset_name` 

### Список dataset_name
- habr
- meduza
- lenta2 для [Lenta dataset](https://github.com/yutkin/Lenta.Ru-News-Dataset)
- proza для [Taiga Сorpus](https://tatianashavrina.github.io/taiga_site/)
- fontanka
- arzamas
- interfax
- kp
- Lenta
- nplus1

## Разделить датасет на несколько частей
1) Откройте и отредактируйте split.py
2) Запустите `python split.py`
