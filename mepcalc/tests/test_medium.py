#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from pint import Quantity

from mepcalc.common.medium import Medium


class TestMedium(TestCase):
    """Unit tests for Medium class."""

    def setUp(self):
        self.name = "Name"
        self.heat_capacity = Quantity(1, "J/(kg K)")
        self.density = Quantity(1, "kg/m³")
        self.medium = Medium(
            name=self.name, heat_cap=self.heat_capacity, density=self.density
        )

    def test_instantiation_fails_on_bad_heat_capacity(self):
        bad_heat_capacity = Quantity(1, "J/K")
        with self.assertRaises(ValueError):
            Medium("Name", bad_heat_capacity, self.density)

    def test_instantiation_fails_on_bad_density(self):
        bad_density = Quantity(1, "m³/kg")
        with self.assertRaises(ValueError):
            Medium("Name", self.heat_capacity, bad_density)

    def test_name_getter_succeeds(self):
        self.assertEqual(self.medium.name, self.name)

    def test_heat_capacity_getter_succeeds(self):
        self.assertEqual(self.medium.heat_capacity, self.heat_capacity)

    def test_density_getter_succeeds(self):
        self.assertEqual(self.medium.density, self.density)

    def test_volumetric_heat_capacity_getter_succeeds(self):
        self.assertEqual(
            self.medium.volumetric_heat_capacity, self.heat_capacity * self.density
        )

    def test_heat_capacity_setter_succeeds(self):
        new_heat_capacity = Quantity(42, "J/(kg K)")
        self.medium.heat_capacity = new_heat_capacity
        self.assertEqual(self.medium.heat_capacity, new_heat_capacity)

    def test_heat_capacity_setter_fails(self):
        with self.assertRaises(ValueError):
            self.medium.heat_capacity = Quantity(666, "J/K")

    def test_density_setter_succeeds(self):
        new_density = Quantity(42, "kg/m³")
        self.medium.density = new_density
        self.assertEqual(self.medium.density, new_density)

    def test_density_setter_fails(self):
        with self.assertRaises(ValueError):
            self.medium.density = Quantity(666, "m³/kg")
