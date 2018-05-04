import math, functools

def picture_magnify(source, target, times):
    with open(source, "rb") as image:
        bytes = bytearray(image.read())
        header, body = bytes[:54], bytes[54:]

    width, height = sum(header[18+i] * 2**(8*i) for i in range(4)), sum(header[22+i] * 2**(8*i) for i in range(4))
    padding = width % 4
    new_width, new_height = width * times, height * times
    i_new_w, i_new_h = int(new_width), int(new_height)
    new_padding = i_new_w % 4

    new_w, new_h = "{:>08}".format(hex(i_new_w)[2:]), "{:>08}".format(hex(i_new_h)[2:])
    header[18:22] = [int(new_w[2*i:2*i+2], 16) for i in range(4)][::-1]
    header[22:26] = [int(new_h[2*i:2*i+2], 16) for i in range(4)][::-1]

    bytes = bytearray()
    for _ in range(height):
        for _ in range(width * 3): bytes.append(body.pop(0))
        for _ in range(padding): body.pop(0)
    body = [[bytes[3*i+j*width*3:3*(i+1)+j*width*3] for i in range(width)] for j in range(height)]

    new_body = [[0 for _ in range(i_new_w)] for _ in range(i_new_h)]
    for i in range(i_new_h):
        for j in range(i_new_w):
            x = j / new_width * width
            y = i / new_height * height
            l, r = int(x), int(math.ceil(x) if x < width-1 else x)
            u, d = int(y), int(math.ceil(y) if y < height-1 else y)
            dx_1 = bytearray()
            dx_2 = bytearray()
            if r - l:
                for n in range(3):
                    dx_1.append(int((r - x)/(r - l) * body[u][l][n] + (x - l)/(r - l) * body[u][r][n]))
                    dx_2.append(int((r - x)/(r - l) * body[d][l][n] + (x - l)/(r - l) * body[d][r][n]))
            else:
                for n in range(3):
                    dx_1.append(int((body[u][l][n] + body[u][r][n]) / 2))
                    dx_2.append(int((body[d][l][n] + body[d][r][n]) / 2))
            dy = bytearray()
            if d - u:
                for n in range(3): dy.append(int((d - y)/(d - u) * dx_1[n] + (y - u)/(d - u) * dx_2[n]))
            else:
                for n in range(3): dy.append(int((dx_1[n] + dx_2[n]) / 2))
            new_body[i][j] = dy

    new_body = functools.reduce(lambda a, b: a + b, [functools.reduce(lambda a, b: a + b, x) + bytearray([0] * new_padding) for x in new_body])

    with open(target, "wb") as image:
        image.write(header + new_body)

picture_magnify("bmp.bmp", "new_picture.bmp", 10)