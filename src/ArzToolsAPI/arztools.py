import requests
from typing import Dict, Any

class ArzToolsAPI:
    def __init__(self, phpsessid: str):
        """
        Инициализирует объект API с указанным PHPSESSID для аутентификации.
        
        :param phpsessid: Значение куки PHPSESSID для доступа к API.
        """
        self.base_url = "https://admin.arztools.tech/api/"
        self.headers = {
            "referer": "https://admin.arztools.tech/index.php",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36"
        }
        self.cookies = {
            "PHPSESSID": phpsessid
        }

    def get_admin_list(self) -> Dict[str, Any]:
        """
        Получает список администраторов через API.
        
        :return: Словарь с данными о списке администраторов.
        :raises Exception: Если запрос завершился неудачно или API вернул ошибку.
        """
        return self._make_request("user/adminlist.php")

    def get_detailed_online(self, nick: str, week: str) -> Dict[str, Any]:
        """
        Получает детализированную информацию об онлайне для указанного администратора и недели.
        
        :param nick: Никнейм администратора.
        :param week: Неделя для получения данных (например, 'previous' или 'current').
        :return: Словарь с детализированной информацией об онлайне.
        :raises Exception: Если запрос завершился неудачно или API вернул ошибку.
        """
        params = {"nick": nick, "week": week}
        return self._make_request("onlines/detailed.php", params=params)

    def get_online(self) -> Dict[str, Any]:
        """
        Получает общую информацию об онлайне всех администраторов.
        
        :return: Словарь с данными об онлайне.
        :raises Exception: Если запрос завершился неудачно или API вернул ошибку.
        """
        return self._make_request("onlines/get.php")

    def _make_request(self, endpoint: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Внутренний метод для выполнения GET-запроса к API с обработкой ошибок.
        
        :param endpoint: Конечная точка API (например, 'user/adminlist.php').
        :param params: Параметры запроса (если есть).
        :return: Словарь с данными ответа API.
        :raises Exception: Если произошла ошибка сети, JSON некорректен или API вернул ошибку.
        """
        url = self.base_url + endpoint
        try:
            response = requests.get(url, headers=self.headers, cookies=self.cookies, params=params)
            response.raise_for_status()  # Проверка на HTTP-ошибки (например, 404, 500)
            data = response.json()
            # Проверка на наличие ошибки в ответе API
            if "error" in data and data["error"]:
                raise Exception(data.get("message", "Неизвестная ошибка"))
            elif "code" in data and data["code"] != 200:
                raise Exception(data.get("data", {}).get("answer", "Неизвестная ошибка"))
            return data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка запроса: {e}")
        except ValueError:
            raise Exception("Некорректный JSON в ответе")