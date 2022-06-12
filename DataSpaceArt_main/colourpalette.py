def line_temperature(temperature: int):
    colours = ['#cc0199', '#c90194', '#c60190', '#c3018c', '#c00187', '#bd0183', '#ba017f', '#b7017b', '#b30176',
               '#b00172', '#ad016f', '#aa016b', '#a70167', '#a40163', '#a1015f', '#9e015c', '#9b0158', '#980155',
               '#950151', '#92004e', '#8f004b', '#8b0048', '#880045', '#850042', '#82003f', '#7f003c', '#7c0039',
               '#790036', '#760033', '#730031', '#70002e', '#6d002c', '#6a0029', '#670027', '#630025', '#600022',
               '#5d0020', '#5a001e', '#57001c', '#54001a', '#510018', '#4e0016', '#4b0015', '#480013', '#450011',
               '#410010', '#3e000e', '#3b000d', '#38000c', '#35000b', '#320009', '#2f0008', '#2c0007', '#290006',
               '#260005', '#230005', '#1f0004', '#1c0003', '#190002', '#160002', '#130001', '#100001']
    if temperature < -23:
        return '#CC0199'  # magenta
    elif temperature > 38:
        return '#100001'  # dark red
    else:
        for k, v in enumerate(colours, -23):
            if temperature == k:
                return v


if __name__ == '__main__':
    temp = input("Please specify a temperature:\n")
    print(f"{temp} corresponds to value {line_temperature(int(temp))}")
