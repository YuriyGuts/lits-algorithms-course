with open("echoer.in", "r") as input_file:
    message=input_file.read()
    with open("echoer.out", "w") as output_file:
        output_file.write("Solution: {message}".format(message=message))
