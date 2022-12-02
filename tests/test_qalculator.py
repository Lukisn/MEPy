#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from mepcalc.qalculator import Qalculator
from mepcalc.medium import Medium

from pint import Quantity


class TestQalculator(TestCase):
    """Unit tests for Qalculator class."""

    def setUp(self):
        self.medium = Medium(
            "Test", heat_cap=Quantity(1, "J/(kg K)"), density=Quantity(1, "kg/m³")
        )
        self.q = Qalculator(medium=self.medium)
        # good inputs
        self.good_heat_flow = Quantity(1, "W")  # [length]**2 * [mass] / [time]**3
        self.good_mass_flow = Quantity(1, "kg/s")  # [mass] / [time]
        self.good_volume_flow = Quantity(1, "m³/s")  # [length]**3 / [time]
        self.good_temp_diff = Quantity(1, "K")  # [temperature]
        # bad_inputs
        self.bad_heat_flow = Quantity(1, "J")
        self.bad_mass_flow = Quantity(1, "kg/m")
        self.bad_volume_flow = Quantity(1, "m³/m")
        self.bad_temp_diff = Quantity(1, "kg")

    # Medium access
    def test_medium_getter_succeeds(self):
        """Check that the medium property returns the medium."""
        self.assertEqual(self.q.medium, self.medium)

    def test_medium_setter_fails(self):
        """Check that medium is a read only property."""
        with self.assertRaises(AttributeError):
            self.q.medium = Medium.air()

    # Heat Flow from Mass Flow
    def test_heat_flow_from_mass_flow_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        Q = m * cp * 𝛥T = 1 kg/s * 1 J/(kg K) * 1 K = 1 J/s = 1 W
        """
        heat_flow = self.q.heat_flow_from_mass_flow(
            mass_flow=self.good_mass_flow, temp_diff=self.good_temp_diff
        )
        self.assertEqual(heat_flow, self.good_heat_flow)

    def test_heat_flow_from_mass_flow_fails_on_bad_mass_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.heat_flow_from_mass_flow(
                mass_flow=self.bad_mass_flow, temp_diff=self.good_temp_diff
            )

    def test_heat_flow_from_mass_flow_fails_on_bad_temp_diff(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.heat_flow_from_mass_flow(
                mass_flow=self.good_mass_flow, temp_diff=self.bad_temp_diff
            )

    # Heat Flow from Volume Flow
    def test_heat_flow_from_volume_flow_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        Q = V * C * 𝛥T = 1 m³/s * 1 J/(m³ K) * 1 K = 1 J/s = 1 W
        """
        heat_flow = self.q.heat_flow_from_volume_flow(
            volume_flow=self.good_volume_flow, temp_diff=self.good_temp_diff
        )
        self.assertEqual(heat_flow, self.good_heat_flow)

    def test_heat_flow_from_volume_flow_fails_on_bad_volume_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.heat_flow_from_volume_flow(
                volume_flow=self.bad_volume_flow, temp_diff=self.good_temp_diff
            )

    def test_heat_flow_from_volume_flow_fails_on_bad_temp_diff(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.heat_flow_from_volume_flow(
                volume_flow=self.good_volume_flow, temp_diff=self.bad_temp_diff
            )

    # Mass Flow from Heat Flow
    def test_mass_flow_from_heat_flow_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        m = Q / (cp * 𝛥T) = 1 W / (1 J/(kg K) * 1 K) = 1 kg/s
        """
        mass_flow = self.q.mass_flow_from_heat_flow(
            heat_flow=self.good_heat_flow, temp_diff=self.good_temp_diff
        )
        self.assertEqual(mass_flow, self.good_mass_flow)

    def test_mass_flow_from_heat_flow_fails_on_bad_heat_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.mass_flow_from_heat_flow(
                heat_flow=self.bad_heat_flow, temp_diff=self.good_temp_diff
            )

    def test_mass_flow_from_heat_flow_fails_on_bad_temp_diff(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.mass_flow_from_heat_flow(
                heat_flow=self.good_heat_flow, temp_diff=self.bad_temp_diff
            )

    # Mass Flow from Volume Flow
    def test_mass_flow_from_volume_flow_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        m = V * ϱ = 1 m³/s * 1 kg/m³ = 1 kg/s
        """
        mass_flow = self.q.mass_flow_from_volume_flow(volume_flow=self.good_volume_flow)
        self.assertEqual(mass_flow, self.good_mass_flow)

    def test_mass_flow_from_volume_flow_fails_on_bad_volume_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.mass_flow_from_volume_flow(volume_flow=self.bad_volume_flow)

    # Volume Flow from Heat Flow
    def test_volume_flow_from_heat_flow_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        V = Q / (C * 𝛥T) = 1 W / (1 J/(m³ K) * 1 K) = 1 m³/s
        """
        volume_flow = self.q.volume_flow_from_heat_flow(
            heat_flow=self.good_heat_flow, temp_diff=self.good_temp_diff
        )
        self.assertEqual(volume_flow, self.good_volume_flow)

    def test_volume_flow_from_heat_flow_fails_on_bad_heat_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.volume_flow_from_heat_flow(
                heat_flow=self.bad_heat_flow, temp_diff=self.good_temp_diff
            )

    def test_volume_flow_from_heat_flow_fails_on_bad_temp_diff(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.volume_flow_from_heat_flow(
                heat_flow=self.good_heat_flow, temp_diff=self.bad_temp_diff
            )

    # Volume Flow from Mass Flow
    def test_volume_flow_from_mass_flow_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        V = m / ϱ = 1 kg/s / 1 kg/m³ = 1 m³/s
        """
        volume_flow = self.q.volume_flow_from_mass_flow(mass_flow=self.good_mass_flow)
        self.assertEqual(volume_flow, self.good_volume_flow)

    def test_volume_flow_from_mass_flow_fails_on_bad_mass_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.volume_flow_from_mass_flow(mass_flow=self.bad_mass_flow)

    # Temperature Difference from Mass Flow
    def test_temp_diff_from_mass_flow_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        𝛥T = Q / (m * cp) = 1 W / (1 kg/s * 1 J/(kg K)) = 1 K
        """
        temp_diff = self.q.temp_diff_from_mass_flow(
            heat_flow=self.good_heat_flow, mass_flow=self.good_mass_flow
        )
        self.assertEqual(temp_diff, self.good_temp_diff)

    def test_temp_diff_from_mass_flow_fails_on_bad_mass_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.temp_diff_from_mass_flow(
                heat_flow=self.good_heat_flow, mass_flow=self.bad_mass_flow
            )

    def test_temp_diff_from_mass_flow_fails_on_bad_heat_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.temp_diff_from_mass_flow(
                heat_flow=self.bad_heat_flow, mass_flow=self.good_mass_flow
            )

    # Temperature Difference from Volume Flow
    def test_temp_diff_from_volume_flow_succeeds(self):
        """Check that a calculation with good inputs succeeds.
        𝛥T = Q / (V * C) = 1 W / (1 m³/s * 1 J(m³ K)) = 1 K
        """
        temp_diff = self.q.temp_diff_from_volume_flow(
            heat_flow=self.good_heat_flow, volume_flow=self.good_volume_flow
        )
        self.assertEqual(temp_diff, self.good_temp_diff)

    def test_temp_diff_from_volume_flow_fails_on_bad_volume_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.temp_diff_from_volume_flow(
                heat_flow=self.good_heat_flow, volume_flow=self.bad_volume_flow
            )

    def test_temp_diff_from_volume_flow_fails_on_bad_heat_flow(self):
        """Check that a calculation with bad inputs fails."""
        with self.assertRaises(ValueError):
            self.q.temp_diff_from_volume_flow(
                heat_flow=self.bad_heat_flow, volume_flow=self.good_volume_flow
            )
