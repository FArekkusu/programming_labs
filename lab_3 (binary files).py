def picture_magnify(source, target, times):
    with open(source, "rb") as image:
        bytes = bytearray(image.read())
        header, body = bytes[:54], bytes[54:]

    width, height = sum(header[18+i] * 2**(8*i) for i in range(4)), sum(header[22+i] * 2**(8*i) for i in range(4))
    padding = width % 4
    new_width, new_height = width * times, height * times
    new_padding = new_width % 4

    new_width, new_height = "{:>08}".format(hex(new_width)[2:]), "{:>08}".format(hex(new_height)[2:])
    header[18:22] = [int(new_width[2*i:2*i+2], 16) for i in range(4)][::-1]
    header[22:26] = [int(new_height[2*i:2*i+2], 16) for i in range(4)][::-1]

    bytes = bytearray()
    for _ in range(height):
        for _ in range(width * 3): bytes.append(body.pop(0))
        for _ in range(padding): body.pop(0)
    body = [bytes[3*i:3*(i+1)] for i in range(width * height)]

    new_body = bytearray()
    for i in range(height * times):
        for j in range(width):
            new_body += bytearray(body[width * (i//times) + j] * times)
        new_body += bytearray([0] * new_padding)

    with open(target, "wb") as image:
        image.write(header + new_body)

picture_magnify("bmp.bmp", "new_picture.bmp", 3)
