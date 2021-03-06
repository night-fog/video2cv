# VIDEO2CV  
  
## Trello по задачам:  
https://trello.com/b/tQVCnvNn  
  
## Цель проекта:  
Создать модульный компонент, позволяющий легко добавить интерактива
в музыкальные перфомансы.  
### Пример использования:  
Перед камерой висит монохромный предмет сложной формы и вращается
по-горизонтали вокруг своей оси. Программе задается диапазон цвета.  
Каждый кадр анализируется, высчитывается процентное наличие заданного цвета
пикселей в кадре. Результат помножается на нужный коэффициент и лимитируется,
если необходимо и преобразуется в управляющий сигнал
(в текущей реализации это MIDI).  
  
## Функционал:  
### Модуль анализа видеопотока:  
* задавать цвет для фильтра кадра  
* получать кадры с камеры  
* получать процентное соотношение пикселей, попадающих под фильтр в кадре  
  
### Модуль передачи управляющего сигнала:  
* Получать число из модуля анализа видеопотока  
* Помножать его на коэффициент и лимитировать по минимальным-максимальным границам  
* Передавать управляющий сигнал  
  
### Примеры использования:  
В конце main.py есть бесконечный цикл, в котором и происходит все вычисление.  
В данный момент есть два варианта развития событий:  
* Отправить MIDI-ноту:  
```midi_out.send_midi_note(vid.count_pixels(), 127)```, где второй параметр
метода send_midi_note задает значение velocity ноты int [0, 127].  
* Отправить управляющий MIDI-сигнал:  
```midi_out.send_midi_cc(vid.count_pixels())```  
