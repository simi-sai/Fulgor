`timescale 1ns / 100ps

module tb_TOP ();
    reg clk, reset;
    reg [3:0] switch;
    reg TX;

    wire [3:0] led;
    wire RX;

    TOP uut (
        .clk(clk),
        .reset(reset),
        .switch(switch),
        .TX(TX),
        .led(led),
        .RX(RX)
    );

    initial begin
        clk = 0;
        forever #20 clk = ~clk;
    end

    task wait;
    input integer time_ns;
    begin
        #(time_ns);
        @(posedge clk);
    end
    endtask

    initial begin
        reset = 0;
        switch = 4'b0000;
        TX = 0;

        wait(1000);

        reset = 1;

        wait(1000);

        switch = 4'b0001;

        wait(1000);

        switch = 4'b0011;
        TX = 1;

        repeat (8) begin
            wait(0);
            TX = ~TX;
        end

        wait(0);

        switch = 4'b1101;

        wait(1000);

        switch = 4'b0000;

        wait(1000);

        $finish;
    end

endmodule
