#!/usr/bin/env python3

### Edge cases test: this test checks some edges cases where an
### adder may return incorrect output, this is, there are 2
### positive numbers or 2 negative numbers added.
###
###
###
### 0 errors are returned due to lack of overflow control

from nmigen import *
from nmigen_cocotb import run
import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from random import getrandbits

# adder module
from adder import *



async def init_test(dut):
    cocotb.fork(Clock(dut.clk, 10, 'ns').start())
    dut.rst <= 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst <= 0


@cocotb.test()
async def burst(dut):
    await init_test(dut)

    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    #N = 100
    width = len(dut.a__data)
    mask = int('1' * width, 2)

    data_a = [int('1'*(width-1), 2), int('1' + '0'*(width-1), 2)]
    data_b = [int('1'*(width-1), 2), int('1' + '0'*(width-1), 2)]
    N = len(data_a)
    expected = [(da + db) & mask for da, db in zip(data_a, data_b)]
    cocotb.fork(stream_input_a.send(data_a))
    cocotb.fork(stream_input_b.send(data_b))
    recved = await stream_output.recv(N)
    assert recved == expected


if __name__ == '__main__':
    core = Adder(5)
    run(
        core, 'edge_cases_t',
        ports=
        [
            *list(core.a.fields.values()),
            *list(core.b.fields.values()),
            *list(core.r.fields.values())
        ],
        vcd_file='edge_cases_t.vcd'
    )
