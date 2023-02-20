#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from pint import Quantity

from mepcalc.common.medium import Medium
from mepcalc.common.ductulator import Ductulator


class TestQalculator(TestCase):
    """Unit tests for Ductulator class."""

    def setUp(self):
        self.medium = Medium(
            "Test", heat_cap=Quantity(1, "J/(kg K)"), density=Quantity(1, "kg/m³")
        )
        self.d = Ductulator(medium=self.medium)
        # good inputs
        self.good_mass_flow = Quantity(1, "kg/s")  # [mass] / [time]
        self.good_volume_flow = Quantity(1, "m³/s")  # [length]**3 / [time]

        # bad_inputs
        self.bad_mass_flow = Quantity(1, "kg/m")
        self.bad_volume_flow = Quantity(1, "m³/m")

    # Medium access TODO: extract to base class?
    def test_medium_getter_succeeds(self):
        """Check that the medium property returns the medium."""
        self.assertEqual(self.d.medium, self.medium)

    def test_medium_setter_fails(self):
        """Check that medium is a read only property."""
        with self.assertRaises(AttributeError):
            self.d.medium = Medium.air()

    # Heat Flow from Mass Flow
    def test_something_succeeds(self):
        """."""
        ...

    def test_something_fails_on_some_error(self):
        """."""
        ...
