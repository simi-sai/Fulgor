//! @title Switch-controlled shift register - Testbench
//! @file tb_shiftleds.v
//! @author Advance Digital Design - Ariel Pola
//! @date 29-08-2021
//! @version Unit01 - Verilog

//! - Shift Register controlled by Switchs 
//! - **ck_rst** is the system reset, which resets the counter and initializes the shiftregister (SR).
//! - **i_sw[0]** controls the enable (1) of the counter. The value (0) stops the systems without change of the current state of the counter and the SR.
//! - The SR is moved only when the counter reached some limit **R0-R3**. 
//! - The choice of the limit can be made at any time during operation.
//! - **i_sw[3]** chooses the color of the RGB LEDs.

// Definitions
`define N_LEDS 4
`define NB_SEL 2
`define NB_COUNT 14
`define NB_SW 4

`timescale 1ns/100ps

module tb_shiftleds_file();

  // Parameters
  parameter N_LEDS    = `N_LEDS  ; //! Number of leds (4)
  parameter NB_SEL    = `NB_SEL  ; //! Number of bits of the selectors (2)
  parameter NB_COUNT  = `NB_COUNT; //! Number of bits of the counter (32)
  parameter NB_SW     = `NB_SW   ; //! Number of bits of the switch (4)


  wire [N_LEDS - 1 : 0] o_led    ; //! Leds
  wire [N_LEDS - 1 : 0] o_led_b  ; //! RGB Leds - Color Blue
  wire [N_LEDS - 1 : 0] o_led_g  ; //! RGB Leds - Color Green
  reg [NB_SW   - 1 : 0] i_sw     ; //! Switchs
  reg                   i_reset  ; //! Reset
  reg                   clock    ; //! System clock

  reg [NB_SW   - 1 : 0] switch_tmp; //! Load values for switch
  reg                   reset_tmp ; //! Load values for reset

  integer               fid_reset ;  //! File ID
  integer               fid_switch;  //! File ID
  integer               code_error;  //! Error pointer
  integer               code_error1; //! Error pointer
  integer               ptr_switch;  //! Pointer for read file
   
   //! Pointer initialization
   initial begin
      fid_reset  = $fopen("/home/apola/projects/cursodda/GuiaPractica01/rtl/vectors/reset.out","r");
	    if(fid_reset==0) $stop;
      fid_switch = $fopen("/home/apola/projects/cursodda/GuiaPractica01/rtl/vectors/switch.out","r");
	    if(fid_switch==0) $stop;

      clock    = 1'b0  ;
   end

   //! Clock generator
   always #2.5 clock = ~clock;

   //! Load files
   always@(posedge clock) begin: loadFile
      code_error <= $fscanf(fid_reset,"%d",reset_tmp);
      if(code_error!=1) $stop;

      for(ptr_switch=0;ptr_switch<NB_SW;ptr_switch = ptr_switch+1) begin
	     code_error1 <= $fscanf(fid_switch,"%d",switch_tmp[(ptr_switch+1)-1 -: 1]);
	     if(code_error1!=1) $stop;
	  end

      i_reset <= reset_tmp ;
      i_sw    <= switch_tmp;
      $display("%d",i_reset);
   end

   //! Shifleds instance
   shiftleds
     #(
       .N_LEDS   (N_LEDS  ),
       .NB_SEL   (NB_SEL  ),
       .NB_COUNT (NB_COUNT),
       .NB_SW    (NB_SW   )
       )
   u_shiftleds
     (
      .o_led     (o_led   ),
      .o_led_b   (o_led_b ),
      .o_led_g   (o_led_g ),
      .i_sw      (i_sw    ),
      .i_reset   (i_reset ),
      .clock     (clock   )
      );
   
endmodule // tb_shiftleds
