`timescale 1ns / 100ps

module tb_TOP();

    parameter N_LEDS = 4;
    parameter NB_SEL = 2;
    parameter NB_COUNT = 32;
    parameter NB_SW = 4;

    wire [N_LEDS-1:0] LED, G_LED, B_LED;
    reg [NB_SW-1:0] switch;
    reg clk, reset;

    reg [NB_SW-1:0] switch_tmp;
    reg reset_tmp;

    integer fid_reset;
    integer fid_switch;
    integer code_error, code_error1;
    integer ptr_switch;

    TOP #(.N_LEDS(N_LEDS), .NB_SEL(NB_SEL), .NB_COUNT(NB_COUNT), .NB_SW(NB_SW)) 
    uut (
        .clk(clk),
        .ext_reset(reset),
        .switch(switch),
        .LED(LED),
        .G_LED(G_LED),
        .B_LED(B_LED)
    );

    initial begin
        fid_reset = $fopen("reset.out", "r");
        if (fid_reset == 0) $stop;
        fid_switch = $fopen("switch.out", "r");
        if (fid_switch == 0) $stop;

        clk = 1'b0;
    end

    always #2.5 clk = ~clk;

    always @(posedge clk) begin : loadFile
        code_error <= $fscanf(fid_reset, "%d", reset_tmp);
        if (code_error != 1) $stop;

        for (ptr_switch = 0; ptr_switch < NB_SW; ptr_switch = ptr_switch + 1) begin
            code_error1 <= $fscanf(fid_switch, "%d", switch_tmp[(ptr_switch + 1) - 1 -: 1]);
            if (code_error1 != 1) $stop;
        end

        reset <= reset_tmp;
        switch <= switch_tmp;
        $display("Reset: %d, Switch: %b", reset, switch);
    end

endmodule
