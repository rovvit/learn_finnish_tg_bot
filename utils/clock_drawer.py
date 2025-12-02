from PIL import Image, ImageDraw
import io
import math

def generate_clock(hour: int, minute: int):
    canvas_size = 256
    margin = 2

    center = canvas_size / 2
    radius = (canvas_size - margin * 2) / 2 * 0.95
    pivot_radius = 5
    hour_hand_length = radius * 0.64
    minute_hand_length = radius * 0.8
    hand_inner_offset = radius * 0.08

    # Создаём белый холст
    img = Image.new("RGB", (canvas_size, canvas_size), "white")
    draw = ImageDraw.Draw(img)

    # Рамка
    draw.rectangle(
        [margin, margin, canvas_size - margin, canvas_size - margin],
        outline="black",
        width=2
    )

    # Циферблат
    draw.ellipse(
        [center - radius, center - radius,
         center + radius, center + radius],
        outline="black",
        width=2
    )

    # Центральная точка
    draw.ellipse(
        [center - pivot_radius, center - pivot_radius,
         center + pivot_radius, center + pivot_radius],
        fill="black"
    )

    # Деления
    for i in range(12):
        angle = 2 * math.pi * (i / 12)
        outer_x = center + radius * 0.96 * math.sin(angle)
        outer_y = center - radius * 0.96 * math.cos(angle)
        inner_x = center + radius * 0.75 * math.sin(angle)
        inner_y = center - radius * 0.75 * math.cos(angle)

        draw.line(
            [(inner_x, inner_y), (outer_x, outer_y)],
            fill="black",
            width=2
        )

    # Часовая стрелка
    hour_angle = 2 * math.pi * (hour % 12 + minute / 60) / 12
    hx_outer = center + hour_hand_length * math.sin(hour_angle)
    hy_outer = center - hour_hand_length * math.cos(hour_angle)
    hx_inner = center + hand_inner_offset * math.sin(hour_angle)
    hy_inner = center - hand_inner_offset * math.cos(hour_angle)

    draw.line(
        [(hx_inner, hy_inner), (hx_outer, hy_outer)],
        fill="black",
        width=7
    )

    # Минутная стрелка
    minute_angle = 2 * math.pi * minute / 60
    mx_outer = center + minute_hand_length * math.sin(minute_angle)
    my_outer = center - minute_hand_length * math.cos(minute_angle)
    mx_inner = center + hand_inner_offset * math.sin(minute_angle)
    my_inner = center - hand_inner_offset * math.cos(minute_angle)

    draw.line(
        [(mx_inner, my_inner), (mx_outer, my_outer)],
        fill="black",
        width=4
    )

    # В буфер
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
