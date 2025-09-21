module tt_um_wentansu_counter (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    wire load = ui_in[0];
    wire increment = ui_in[1];
    wire out_enable = ui_in[2];

    reg [7:0] value = 8'b0;

    always @(posedge clk) begin
        if (!rst_n) begin
            value[7:0] <= 8'b0;
        end

        else if (load) begin
            value[7:0] <= uio_in[7:0];
        end

        else if (increment) begin
            value[7:0] <= value[7:0] + 8'b1;
        end
    end

    assign uo_out[7:0] = out_enable ? value[7:0] : 8'b0;
    assign uio_out = 0;
    assign uio_oe = 0;

endmodule