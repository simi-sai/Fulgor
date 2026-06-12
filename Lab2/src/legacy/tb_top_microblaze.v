`timescale 1ns/100ps

module tb_top_microblaze();

    reg              	clock;
    reg	    [3:0]       i_sw;
    //reg	    [3:0]       i_btn;
    wire 	[3:0]       o_led;
    wire                uart_rxd_out;
    reg                 uart_txd_in;
    reg                 i_reset; 

    initial begin
        clock         = 1'b0;
        i_reset       = 1'b0;
        i_sw          = 4'b0000;
        //i_btn         = 4'b0000;
        uart_txd_in   = 1'b0;
        #1000;
        @(posedge clock);
        i_reset       = 1'b1;
        #1000;
        @(posedge clock);
        i_sw          = 4'b0001;
        #1000;
        @(posedge clock);
        i_sw          = 4'b0011;
        uart_txd_in   = 1'b1;
        repeat (8) begin
            @(posedge clock);
            uart_txd_in   = ~uart_txd_in;          
        end
        @(posedge clock);
        i_sw          = 4'b1101;
        #1000;
        @(posedge clock);
        i_sw          = 4'b0000;
        #1000;
        @(posedge clock);
        $finish;
    end

    always #20 clock = ~clock;

    top_microblaze
        u_top_microblaze
            (
            .clock        (clock),
            .i_sw         (i_sw),
            .i_reset      (i_reset),
            //.btn        (i_btn),
            .o_led        (o_led),
            .uart_rxd_out (uart_rxd_out),
            .uart_txd_in  (uart_txd_in) 
            );

endmodule