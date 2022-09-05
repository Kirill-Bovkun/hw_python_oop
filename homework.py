
class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вывести информацию о тренировке."""

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # Расстояние, которое спортсмен преодолевает за один шаг.
    M_IN_KM = 1000  # Константа для перевода значений из метров в километры.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action  # Кол-во совершённых действий
        #  (число шагов при ходьбе и беге либо гребков — при плавании).
        self.duration = duration  # Длительность тренировки в часах.
        self.weight = weight  # Вес спортсмена.

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""

        run_cc_1 = 18  # Коэффициент для подсчёта каллорий №1.
        run_cc_2 = 20  # Коэффициент для подсчёта каллорий №2.
        v = self.get_mean_speed()  # Средняя скорость.
        w = self.weight  # Вес спортсмена.
        t = self.duration * 60  # Время тренировки в минутах.
        return ((run_cc_1 * v - run_cc_2) * w / self.M_IN_KM * t)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""

        sp_wlk_cc_1 = 0.035  # Коэффициент для подсчёта каллорий №3.
        sp_wlk_cc_2 = 2  # Коэффициент для подсчёта каллорий №4.
        sp_wlk_cc_3 = 0.029  # Коэффициент для подсчёта каллорий №5.
        v = self.get_mean_speed()  # Средняя скорость.
        w = self.weight  # Вес спортсмена.
        t = self.duration * 60  # Время тренировки в минутах.
        h = self.height  # Рост спортсмена.
        return ((sp_wlk_cc_1 * w + (v**sp_wlk_cc_2 // h) * sp_wlk_cc_3 * w) * t
                )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    # Расстояние, которое спортсмен преодолевает за один гребок.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в бассейне."""

        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""

        swm_cc_1 = 1.1  # Коэффициент для подсчёта каллорий №6.
        swm_cc_2 = 2  # Коэффициент для подсчёта каллорий №7.
        w = self.weight  # Вес спортсмена.
        v = self.get_mean_speed()  # Средняя скорость спортсмена.
        return ((v + swm_cc_1) * swm_cc_2 * w)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_type: dict = {
                            'SWM': Swimming,
                            'RUN': Running,
                            'WLK': SportsWalking
                          }
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
