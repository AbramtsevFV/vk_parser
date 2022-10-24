### Vk parser
 1. Для запуска нужно указать token в файле, 'creds/tokens.py'
2.  Получить token можно согласно [инструкции](https://dev.vk.com/api/getting-started)
- Пример GET запроса для получения token, где id это id приложения
```
https://oauth.vk.com/authorize?client_id={id}4&redirect_uri=https://oauth.vk.com/blank.html&response_type=token
```