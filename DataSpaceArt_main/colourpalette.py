from colour import Color


def line_temperature(temperature: int):
    min_temp = -23
    max_temp = 38
    colours = list(Color('#cc0199').range_to('#100001', max_temp - min_temp + 1))
    if temperature < min_temp:
        return '#cc0199'  # magenta
    elif temperature > max_temp:
        return '#100001'  # dark red
    else:
        for k, v in enumerate(colours, min_temp):
            if temperature == k:
                return str(v)


if __name__ == '__main__':
    temp = input("Please specify a temperature:\n")
    print(f"{temp} corresponds to value {line_temperature(int(temp))}")
