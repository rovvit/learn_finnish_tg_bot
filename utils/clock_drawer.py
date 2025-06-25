import io
import cairo
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

    # Создаем изображение в памяти
    buffer = io.BytesIO()
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, canvas_size, canvas_size)
    ctx = cairo.Context(surface)

    # Фон — белый
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()

    # Рамка вокруг холста
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2.0)
    ctx.rectangle(margin, margin, canvas_size - 2 * margin, canvas_size - 2 * margin)
    ctx.stroke()

    # Обводка циферблата
    ctx.arc(center, center, radius, 0, 2 * math.pi)
    ctx.stroke()

    # Центр круга
    ctx.arc(center, center, pivot_radius, 0, 2 * math.pi)
    ctx.fill()

    # Часовые метки (деления)
    for i in range(12):
        angle = 2 * math.pi * (i / 12)
        outer_x = center + radius * 0.96 * math.sin(angle)
        outer_y = center - radius * 0.96 * math.cos(angle)
        inner_x = center + radius * 0.75 * math.sin(angle)
        inner_y = center - radius * 0.75 * math.cos(angle)

        ctx.set_line_width(1)
        ctx.move_to(inner_x, inner_y)
        ctx.line_to(outer_x, outer_y)
        ctx.stroke()

    # Часовая стрелка
    ctx.set_line_width(7)
    hour_angle = 2 * math.pi * (hour % 12 + minute / 60) / 12
    hx_outer = center + hour_hand_length * math.sin(hour_angle)
    hy_outer = center - hour_hand_length * math.cos(hour_angle)
    hx_inner = center + hand_inner_offset * math.sin(hour_angle)
    hy_inner = center - hand_inner_offset * math.cos(hour_angle)

    ctx.move_to(hx_outer, hy_outer)
    ctx.line_to(hx_inner, hy_inner)
    ctx.stroke()

    # Минутная стрелка
    ctx.set_line_width(4)
    minute_angle = 2 * math.pi * minute / 60
    mx_outer = center + minute_hand_length * math.sin(minute_angle)
    my_outer = center - minute_hand_length * math.cos(minute_angle)
    mx_inner = center + hand_inner_offset * math.sin(minute_angle)
    my_inner = center - hand_inner_offset * math.cos(minute_angle)

    ctx.move_to(mx_outer, my_outer)
    ctx.line_to(mx_inner, my_inner)
    ctx.stroke()

    surface.write_to_png(buffer)
    buffer.seek(0)
    return buffer
