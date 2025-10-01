# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

def display_output(dut, cycle: int, value: int) -> None:
    dut._log.info(f"Output after cycle {cycle}: {value}")

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.ui_in.value = 0b110
    dut.uio_in.value = 0b11110

    cycle = 0

    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 1)
    cycle += 1
    display_output(dut, cycle, dut.uo_out.value)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    assert dut.uo_out.value == 0b0

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.

    await ClockCycles(dut.clk, 1)
    cycle += 1
    display_output(dut, cycle, dut.uo_out.value)

    dut.ui_in.value = 0b111
    await ClockCycles(dut.clk, 2)
    cycle += 2
    display_output(dut, cycle, dut.uo_out.value)

    dut.ui_in.value = 0b110
    await ClockCycles(dut.clk, 16)
    cycle += 16
    display_output(dut, cycle, dut.uo_out.value)

    dut.ui_in.value = 0b010
    await ClockCycles(dut.clk, 1)
    cycle += 1
    display_output(dut, cycle, dut.uo_out.value)
