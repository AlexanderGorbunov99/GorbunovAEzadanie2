# GorbunovAEzadanie2
# 1. ФИО + группа
Горбунов Александр Евгеньевич, группа АСУбз-21-1
# 2. Краткое описание проекта
Необходимо сделать систему распознавания штрих кодов, с помощью библиотеки видеообработки opencv. Для захвата изображения будем использовать Ваш смартфон, который необходимо будет по wi-fi подключить к ПК, и организовать трансляцию по rtsp потоку, сделать это (для примера) можно с помощью Free Security Camera. https://zapishemvse.ru/free-security-camera-prilozhenie-dlja-videonabljudenija-rukovodstvo-skachat/
Далее передаем поток на ПК, проверяем его захват. https://lindevs.com/capture-rtsp-stream-from-ip-camera-using-opencv
Далее можно воспользоваться библиотекой для чтения штрих кодов https://opencv.org/recognizing-one-dimensional-barcode-using-opencv/, также возможно потребуется определение области, в которой находится штрих код. https://habr.com/ru/company/enterra/blog/244163/
После прочтения штрих кода, необходимо будет через сайт https://barcode-list.ru/barcode/RU/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA.htm?barcode=6921734941299, определить товар.
# Используемые технологии
**Язык программирования:** Python 3.13
