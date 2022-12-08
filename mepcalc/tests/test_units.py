#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from pint import Quantity, Unit

from mepcalc.common.units import check_dimensionality


class TestCheckDimensionality(TestCase):
    """Unit tests for check_dimensionality function."""

    def setUp(self):
        self.quantity = Quantity(1, "m")
        self.good_unit = Unit("m")
        self.bad_unit = Unit("kg")

    def test_check_runs_through(self):
        self.assertEqual(check_dimensionality(self.quantity, self.good_unit), None)

    def test_check_raises(self):
        with self.assertRaises(ValueError):
            check_dimensionality(self.quantity, self.bad_unit)
