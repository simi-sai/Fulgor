`timescale 1ns / 1ps

module TOP (
    input clk, reset, 
    input TX,
    input [3:0] switch,
    output [3:0] led,
    output RX
);

    reg [3:0] DATA;
    reg TX_d;

    always @(posedge clk) begin
        if (!reset) begin
            TX_d <= 1'b0;
            DATA <= 4'b0000;
        end
        else if (switch[0] == 1) begin
            TX_d <= TX;

            if (TX_d != TX && switch[1] == 1) begin
                DATA <= { DATA[2:0], TX };
            end
            else if (switch[2] == 1 && switch[3] == 1) begin
                DATA <= 4'b1111;
            end
            else begin
                DATA <= DATA;
            end
        end
        else begin
            TX_d <= TX_d;
            DATA <= DATA;
        end
    end

    assign RX = TX_d;
    assign led = DATA;

endmodule
