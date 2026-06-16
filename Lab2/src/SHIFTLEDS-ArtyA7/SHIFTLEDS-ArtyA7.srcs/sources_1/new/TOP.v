`timescale 1ns / 1ps

module TOP #(parameter N_LEDS = 4, NB_SEL = 2, NB_COUNT = 32, NB_SW = 4) (
    input clk, ext_reset,
    input [NB_SW-1:0] switch,
    output [N_LEDS-1:0] LED, G_LED, B_LED
);

    localparam R0 = (2**(NB_COUNT-10)) - 1;
    localparam R1 = (2**(NB_COUNT-9)) - 1;
    localparam R2 = (2**(NB_COUNT-8)) - 1;
    localparam R3 = (2**(NB_COUNT-7)) - 1;

    localparam SEL0 = 2'b00;
    localparam SEL1 = 2'b01;
    localparam SEL2 = 2'b10;
    localparam SEL3 = 2'b11;

    wire init, reset;
    wire [NB_SW-1:0] switch_wire;
    wire [NB_COUNT-1:0] limit;
    reg [NB_COUNT-1:0] counter;
    reg [N_LEDS-1:0] shiftreg;

    wire select_mux, vio_reset;
    wire [NB_SW-1:0] vio_switch;

    assign switch_wire = (select_mux) ? vio_switch : switch;
    assign reset = (select_mux) ? ~vio_reset : ~ext_reset;
    assign init = switch_wire[0];
    assign limit = (switch_wire[(NB_SW-1)-1 -: NB_SEL] == SEL0) ? R0 :
                   (switch_wire[(NB_SW-1)-1 -: NB_SEL] == SEL1) ? R1 :
                   (switch_wire[(NB_SW-1)-1 -: NB_SEL] == SEL2) ? R2 : R3;

    always @(posedge clk, posedge reset) begin : countAndShift
        if (reset) begin
            counter <= 0;
            shiftreg <= { {N_LEDS-1{1'b0}}, 1'b1 };
        end
        else if (init) begin
            if (counter >= limit) begin
                counter <= 0;
                shiftreg <= { shiftreg[N_LEDS-2 -: N_LEDS-1], shiftreg[N_LEDS-1] };
            end 
            else begin
                counter <= counter + 1;
                shiftreg <= shiftreg;
            end
        end 
        else begin
            counter <= counter;
            shiftreg <= shiftreg;
        end
    end

    assign LED = shiftreg;
    assign B_LED = (switch_wire[3] == 1'b0 ? shiftreg : {N_LEDS{1'b0}});
    assign G_LED = (switch_wire[3] == 1'b1 ? shiftreg : {N_LEDS{1'b0}});

    // VIO and ILA instance
    VIO vio_unit (
        .clk_0(clk),
        .probe_in0_0(LED),
        .probe_in1_0(B_LED),
        .probe_in2_0(G_LED),
        .probe_out0_0(select_mux),
        .probe_out1_0(vio_reset),
        .probe_out2_0(vio_switch)
    );

    ILA ila_unit (
        .clk_0(clk),
        .probe0_0(LED)
    );

endmodule
