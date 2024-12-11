from screeninfo import get_monitors
import ctypes

# 获取当前显示缩放百分比


def get_screen_scaling_rate():
    """Get the DPI of the primary monitor."""
    monitors = get_monitors()
    hwd = ctypes.windll.user32.GetDC(0)
    scaling = ctypes.windll.gdi32.GetDeviceCaps(hwd, 88)  # 88 获取设备 DPI 缩放
    print(f"Current Display Scaling: {scaling}%")

    return scaling / 96
