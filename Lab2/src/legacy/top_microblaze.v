`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 09/27/2016 04:45:38 PM
// Design Name: 
// Module Name: top_instancia
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module top_microblaze
    (
        input           	 clock,
        input 	[3:0]        i_sw,
        //input 	[3:0]        i_btn,
        input                i_reset,
        output 	[3:0]        o_led,
        output          	 uart_rxd_out,
        input           	 uart_txd_in 
    );

        reg [3:0] copydata;
        reg       uart_txd_in_d;

        always@(posedge clock) begin
            if(!i_reset) begin
                uart_txd_in_d <= 1'b0;
                copydata      <= {4{1'b0}};
            end
            else if(i_sw[0]) begin
                uart_txd_in_d <= uart_txd_in;
                if(uart_txd_in_d!=uart_txd_in && i_sw[1])
                    copydata <= {copydata[2:0],uart_txd_in};
                else if(i_sw[2] && i_sw[3])
                    copydata <= {4{1'b1}};
                else
                    copydata <= copydata;
            end
            else begin
                uart_txd_in_d <= uart_txd_in_d;
                copydata      <= copydata;
            end
        end

        assign uart_rxd_out  = uart_txd_in_d;
        assign o_led         = copydata;
        
        
    
endmodule

