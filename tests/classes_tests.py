import unittest
from classes import *


class TestTime(unittest.TestCase):
    def test_init_mil_time_conversion(self):
        a = Time(1, 2, 3, 400)
        b = Time(milliseconds=3723400)
        self.assertEqual(a, b)

    def test_add(self):
        a = Time(1, 2, 3, 4)
        b = Time(2, 3, 4, 5)
        c = Time(3, 5, 7, 9)
        self.assertEqual(a + b, c)

    def test_sub(self):
        a = Time(3, 5, 7, 9)
        b = Time(2, 3, 4, 5)
        c = Time(1, 2, 3, 4)
        self.assertEqual(a - b, c)

    def test_mul_right(self):
        a = Time(1, 2, 3, 4)
        b = 2
        c = Time(2, 4, 6, 8)
        self.assertEqual(a * b, c)

    def test_mul_left(self):
        a = 2
        b = Time(1, 2, 3, 4)
        c = Time(2, 4, 6, 8)
        self.assertEqual(a * b, c)

    def test_divide_by_int(self):
        a = Time(2, 4, 6, 8)
        b = 2
        c = Time(1, 2, 3, 4)
        self.assertEqual(a / b, c)

    def test_divide_by_time(self):
        t1 = Time(0, 2, 20, 0)
        t2 = Time(0, 0, 2, 800)
        ans = 50
        self.assertEqual(t1 / t2, ans)

    def test_eq(self):
        a = Time(1, 2, 3, 4)
        b = Time(1, 2, 3, 4)
        self.assertTrue(a == b)

    def test_lt(self):
        a = Time(1, 2, 3, 4)
        b = Time(5, 6, 7, 8)
        self.assertTrue(a < b)

    def test_gt(self):
        a = Time(5, 6, 7, 8)
        b = Time(1, 2, 3, 4)
        self.assertTrue(a > b)

    def test_str_positive_time(self):
        a = "01:01:01.002"
        b = Time(1, 1, 1, 2)
        self.assertEqual(a, b.__str__())

    def test_str_negative_time(self):
        a = "-01:02:03.400"
        b = Time(milliseconds=-3723400)
        self.assertEqual(a, b.__str__())

    def test_in_seconds(self):
        a = Time(1, 2, 3, 456)
        b = 3723.456
        self.assertEqual(a.in_seconds(), b)


class TestQuadraticEquation(unittest.TestCase):
    def test_get_value(self):
        test_equation = QuadraticEquation(0.4, 0.01, 4.3)
        self.assertEqual(test_equation.get_value(10), 44.4)     # can run into float representation error

    def test_call(self):
        test_equation = QuadraticEquation(0.4, 0.01, 4.3)
        self.assertEqual(test_equation(10), 44.4)  # can run into float representation error


class TestCarParameters(unittest.TestCase):
    def test_fuel_setter(self):
        tyre_deg_equation = QuadraticEquation(0, 0.01, 0)
        car_params = CarParameters(75, 2.0, 5, Time(milliseconds=10), Time(seconds=20), tyre_deg_equation)
        car_params.fuel = 25
        self.assertEqual(car_params.fuel, 25)

    def test_fuel_setter_too_much_added(self):
        tyre_deg_equation = QuadraticEquation(0, 0.01, 0)
        car_params = CarParameters(75, 2.0, 5, Time(milliseconds=10), Time(seconds=20), tyre_deg_equation)
        car_params.fuel = 100
        self.assertEqual(car_params.fuel, 75)

    def test_get_fuel_time_gain(self):
        tyre_deg_equation = QuadraticEquation(0, 0.01, 0)
        car_params = CarParameters(75, 2.0, 5, Time(milliseconds=10), Time(seconds=20), tyre_deg_equation)
        car_params.fuel = 25
        self.assertEqual(car_params.get_fuel_time_gain(), Time(milliseconds=500))

    def test_get_tyre_time_loss(self):
        tyre_deg_equation = QuadraticEquation(0, 0.01, 0)
        car_params = CarParameters(75, 2.0, 5, Time(milliseconds=10), Time(seconds=20), tyre_deg_equation)
        self.assertEqual(car_params.get_tyre_time_loss(10), Time(seconds=0.1))

    def test_top_fuel_tank(self):
        tyre_deg_equation = QuadraticEquation(0, 0.01, 0)
        car_params = CarParameters(75, 2.0, 5, Time(milliseconds=10), Time(seconds=20), tyre_deg_equation)
        car_params.fuel = 25
        self.assertEqual(car_params.top_fuel_tank(), Time(seconds=25))
        self.assertEqual(car_params.fuel, 75)

    def test_get_tyre_change_speed(self):
        tyre_deg_equation = QuadraticEquation(0, 0.01, 0)
        car_params = CarParameters(75, 2.0, 5, Time(milliseconds=10), Time(seconds=20), tyre_deg_equation)
        self.assertEqual(car_params.get_tyre_change_speed(), Time(seconds=20))

    def test_update_fuel(self):
        tyre_deg_equation = QuadraticEquation(0, 0.01, 0)
        car_params = CarParameters(75, 2.0, 5, Time(milliseconds=10), Time(seconds=20), tyre_deg_equation)
        car_params.update_fuel()
        self.assertEqual(car_params.fuel, 70)


class TestRaceParameters(unittest.TestCase):
    def test_get_remaining_time(self):
        race_length = Time(6, 0, 0, 0)
        out_lap_time_loss = Time(0, 0, 20, 0)
        in_lap_time_loss = Time(0, 0, 10, 0)
        lower_class_cars = 20
        avg_overtake_time_loss = Time(0, 0, 0, 400)
        test_obj = RaceParameters(race_length, out_lap_time_loss, in_lap_time_loss, lower_class_cars, avg_overtake_time_loss)
        self.assertEqual(test_obj.get_remaining_time(), race_length)

    def test_update_remaining_time(self):
        race_length = Time(6, 0, 0, 0)
        out_lap_time_loss = Time(0, 0, 20, 0)
        in_lap_time_loss = Time(0, 0, 10, 0)
        lower_class_cars = 20
        avg_overtake_time_loss = Time(0, 0, 0, 400)
        test_obj = RaceParameters(race_length, out_lap_time_loss, in_lap_time_loss, lower_class_cars, avg_overtake_time_loss)
        time_update = Time(0, 2, 0, 0)
        test_obj.update_remaining_time(time_update)
        correct_time_after_update = Time(5, 58, 0, 0)
        self.assertEqual(test_obj.get_remaining_time(), correct_time_after_update)


class TestSimulation(unittest.TestCase):
    def test_get_random_driver_diff(self):
        race_length = Time(6, 0, 0, 0)
        out_lap_time_loss = Time(0, 0, 20, 0)
        in_lap_time_loss = Time(0, 0, 10, 0)
        lower_class_cars = 20
        avg_overtake_time_loss = Time(0, 0, 0, 400)
        race_params = RaceParameters(race_length, out_lap_time_loss, in_lap_time_loss, lower_class_cars, avg_overtake_time_loss)
        tyre_deg_equation = QuadraticEquation(0, 0.01, 0)
        car_params = CarParameters(75, 2.2, 4, Time(milliseconds=10), Time(seconds=20), tyre_deg_equation)

        sim = Simulation(Time(0, 1, 40, 0), 0.2, race_params, car_params)
        test_value = sim.get_random_driver_diff()
        # with standard deviation = 0.2 random value should fit in (-1, 1) range with 100% probability
        self.assertGreater(test_value, Time(seconds=-1))
        self.assertLess(test_value, Time(seconds=1))

    def test_tyre_time_loss_over_laps(self):
        race_length = Time(6, 0, 0, 0)
        out_lap_time_loss = Time(0, 0, 20, 0)
        in_lap_time_loss = Time(0, 0, 10, 0)
        lower_class_cars = 20
        avg_overtake_time_loss = Time(0, 0, 0, 400)
        race_params = RaceParameters(race_length, out_lap_time_loss, in_lap_time_loss, lower_class_cars, avg_overtake_time_loss)
        tyre_deg_equation = QuadraticEquation(0.1, 0.2, 0)
        car_params = CarParameters(75, 2.2, 4, Time(milliseconds=10), Time(seconds=20), tyre_deg_equation)

        sim = Simulation(Time(0, 1, 40, 0), 0.2, race_params, car_params)

        time_loss = sim.tyre_time_loss_over_laps(2, 5)
        correct_time_loss = Time(0, 0, 4, 700)
        self.assertEqual(time_loss, correct_time_loss)


if __name__ == '__main__':
    unittest.main()
