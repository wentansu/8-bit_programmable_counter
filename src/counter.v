module tt_um_wentansu_counter (
    input wire clk,
    input wire rst_n,
    input wire [7:0] load,
    input wire load_enable,
    input wire increment,
    input wire out_enable,
    output reg [7:0] value,
    output wire [7:0] out
);

    always @(posedge clk) begin
        if (!rst_n) begin
            value <= 8'b0;
        end

        else if (load_enable) begin
            value <= load;
        end

        else if (increment) begin
            value <= value + 8'b1;
        end
    end

    assign out = value;

endmodule