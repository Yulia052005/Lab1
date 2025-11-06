import json
import xml.etree.ElementTree as ET


class TransportError(Exception):
    """Базовое исключение для транспортной системы"""
    pass


class CapacityExceededError(TransportError):
    """Превышена вместимость транспорта"""
    pass


class PassengerNotFoundError(TransportError):
    """Пассажир не найден"""
    pass


class InvalidDataError(TransportError):
    """Неверные данные"""
    pass


class FileOperationError(TransportError):
    """Ошибка работы с файлом"""
    pass


class DuplicateIdError(TransportError):
    """Объект с таким ID уже существует в системе"""
    pass


class EmptySystemError(TransportError):
    """Операция невозможна - система пуста"""
    pass


class RouteConflictError(TransportError):
    """Конфликт маршрутов - транспорт уже назначен на другой маршрут"""
    pass


class Transport:
    def __init__(self, transport_id, name, capacity):
        # Проверка входных данных
        if capacity <= 0:
            raise InvalidDataError("Вместимость должна быть больше нуля")
        if not name:
            raise InvalidDataError("Название транспорта не может быть пустым")
        if transport_id <= 0:
            raise InvalidDataError("ID транспорта должен быть юольше нуля")

        self.id = transport_id
        self.name = name
        self.capacity = capacity
        self.route = None
        self.passengers = []

    def add_passenger(self, passenger):
        try:
            if passenger is None:
                raise InvalidDataError("Пассажир не может быть пустым")

            if len(self.passengers) >= self.capacity:
                raise CapacityExceededError(
                    f"Нет свободных мест в {self.name}! Вместимость: {self.capacity}"
                )

            self.passengers.append(passenger)
            print(f"Пассажир {passenger.name} добавлен в {self.name}")
            return True

        except CapacityExceededError as e:
            print(f"Ошибка: {e}")
            return False
        except InvalidDataError as e:
            print(f"Ошибка: {e}")
            return False

    def remove_passenger(self, passenger):
        try:
            if passenger is None:
                raise InvalidDataError("Пассажир не может быть пустым")

            if passenger in self.passengers:
                self.passengers.remove(passenger)
                print(f"Пассажир {passenger.name} удален из {self.name}")
                return True
            else:
                raise PassengerNotFoundError(
                    f"Пассажир {passenger.name} не найден в {self.name}"
                )

        except (PassengerNotFoundError, InvalidDataError) as e:
            print(f"Ошибка: {e}")
            return False
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return False

    def __str__(self):
        return f"{self.name} (ID: {self.id}, мест: {self.capacity})"


class Bus(Transport):
    def __init__(self, transport_id, name, capacity, bus_number):
        super().__init__(transport_id, name, capacity)
        if not bus_number:
            raise InvalidDataError("Номер автобуса не может быть пустым")
        self.bus_number = bus_number
        self.type = "bus"

    def __str__(self):
        return f"Автобус {self.bus_number} - {self.name}"


class Tram(Transport):
    def __init__(self, transport_id, name, capacity, line_number):
        super().__init__(transport_id, name, capacity)
        if not line_number:
            raise InvalidDataError("Номер линии трамвая не может быть пустым")
        self.line_number = line_number
        self.type = "tram"

    def __str__(self):
        return f"Трамвай {self.line_number} - {self.name}"


class Train(Transport):
    def __init__(self, transport_id, name, capacity, carriages):
        super().__init__(transport_id, name, capacity)
        if carriages <= 0:
            raise InvalidDataError("Количество вагонов должно быть положительным")
        self.carriages = carriages
        self.type = "train"

    def __str__(self):
        return f"Поезд ({self.carriages} вагонов) - {self.name}"


class Passenger:
    def __init__(self, passenger_id, name, ticket_number):
        if passenger_id <= 0:
            raise InvalidDataError("ID пассажира должен быть положительным")
        if not name:
            raise InvalidDataError("Имя пассажира не может быть пустым")
        if not ticket_number:
            raise InvalidDataError("Номер билета не может быть пустым")

        self.id = passenger_id
        self.name = name
        self.ticket_number = ticket_number

    def __str__(self):
        return f"Пассажир {self.name} (билет: {self.ticket_number})"


class Route:
    def __init__(self, route_id, start_point, end_point):
        if route_id <= 0:
            raise InvalidDataError("ID маршрута должен быть положительным")
        if not start_point or not end_point:
            raise InvalidDataError("Начальная и конечная точки маршрута не могут быть пустыми")

        self.id = route_id
        self.start_point = start_point
        self.end_point = end_point

    def __str__(self):
        return f"Маршрут {self.id}: {self.start_point} -> {self.end_point}"


class TransportSystem:
    def __init__(self):
        self.transports = []
        self.passengers = []
        self.routes = []

    def add_transport(self, transport):
        try:
            if transport is None:
                raise InvalidDataError("Транспорт не может быть пустым")
            self.transports.append(transport)
            print(f"Добавлен транспорт: {transport}")
        except InvalidDataError as e:
            print(f"Ошибка: {e}")

    def add_passenger(self, passenger):
        try:
            if passenger is None:
                raise InvalidDataError("Пассажир не может быть пустым")
            self.passengers.append(passenger)
            print(f"Добавлен пассажир: {passenger}")
        except InvalidDataError as e:
            print(f"Ошибка: {e}")

    def add_route(self, route):
        try:
            if route is None:
                raise InvalidDataError("Маршрут не может быть пустым")
            self.routes.append(route)
            print(f"Добавлен маршрут: {route}")
        except InvalidDataError as e:
            print(f"Ошибка: {e}")

    def assign_route_to_transport(self, transport_id, route_id):
        try:
            transport = self.find_transport(transport_id)
            route = self.find_route(route_id)

            if transport is None:
                raise PassengerNotFoundError(f"Транспорт с ID {transport_id} не найден")
            if route is None:
                raise PassengerNotFoundError(f"Маршрут с ID {route_id} не найден")

            transport.route = route
            print(f"Маршрут {route} назначен транспорту {transport.name}")

        except PassengerNotFoundError as e:
            print(f"Ошибка: {e}")

    def find_transport(self, transport_id):
        for transport in self.transports:
            if transport.id == transport_id:
                return transport
        return None

    def find_passenger(self, passenger_id):
        for passenger in self.passengers:
            if passenger.id == passenger_id:
                return passenger
        return None

    def find_route(self, route_id):
        for route in self.routes:
            if route.id == route_id:
                return route
        return None

    def show_system_info(self):
        """Показывает всю информацию о системе на экране"""
        print("\n" + "=" * 50)
        print(" ИНФОРМАЦИЯ О ТРАНСПОРТНОЙ СИСТЕМЕ")
        print("=" * 50)

        print(f"\nОБЩАЯ СТАТИСТИКА:")
        print(f" Транспортных средств: {len(self.transports)}")
        print(f" Пассажиров: {len(self.passengers)}")
        print(f" Маршрутов: {len(self.routes)}")

        print(f"\nМАРШРУТЫ:")
        for route in self.routes:
            print(f" {route}")

        print(f"\nТРАНСПОРТ:")
        for transport in self.transports:
            route_info = f" на маршруте {transport.route}" if transport.route else " (без маршрута)"
            passengers_info = f", пассажиров: {len(transport.passengers)}"
            print(f" {transport}{route_info}{passengers_info}")

            # Показываем пассажиров в каждом транспорте
            if transport.passengers:
                for passenger in transport.passengers:
                    print(f"   - {passenger.name}")

        print(f"\nПАССАЖИРЫ:")
        for passenger in self.passengers:
            # Находим в каком транспорте пассажир
            in_transport = None
            for transport in self.transports:
                if passenger in transport.passengers:
                    in_transport = transport.name
                    break
            transport_info = f" в {in_transport}" if in_transport else " (ждет транспорта)"
            print(f" {passenger.name}{transport_info}")

    def save_to_json(self, filename):
        """Сохранение в JSON по разработанной структуре"""
        try:
            if not filename:
                raise InvalidDataError("Имя файла не может быть пустым")

            data = {
                "transport_system": {
                    "transports": [
                        {
                            "id": t.id,
                            "type": getattr(t, 'type', 'transport'),
                            "name": t.name,
                            "capacity": t.capacity,
                            "bus_number": getattr(t, 'bus_number', None),
                            "line_number": getattr(t, 'line_number', None),
                            "carriages": getattr(t, 'carriages', None),
                            "route_id": t.route.id if t.route else None,
                            "passengers": [p.id for p in t.passengers]
                        }
                        for t in self.transports
                    ],
                    "passengers": [
                        {
                            "id": p.id,
                            "name": p.name,
                            "ticket_number": p.ticket_number
                        }
                        for p in self.passengers
                    ],
                    "routes": [
                        {
                            "id": r.id,
                            "start_point": r.start_point,
                            "end_point": r.end_point
                        }
                        for r in self.routes
                    ]
                }
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Данные сохранены в JSON: {filename}")

        except InvalidDataError as e:
            print(f"Ошибка данных: {e}")
        except IOError as e:
            print(f"Ошибка ввода-вывода: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при сохранении JSON: {e}")

    def load_from_json(self, filename):
        """Чтение из JSON файла по разработанной структуре"""
        try:
            if not filename:
                raise InvalidDataError("Имя файла не может быть пустым")

            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Чтение данных из JSON: {filename}")

            # Очищаем текущие данные
            self.transports.clear()
            self.passengers.clear()
            self.routes.clear()

            # Загружаем маршруты
            for route_data in data["transport_system"]["routes"]:
                route = Route(
                    route_data["id"],
                    route_data["start_point"],
                    route_data["end_point"]
                )
                self.routes.append(route)
                print(f" Загружен маршрут: {route}")

            # Загружаем пассажиров
            for passenger_data in data["transport_system"]["passengers"]:
                passenger = Passenger(
                    passenger_data["id"],
                    passenger_data["name"],
                    passenger_data["ticket_number"]
                )
                self.passengers.append(passenger)
                print(f" Загружен пассажир: {passenger}")

            # Загружаем транспорт
            for transport_data in data["transport_system"]["transports"]:
                transport_type = transport_data["type"]

                if transport_type == "bus":
                    transport = Bus(
                        transport_data["id"],
                        transport_data["name"],
                        transport_data["capacity"],
                        transport_data["bus_number"]
                    )
                elif transport_type == "tram":
                    transport = Tram(
                        transport_data["id"],
                        transport_data["name"],
                        transport_data["capacity"],
                        transport_data["line_number"]
                    )
                elif transport_type == "train":
                    transport = Train(
                        transport_data["id"],
                        transport_data["name"],
                        transport_data["capacity"],
                        transport_data["carriages"]
                    )
                else:
                    transport = Transport(
                        transport_data["id"],
                        transport_data["name"],
                        transport_data["capacity"]
                    )

                # Восстанавливаем связь с маршрутом
                if transport_data["route_id"]:
                    route = self.find_route(transport_data["route_id"])
                    if route:
                        transport.route = route

                # Восстанавливаем связь с пассажирами
                for passenger_id in transport_data["passengers"]:
                    passenger = self.find_passenger(passenger_id)
                    if passenger:
                        transport.passengers.append(passenger)

                self.transports.append(transport)
                print(f" Загружен транспорт: {transport}")

            print("Все данные успешно загружены из JSON!")

        except FileNotFoundError:
            print(f"Файл {filename} не найден")
        except json.JSONDecodeError:
            print(f"Ошибка формата JSON в файле {filename}")
        except InvalidDataError as e:
            print(f"Ошибка данных: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при загрузке JSON: {e}")

    def save_to_xml(self, filename):
        """Сохранение в XML по разработанной структуре"""
        try:
            if not filename:
                raise InvalidDataError("Имя файла не может быть пустым")

            root = ET.Element("transport_system")

            # Транспорт
            transports_elem = ET.SubElement(root, "transports")
            for transport in self.transports:
                transport_elem = ET.SubElement(transports_elem, "transport")
                ET.SubElement(transport_elem, "id").text = str(transport.id)
                ET.SubElement(transport_elem, "type").text = getattr(transport, 'type', 'transport')
                ET.SubElement(transport_elem, "name").text = transport.name
                ET.SubElement(transport_elem, "capacity").text = str(transport.capacity)

                if hasattr(transport, 'bus_number'):
                    ET.SubElement(transport_elem, "bus_number").text = transport.bus_number
                if hasattr(transport, 'line_number'):
                    ET.SubElement(transport_elem, "line_number").text = transport.line_number
                if hasattr(transport, 'carriages'):
                    ET.SubElement(transport_elem, "carriages").text = str(transport.carriages)

                ET.SubElement(transport_elem, "route_id").text = str(transport.route.id) if transport.route else ""

                passengers_elem = ET.SubElement(transport_elem, "passengers")
                for passenger in transport.passengers:
                    ET.SubElement(passengers_elem, "passenger_id").text = str(passenger.id)

            # Пассажиры
            passengers_elem = ET.SubElement(root, "passengers")
            for passenger in self.passengers:
                passenger_elem = ET.SubElement(passengers_elem, "passenger")
                ET.SubElement(passenger_elem, "id").text = str(passenger.id)
                ET.SubElement(passenger_elem, "name").text = passenger.name
                ET.SubElement(passenger_elem, "ticket_number").text = passenger.ticket_number

            # Маршруты
            routes_elem = ET.SubElement(root, "routes")
            for route in self.routes:
                route_elem = ET.SubElement(routes_elem, "route")
                ET.SubElement(route_elem, "id").text = str(route.id)
                ET.SubElement(route_elem, "start_point").text = route.start_point
                ET.SubElement(route_elem, "end_point").text = route.end_point

            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)
            print(f"Данные сохранены в XML: {filename}")

        except InvalidDataError as e:
            print(f"Ошибка данных: {e}")
        except IOError as e:
            print(f"Ошибка ввода-вывода: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при сохранении XML: {e}")

    def load_from_xml(self, filename):
        """Чтение из XML файла по разработанной структуре"""
        try:
            if not filename:
                raise InvalidDataError("Имя файла не может быть пустым")

            tree = ET.parse(filename)
            root = tree.getroot()
            print(f"Чтение данных из XML: {filename}")

            # Очищаем текущие данные
            self.transports.clear()
            self.passengers.clear()
            self.routes.clear()

            # Загружаем маршруты
            for route_elem in root.find("routes"):
                route = Route(
                    int(route_elem.find("id").text),
                    route_elem.find("start_point").text,
                    route_elem.find("end_point").text
                )
                self.routes.append(route)
                print(f" Загружен маршрут: {route}")

            # Загружаем пассажиров
            for passenger_elem in root.find("passengers"):
                passenger = Passenger(
                    int(passenger_elem.find("id").text),
                    passenger_elem.find("name").text,
                    passenger_elem.find("ticket_number").text
                )
                self.passengers.append(passenger)
                print(f" Загружен пассажир: {passenger}")

            # Загружаем транспорт
            for transport_elem in root.find("transports"):
                transport_type = transport_elem.find("type").text
                transport_id = int(transport_elem.find("id").text)
                name = transport_elem.find("name").text
                capacity = int(transport_elem.find("capacity").text)

                if transport_type == "bus":
                    bus_number = transport_elem.find("bus_number").text
                    transport = Bus(transport_id, name, capacity, bus_number)
                elif transport_type == "tram":
                    line_number = transport_elem.find("line_number").text
                    transport = Tram(transport_id, name, capacity, line_number)
                elif transport_type == "train":
                    carriages = int(transport_elem.find("carriages").text)
                    transport = Train(transport_id, name, capacity, carriages)
                else:
                    transport = Transport(transport_id, name, capacity)

                # Восстанавливаем связь с маршрутом
                route_id_elem = transport_elem.find("route_id")
                if route_id_elem is not None and route_id_elem.text:
                    route = self.find_route(int(route_id_elem.text))
                    if route:
                        transport.route = route

                # Восстанавливаем связь с пассажирами
                passengers_elem = transport_elem.find("passengers")
                if passengers_elem is not None:
                    for passenger_id_elem in passengers_elem.findall("passenger_id"):
                        passenger = self.find_passenger(int(passenger_id_elem.text))
                        if passenger:
                            transport.passengers.append(passenger)

                self.transports.append(transport)
                print(f" Загружен транспорт: {transport}")

            print("Все данные успешно загружены из XML!")

        except FileNotFoundError:
            print(f"Файл {filename} не найден")
        except ET.ParseError:
            print(f"Ошибка формата XML в файле {filename}")
        except InvalidDataError as e:
            print(f"Ошибка данных: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при загрузке XML: {e}")


def main():
    print("ЗАПУСК ТРАНСПОРТНОЙ СИСТЕМЫ")
    print("=" * 40)

    system = TransportSystem()

    # Создаем тестовые данные
    print("\nСОЗДАЕМ ТЕСТОВЫЕ ДАННЫЕ:")

    try:
        route1 = Route(1, "Метро", "Общежитие")
        route2 = Route(2, "Университет", "Театр")

        bus = Bus(1, "Автобус №79", 2, "А79")  # Маленькая вместимость для демонстрации ошибок
        bus.route = route1

        tram = Tram(2, "Трамвай №1", 90, "1")
        tram.route = route2

        train = Train(3, "Электричка", 500, 5)

        passenger1 = Passenger(1, "Сергей Иванов", "M001")
        passenger2 = Passenger(2, "Мария Васильева", "M002")
        passenger3 = Passenger(3, "Ольга Петрова", "M003")
        passenger4 = Passenger(4, "Любовь Иванова", "M004")

        system.add_transport(bus)
        system.add_transport(tram)
        system.add_transport(train)
        system.add_passenger(passenger1)
        system.add_passenger(passenger2)
        system.add_passenger(passenger3)
        system.add_passenger(passenger4)
        system.add_route(route1)
        system.add_route(route2)

        # Демонстрация работы с исключениями
        print("\nДЕМОНСТРАЦИЯ ОБРАБОТКИ ОШИБОК:")

        # Попытка добавить пассажира в переполненный автобус
        print("\n1. Попытка переполнить автобус:")
        bus.add_passenger(passenger1)
        bus.add_passenger(passenger2)
        bus.add_passenger(passenger3)  # Должна быть ошибка!

        # Попытка удалить несуществующего пассажира
        print("\n2. Попытка удалить несуществующего пассажира:")
        bus.remove_passenger(passenger4)

        # Сажаем пассажиров в транспорт
        print("\n3. Корректная посадка пассажиров:")
        bus.add_passenger(passenger1)
        bus.add_passenger(passenger2)
        tram.add_passenger(passenger3)
        train.add_passenger(passenger4)

        # Показываем созданные данные
        system.show_system_info()

        # Сохраняем в оба формата (создаем файлы)
        print("\nСОХРАНЕНИЕ ДАННЫХ:")
        system.save_to_json("transport_data.json")
        system.save_to_xml("transport_data.xml")

        # Демонстрируем чтение (теперь файлы существуют!)
        print("\nДЕМОНСТРАЦИЯ ЧТЕНИЯ:")

        # Создаем новую пустую систему
        new_system = TransportSystem()

        # Читаем из JSON (файл уже создан выше)
        print("\n--- Чтение из JSON ---")
        new_system.load_from_json("transport_data.json")
        new_system.show_system_info()

        # Создаем еще одну пустую систему
        another_system = TransportSystem()

        # Читаем из XML (файл уже создан выше)
        print("\n--- Чтение из XML ---")
        another_system.load_from_xml("transport_data.xml")
        another_system.show_system_info()

    except Exception as e:
        print(f"Критическая ошибка в основном потоке: {e}")


if __name__ == "__main__":
    main()

