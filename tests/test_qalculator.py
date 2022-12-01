#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, main

from mepcalc.qalculator import Qalculator
from mepcalc.medium import Medium

from pint import Quantity, Unit


class TestQalculator(TestCase):
    """Unit tests for Qalculator class."""

    def setUp(self):
        self.medium = Medium(
            "Test", heat_cap=Quantity(1, "J/(kg K)"), density=Quantity(1, "kg/m³")
        )
        self.qalc = Qalculator(medium=self.medium)

    def test_medium_getter_succeeds(self):
        """Check that the medium property returns the medium."""
        self.assertEqual(self.qalc.medium, self.medium)

    def test_medium_setter_fails(self):
        """Check that medium is a read only property."""
        with self.assertRaises(AttributeError):
            self.qalc.medium = Medium.air()

    def test_check_succeeds(self):
        """Check for different unit with same dimensionality succeeds."""
        quantity = Quantity(1, "kg/s")
        unit = Unit("kg/h")
        self.qalc.check(quantity, unit)

    def test_check_fails(self):
        """Check for different unit with difference dimensionality fails."""
        quantity = Quantity(1, "kg/s")
        unit = Unit("kg")
        with self.assertRaises(ValueError):
            self.qalc.check(quantity, unit)

    def test_heat_flow_from_mass_flow_succeeds(self):
        """Check that a calculation with good inputs succeeds."""
        mass_flow = Quantity(1, "kg/s")
        temp_diff = Quantity(1, "K")
        result = self.qalc.heat_flow_from_mass_flow(mass_flow, temp_diff)
        self.assertEqual(result, Quantity(1, "W"))

    def test_heat_flow_from_mass_flow_fails(self):
        """Check that a calculation with bad inputs fails."""
        good_mass_flow = Quantity(1, "kg/s")
        good_temp_diff = Quantity(1, "K")
        bad_mass_flow = Quantity(1, "kg")
        bad_temp_diff = Quantity(1, "m")
        with self.assertRaises(ValueError):
            self.qalc.heat_flow_from_mass_flow(bad_mass_flow, good_temp_diff)
            self.qalc.heat_flow_from_mass_flow(good_mass_flow, bad_temp_diff)

    # TODO: write remaining unit tests


if __name__ == "__main__":
    main()
