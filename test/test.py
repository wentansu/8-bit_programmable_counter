# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

def display_output(dut, cycle: int, value: int) -> None:
    dut._log.info(f"Output after cycle {cycle}: {value}")

async def test_reset(dut):
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value == 0
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

async def test_tri_state(dut):
    dut.ui_in.value = 0b010
    await ClockCycles(dut.clk, 1)
    # assert dut.uo_out.value == 'ZZZZZZZZ'
    dut.ui_in.value = 0b110
    await ClockCycles(dut.clk, 1)

async def test_load(dut):
    dut.uio_in.value = 0b11111100
    dut.ui_in.value = 0b111
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value == 0b11111100
    dut.ui_in.value = 0b110

async def test_increment(dut):
    dut.uio_in.value = 0b00001111
    dut.ui_in.value = 0b111
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value == 0b00001111
    dut.ui_in.value = 0b100
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00001111
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == 0b00001111
    dut.ui_in.value = 0b110

async def test_counting(dut):
    dut.uio_in.value = 0b0
    dut.ui_in.value = 0b111
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value == 0b0
    dut.ui_in.value = 0b110
    await ClockCycles(dut.clk, 255)
    assert dut.uo_out.value == 0b11111110
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == 0b1000

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 1 us (1 MHz)
    clock = Clock(dut.clk, 1, units="us")
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

    dut.ui_in.value = 0b110
    await ClockCycles(dut.clk, 11)
    assert dut.uo_out.value == 0b1010

    await test_reset(dut)
    await test_tri_state(dut)
    await test_load(dut)
    await test_increment(dut)
    await test_counting(dut)
