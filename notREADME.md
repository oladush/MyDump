# MyDump
Зашифрованное облачное(в необозримом будущем) хранилище паролей. Врядли кто-то это будет читать, это даже хорошо... Нынешняя программа всего лишь тест. Отсутствует  процедура регистрации, нет общего сервера(может работать внутри локальной сети), не очень оптимизированная работа с БД(в силу особенностей JSON и специфики приложения). Это приложение вторично - у него наверняка есть множество как корпоративных, так и опенсорсных аналагов. Но маленький жирный плюсик, конечно же, есть. Вы можете развернуть свое собственное криптографически защищенное приложение на своем же сервере, стать настоящим бунтарем, почувствовать себя независимым, бросить вызов корпорациям. Ну или просто потыкать в удобное(мне оно кажется удобным) консольное приложение. Так же, если каким-то чудом вы наткнулись на это приложение и захотите помочь, ткнуть мой нос в отвратитеольные методы и проектировку которая вызывает много вопросов, вы всегда можете написать мне на почту, я буду очень признателен.    

Но если вас не останавливат все вышесказанное, вы храбрый человек с мазохистскими наклонностями, вам может помочь следующая информация:
1) перед использованием приложения нужно установить следующие зависимости: pyaes, rsa.
2) Сгенерировать себе пару RSA ключей(это можно сделать с помощью библиотеки rsa).

3) Придумать логин и пароль, добавить в server.client_info пользователя с вашим логином.
4) Сгененрировать с помощью хеш-функции RSA-512, хеш, будет не лишним его "посолить", добавить к вашему пользователю соль, хеш и публичный RSA ключ.
5) Если вы преодолели предыдущий шаг - вы восхитительны, если нет вы тоже молодцы, в скором времени процедура регистрации станет проще.
6) Запустить сервер, если все запустилось - вы точно восхитительны. 
7) Теперь внутри своей локальной сети вы можете хранить пароли.
