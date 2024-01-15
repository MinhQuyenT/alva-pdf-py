def find_head_region_position(x1, x2, y1, y2, frame):
    _x = 0
    _y = 0
    w = frame.shape[1]

    if x1 > _x:
        _x1 = x1
    if x2 > _x:
        _x = x2

    if y1 > _y:
        _y = y1
    if y2 > _y:
        _y = y2
    if w > _x:
        _x = w

    return _x, _y

