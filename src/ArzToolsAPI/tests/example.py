from ..arztools import ArzToolsAPI

def main():
    # Замените 'your_phpsessid_here' на ваш реальный PHPSESSID
    api = ArzToolsAPI('your_phpsessid_here')

    try:
        # Получение списка администраторов
        admin_list = api.get_admin_list()
        print(f"Количество администраторов: {len(admin_list['admins'])}")
        print("Первые 5 администраторов:")
        for admin in admin_list['admins'][:5]:
            print(f"Ник: {admin['nick']}, Уровень: {admin['lvl']}, Должность: {admin['post']}")

        # Получение детализированного онлайна
        detailed_online = api.get_detailed_online('Nicolas_Reed', 'previous')
        print(f"\nДетализированный онлайн для {detailed_online['data']['nick']}:")
        for day in detailed_online['data']['info']:
            print(f"{day['date']} ({day['weekday']}): {day['online']} секунд онлайн")

        # Получение общей информации об онлайне
        online = api.get_online()
        print(f"\nКоличество записей в общем онлайне: {len(online['data']['rows'])}")
        print("Первые 5 записей:")
        for row in online['data']['rows'][:5]:
            print(f"Ник: {row['nick']}, Должность: {row['post']}, Онлайн за прошлую неделю: {row['previous_week']['online']} секунд")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()