from random import gauss


class Time:
    def __init__(self, hours=0, minutes=0, seconds=0.0, milliseconds=0):
        self.mil_time = int(((((hours * 60) + minutes) * 60) + seconds) * 1000 + milliseconds)

    def __str__(self):
        if self.mil_time >= 0:
            hour = self.mil_time // (60 * 60 * 1000)
            minute = (self.mil_time % (60 * 60 * 1000)) // (60 * 1000)
            second = (self.mil_time % (60 * 1000)) // 1000
            millisecond = self.mil_time % 1000
            return f"{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}." \
                f"{str(millisecond).zfill(3)}"

        else:
            absolute_mil_time = -1 * self.mil_time
            hour = absolute_mil_time // (60 * 60 * 1000)
            minute = (absolute_mil_time % (60 * 60 * 1000)) // (60 * 1000)
            second = (absolute_mil_time % (60 * 1000)) // 1000
            millisecond = absolute_mil_time % 1000
            return f"-{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}." \
                   f"{str(millisecond).zfill(3)}"

    def __mul__(self, multiplier):
        temp_time = self.mil_time * multiplier
        return Time(milliseconds=temp_time)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, divider):
        if isinstance(divider, (int, float)):
            return Time(milliseconds=int(self.mil_time / divider))
        else:
            # temp_time = self.mil_time / divider.mil_time
            return self.mil_time / divider.mil_time

    def __add__(self, other):
        temp_time = self.mil_time + other.mil_time
        return Time(milliseconds=temp_time)

    def __sub__(self, other):
        temp_time = self.mil_time - other.mil_time
        return Time(milliseconds=temp_time)

    def __eq__(self, other):
        return self.mil_time == other.mil_time

    def __lt__(self, other):
        return self.mil_time < other.mil_time

    def __gt__(self, other):
        return self.mil_time > other.mil_time

    def show_time(self):
        print(self.__str__())

    def in_seconds(self):
        return self.mil_time / 1000


class RaceParameters:
    def __init__(self, race_length: Time, out_lap_time_loss: Time, in_lap_time_loss: Time,
                 lower_class_cars: int, avg_overtake_time_loss: Time):
        """
        Class holding parameters necessary for race simulation dependent on circuit.
        :param race_length: time length of race
        :param out_lap_time_loss: loss of time at out lap
        :param in_lap_time_loss:
        :param lower_class_cars:
        :param avg_overtake_time_loss:
        """
        self.remaining_time = race_length
        self.out_lap_time_loss = out_lap_time_loss
        self.in_lap_time_loss = in_lap_time_loss
        self.lower_class_cars = lower_class_cars
        self.avg_overtake_time_loss = avg_overtake_time_loss

    def update_remaining_time(self, last_lap_time: Time) -> None:
        self.remaining_time -= last_lap_time

    def get_remaining_time(self) -> Time:
        return self.remaining_time


class QuadraticEquation:
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def __call__(self, value: float) -> float:
        return self.get_value(value)

    def get_value(self, variable: float) -> float:
        return self.a * (variable**2) + self.b * variable + self.c


class CarParameters:
    def __init__(self, fuel_capacity: float, refueling_speed: float, fuel_consumption: float, fuel_adj: Time,
                 tyre_change_time: Time, tyre_degradation: QuadraticEquation):
        """
        Class holding parameters necessary for race simulation dependent on car.
        :param fuel_capacity: fuel capacity in liters
        :param refueling_speed: in liters per second
        :param fuel_consumption: in liters per lap
        :param fuel_adj: avg time gain per liter of fuel (Time class)
        :param tyre_change_time: (Time class)
        :param tyre_degradation: Equation describing time loss with tyre degradation
        """
        self.fuel_capacity = fuel_capacity
        self.refueling_speed = refueling_speed
        self.fuel_consumption = fuel_consumption
        self.fuel_adj = fuel_adj
        self._fuel = fuel_capacity
        self.tyre_change_speed = tyre_change_time
        self.tyre_degradation = tyre_degradation

    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, value: float):
        if isinstance(value, (float, int)) and value <= self.fuel_capacity:
            self._fuel = value
        else:
            pass

    def get_fuel_time_gain(self) -> Time:
        return (self.fuel_capacity - self._fuel) * self.fuel_adj

    def get_tyre_time_loss(self, lap_number: int) -> Time:
        return Time(seconds=self.tyre_degradation(lap_number))

    def top_fuel_tank(self) -> Time:
        added_fuel = self.fuel_capacity - self._fuel
        self._fuel = self.fuel_capacity
        return Time(seconds=(added_fuel / self.refueling_speed))

    def add_fuel(self, fuel_amount: float) -> Time:
        if (self._fuel + fuel_amount) <= self.fuel_capacity:
            self._fuel += fuel_amount
            return Time(seconds=(fuel_amount / self.refueling_speed))
        else:
            return self.top_fuel_tank()

    def get_tyre_change_speed(self) -> Time:
        return self.tyre_change_speed

    def update_fuel(self) -> None:
        self._fuel -= self.fuel_consumption


class Simulation:
    def __init__(self, start_lap_time: Time, lap_time_std_dev: float, race_parameters: RaceParameters, car_parameters: CarParameters):
        self.start_lap_time = start_lap_time
        self.lap_time_std_dev = lap_time_std_dev
        self.race_parameters = race_parameters
        self.car_parameters = car_parameters
        self.laps_raced = 0
        self.laps_in_stint = 0
        self.tyre_laps = 0
        self.stint_length = Time(0, 0, 0, 0)

    def get_random_driver_diff(self) -> Time:
        return Time(seconds=gauss(0, self.lap_time_std_dev))

    def predict_lap_time(self) -> Time:
        lap_time = self.start_lap_time + self.car_parameters.get_fuel_time_gain() + \
            self.car_parameters.get_tyre_time_loss(self.tyre_laps) + \
            self.get_random_driver_diff()
        self.race_parameters.update_remaining_time(lap_time)
        self.car_parameters.update_fuel()
        self.laps_in_stint += 1
        self.tyre_laps += 1
        self.laps_raced += 1

        return lap_time

    def in_lap(self) -> Time:
        lap_time = self.start_lap_time + self.car_parameters.get_fuel_time_gain() + \
            self.car_parameters.get_tyre_time_loss(self.tyre_laps) + \
            self.get_random_driver_diff() + self.race_parameters.in_lap_time_loss

        self.race_parameters.update_remaining_time(lap_time)
        self.car_parameters.update_fuel()
        self.laps_in_stint = 0
        self.tyre_laps += 1
        self.laps_raced += 1

        return lap_time

    def out_lap(self, fuel_to_add: float, tyre_change=True) -> Time:
        lap_time = self.start_lap_time + self.car_parameters.get_fuel_time_gain() + \
                   self.get_random_driver_diff() + self.race_parameters.out_lap_time_loss + \
                   self.car_parameters.add_fuel(fuel_to_add)

        if tyre_change:
            lap_time = lap_time + self.car_parameters.tyre_change_speed
            self.tyre_laps = 0

        lap_time = lap_time + self.car_parameters.get_tyre_time_loss(self.tyre_laps)

        self.race_parameters.update_remaining_time(lap_time)
        self.car_parameters.update_fuel()
        self.laps_in_stint += 1
        self.laps_raced += 1

        return lap_time

    def tyre_time_loss_over_laps(self, from_lap: int, to_lap: int) -> Time:
        time_loss = Time(0, 0, 0, 0)
        while from_lap < to_lap:
            time_loss += self.car_parameters.get_tyre_time_loss(from_lap)
            from_lap += 1

        return time_loss


if __name__ == '__main__':
    pass
