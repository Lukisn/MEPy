#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
from unittest import TestCase

from pint import Quantity

from mepcalc.common.medium import Medium
from mepcalc.common.base_calculator import BaseCalculator


class TestBaseCalculator(TestCase):
    """Unit tests for Calculator class."""

    def setUp(self):
        self.medium = Medium(
            "Test", heat_cap=Quantity(1, "J/(kg K)"), density=Quantity(1, "kg/m³")
        )
        self.calc = BaseCalculator(medium=self.medium)

    def test_medium_getter_succeeds(self):
        """Check that the medium property returns the medium."""
        self.assertEqual(self.calc.medium, self.medium)

    def test_medium_setter_fails(self):
        """Check that medium is a read only property."""
        with self.assertRaises(AttributeError):
            self.calc.medium = Medium.air()
