class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type,
                 duration, distance,
                 speed, calories) -> str:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    HOURS_IN_M: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (Training.get_distance(self) / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type,
                           duration,
                           distance,
                           speed,
                           calories)


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    M_IN_KM: int = 1000

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        HOURS_IN_M: float = self.duration * 60
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * Running.get_mean_speed(self)
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * HOURS_IN_M)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65
    MULTIPLIER_FOR_WEIGHT_1: float = 0.035
    MULTIPLIER_FOR_WEIGHT_2: float = 0.029
    SPEED_PER_SECOND: float = 0.278
    M_IN_SM: int = 100
    M_IN_HOURS = 60

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        MEAN_SPEED_MC = self.get_mean_speed() * self.SPEED_PER_SECOND
        HEIGHT_IN_M = self.height / self.M_IN_SM
        return ((self.MULTIPLIER_FOR_WEIGHT_1 * self.weight
                 + (MEAN_SPEED_MC**2 / HEIGHT_IN_M)
                 * self.MULTIPLIER_FOR_WEIGHT_2 * self.weight)
                * self.duration * self.M_IN_HOURS)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_MULTIPLIER_1: float = 1.1
    SWIM_MULTIPLIER_2: float = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        spent_calories = (
            (self.get_mean_speed() + self.SWIM_MULTIPLIER_1)
            * self.SWIM_MULTIPLIER_2 * self.weight * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout = {'SWM': Swimming,
               'RUN': Running,
               'WLK': SportsWalking}
    if workout_type in workout:
        return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
