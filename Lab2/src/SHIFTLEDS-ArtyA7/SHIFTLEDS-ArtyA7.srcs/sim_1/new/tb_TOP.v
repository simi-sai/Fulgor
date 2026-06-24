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

    // File-related variables
    integer fid_reset, fid_switch;
    integer error_reset, error_switch;
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
        clk = 0;
        forever #2.5 clk = ~clk; // 100MHz clock
    end

    initial begin
        fid_reset = $fopen("../../../../../vectors/reset.out", "r");
        if (fid_reset == 0) $stop;

        fid_switch = $fopen("../../../../../vectors/switch.out", "r");
        if (fid_switch == 0) $stop;
    end

    always @(posedge clk) begin : loadFile
        error_reset <= $fscanf(fid_reset, "%d", reset_tmp);
        if (error_reset != 1) $stop;

        for (ptr_switch = 0; ptr_switch < NB_SW; ptr_switch = ptr_switch + 1) begin
            error_switch <= $fscanf(fid_switch, "%d", switch_tmp[(ptr_switch + 1) - 1 -: 1]);
            if (error_switch != 1) $stop;
        end

        reset <= reset_tmp;
        switch <= switch_tmp;
        $display("%d", reset);
        $display("%d", switch);
    end

endmodule
