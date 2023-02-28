#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
from unittest import TestCase

from pint import Quantity

from mepcalc.common.medium import Medium
from mepcalc.common.duct_calculator import DuctCalculator


class TestDuctCalculator(TestCase):
    """Unit tests for DuctCalculator class."""

    def setUp(self):
        self.medium = Medium(
            "Test", heat_cap=Quantity(1, "J/(kg K)"), density=Quantity(1, "kg/m³")
        )
        self.d = DuctCalculator(medium=self.medium)
        # good inputs
        self.good_mass_flow = Quantity(1, "kg/s")  # [mass] / [time]
        self.good_volume_flow = Quantity(1, "m³/s")  # [length]**3 / [time]
        self.good_velocity = Quantity(1, "m/s")  # [length]**2 / [time]
        self.good_area = Quantity(1, "m²")  # [length]**2
        self.good_length = Quantity(1, "m")  # [length]
        # bad inputs
        self.bad_mass_flow = Quantity(1, "kg/m")
        self.bad_volume_flow = Quantity(1, "m³/m")
        self.bad_velocity = Quantity(1, "s/m")
        self.bad_area = Quantity(1, "m")
        self.bad_length = Quantity(1, "m²")

    # Volume Flow from Area
    def test_volume_flow_from_area_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        V = v * A = 1 m/s * 1 m² = 1 m³/s
        """
        volume_flow = self.d.volume_flow_from_area(
            velocity=self.good_velocity, area=self.good_area
        )
        self.assertEqual(volume_flow, self.good_volume_flow)

    def test_volume_flow_from_area_fails_on_bad_velocity(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.volume_flow_from_area(
                velocity=self.bad_velocity, area=self.good_area
            )

    def test_volume_flow_from_area_fails_on_bad_area(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.volume_flow_from_area(
                velocity=self.good_velocity, area=self.bad_area
            )

    # Volume Flow from Width and Height
    def test_volume_flow_from_width_height_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        V = v * w * h = 1 m/s * 1 m * 1 m = 1 m³/s
        """
        volume_flow = self.d.volume_flow_from_width_height(
            velocity=self.good_velocity, width=self.good_length, height=self.good_length
        )
        self.assertEqual(volume_flow, self.good_volume_flow)

    def test_volume_flow_from_width_height_fails_on_bad_velocity(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.volume_flow_from_width_height(
                velocity=self.bad_velocity,
                width=self.good_length,
                height=self.good_length,
            )

    def test_volume_flow_from_width_height_fails_on_bad_length(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.volume_flow_from_width_height(
                velocity=self.good_velocity,
                width=self.bad_length,
                height=self.good_length,
            )
        with self.assertRaises(ValueError):
            self.d.volume_flow_from_width_height(
                velocity=self.good_velocity,
                width=self.good_length,
                height=self.bad_length,
            )

    # Volume Flow from Diameter
    def test_volume_flow_from_diameter_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        V = v * pi/4 * D^2 = 1 m/s * pi/4 * 1 m = pi/4 m³/s
        """
        volume_flow = self.d.volume_flow_from_diameter(
            velocity=self.good_velocity, diameter=self.good_length
        )
        good_volume_flow = self.good_volume_flow * (math.pi / 4)
        self.assertEqual(volume_flow, good_volume_flow)

    def test_volume_flow_from_diameter_fails_on_bad_velocity(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.volume_flow_from_diameter(
                velocity=self.bad_velocity, diameter=self.good_area
            )

    def test_volume_flow_from_diameter_fails_on_bad_diameter(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.volume_flow_from_diameter(
                velocity=self.good_velocity, diameter=self.bad_length
            )

    # Velocity from Area
    def test_velocity_from_area_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        v = V / A = 1 m³/s / 1 m² = 1 m/s
        """
        velocity = self.d.velocity_from_area(
            volume_flow=self.good_volume_flow, area=self.good_area
        )
        self.assertEqual(velocity, self.good_velocity)

    def test_velocity_from_area_fails_on_bad_volume_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.velocity_from_area(
                volume_flow=self.bad_volume_flow, area=self.good_area
            )

    def test_velocity_from_area_fails_on_bad_area(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.velocity_from_area(
                volume_flow=self.good_volume_flow, area=self.bad_area
            )

    # Velocity from Width and Height
    def test_velocity_from_width_height_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        v = V / (w * h) = 1 m³/s / (1 m * 1 m) = 1 m/s
        """
        velocity = self.d.velocity_from_width_height(
            volume_flow=self.good_volume_flow,
            width=self.good_length,
            height=self.good_length,
        )
        self.assertEqual(velocity, self.good_velocity)

    def test_velocity_from_width_height_fails_on_bad_volume_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.velocity_from_width_height(
                volume_flow=self.bad_volume_flow,
                width=self.good_length,
                height=self.good_length,
            )

    def test_velocity_from_width_height_fails_on_bad_length(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.velocity_from_width_height(
                volume_flow=self.good_volume_flow,
                width=self.bad_length,
                height=self.good_length,
            )
        with self.assertRaises(ValueError):
            self.d.velocity_from_width_height(
                volume_flow=self.good_volume_flow,
                width=self.good_length,
                height=self.bad_length,
            )

    # Velocity from Diameter
    def test_velocity_from_diameter_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        v = V / (pi/4 * D^2) = 1 m³/s / (pi/4 * (1 m)^2) = 4/pi m/s
        """
        velocity = self.d.velocity_from_diameter(
            volume_flow=self.good_volume_flow, diameter=self.good_length
        )
        good_velocity = self.good_velocity / (math.pi / 4)
        self.assertEqual(velocity, good_velocity)

    def test_velocity_from_diameter_fails_on_bad_volume_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.velocity_from_diameter(
                volume_flow=self.bad_volume_flow, diameter=self.good_length
            )

    def test_velocity_from_area_fails_on_bad_length(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.velocity_from_diameter(
                volume_flow=self.good_volume_flow, diameter=self.bad_length
            )

    # Volume Flow from Mass Flow
    def test_volume_flow_from_mass_flow_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        V = m / ϱ = 1 kg/s / 1 kg/m³ = 1 m³/s
        """
        volume_flow = self.d.volume_flow_from_mass_flow(mass_flow=self.good_mass_flow)
        self.assertEqual(volume_flow, self.good_volume_flow)

    def test_volume_flow_from_mass_flow_fails_on_bad_mass_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.volume_flow_from_mass_flow(mass_flow=self.bad_mass_flow)

    # Mass Flow from Volume Flow
    def test_mass_flow_from_volume_flow_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        m = V * ϱ = 1 m³/s * 1 kg/m³ = 1 kg/s
        """
        mass_flow = self.d.mass_flow_from_volume_flow(volume_flow=self.good_volume_flow)
        self.assertEqual(mass_flow, self.good_mass_flow)

    def test_mass_flow_from_volume_flow_fails_on_bad_volume_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.d.mass_flow_from_volume_flow(volume_flow=self.bad_volume_flow)
