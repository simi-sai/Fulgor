import serial
from legacy.filtro import RaisedCosineFilter


class ConsoleFilter:
    """Console-based interface for creating and visualizing Raised Cosine Filters using a serial communication loopback."""

    def __init__(self) -> None:
        ser = serial.serial_for_url('loop://', timeout=1)
        ser.timeout = None
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        self.filter_instance = None
        self.ser = ser

    def send_command(self, command) -> None:
        """Send a command to the serial interface character by character.
        - command (str): The command to be sent.
        """

        for ptr in range(len(command)):
            self.ser.write(command[ptr].encode())

    def read_response(self) -> str:
        """Read the response from the serial interface until no more data is available.
         - Returns: The complete response as a string.
        """

        out = ''
        while self.ser.in_waiting > 0:
            out += self.ser.read(1).decode()

        return out

    def run(self) -> None:
        """Main loop to run the console interface."""

        print("RaisedCosineFilter by Console \nDeveloped by: @simi-sai \n")

        print("\n--- Commands Available: ---\n"
              "- 'filter' to create a filter\n"
              "- 'plot' to visualize the filter\n"
              "- 'coef' to display filter coefficients\n"
              "- 'help' to get more information\n"
              "- 'exit' to quit.\n")

        while True:
            data = input(">>> ")

            if data == 'exit':
                self.ser.close()
                print("Exiting console...")
                break
            elif data == 'help':
                print("\n--- Commands Available: ---\n"
                      "- 'filter' to create a filter\n"
                      "- 'plot' to visualize the filter\n"
                      "- 'coef' to display filter coefficients\n"
                      "- 'help' to get more information\n"
                      "- 'exit' to quit.\n")
            else:  # Serial command processing
                self.send_command(data)
                response = self.read_response()
                self.process_command(response)

    def process_command(self, command) -> None:
        """Process the received command and execute corresponding actions.
        - command (str): The command received from the serial interface.
        """

        if command == 'filter':
            self.filter_instance = self.generate_filter()

        if command == 'plot':
            self.plot_filter()

        if command == 'coef':
            if self.filter_instance is not None:
                print("\nFilter Coefficients:")
                print(self.filter_instance.get_coefficients())
            else:
                print("No filter generated yet. Please create a filter first.")

    def generate_filter(self) -> RaisedCosineFilter:
        """Generate a Raised Cosine Filter based on user input parameters.
         - Returns: An instance of RaisedCosineFilter with the specified parameters.
        """

        alpha = float(
            input("Enter roll-off factor (0 < alpha <= 1): "))
        if alpha <= 0 or alpha > 1:
            print("Invalid alpha. Setting to default value of 0.25.")
            alpha = 0.25
        span = int(input("Enter filter span in symbols: "))
        sps = int(input("Enter samples per symbol: "))
        rrc = input("Generate Root Raised Cosine? (y/n): ")

        specs = [alpha, span, sps, rrc]
        response = []

        for spec in specs:
            self.send_command(str(spec))
            # Read acknowledgment for each spec
            response.append(self.read_response())

        response[3] = response[3].strip().lower() == 'y'

        filter = RaisedCosineFilter(
            alpha=float(response[0]), span=int(response[1]), sps=int(response[2]), rrc=bool(response[3]))

        print("\nFilter created successfully with the following parameters:")
        print(
            f"Alpha: {float(response[0])}, Span: {int(response[1])}, SPS: {int(response[2])}, RRC: {bool(response[3])}")
        print("Use 'plot' command to visualize the filter.\n")

        return filter

    def plot_filter(self) -> None:
        """Plot the filter response based on user input for time and frequency domain visualization."""

        if self.filter_instance is not None:
            type = input("Plot type (time/freq/both): ")

            self.send_command(type)
            response = self.read_response()

            time_domain = response in ['time', 'both']
            freq_domain = response in ['freq', 'both']

            self.filter_instance.plot(
                time_domain=time_domain, freq_domain=freq_domain)
        else:
            print("No filter generated yet. Please create a filter first.")


if __name__ == "__main__":
    console_filter = ConsoleFilter()
    console_filter.run()
