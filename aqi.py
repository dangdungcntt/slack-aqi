def get_color(value):
    if value <= 50:
        return '#0000ff'
    if value <= 100:
        return '#ffff00'
    if value <= 200:
        return '#ffa500'
    if value <= 300:
        return '#ff0000'
    return '#a52a2a'


def get_instruction(value):
    if value <= 50:
        return 'TỐT - Không ảnh hưởng đến sức khỏe'
    if value <= 100:
        return 'TRUNG BÌNH - Nhóm nhạy cảm nên hạn chế thời gian ở ngoài'
    if value <= 200:
        return 'KÉM - Nhóm nhạy cảm cần hạn chế thời gian ở ngoài'
    if value <= 300:
        return 'XẤU - Nhóm nhạy cảm tránh ra ngoài, những người khác hạn chế ở ngoài'
    return 'NGUY HẠI - Mọi người nên ở trong nhà'
