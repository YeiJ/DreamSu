def format_file_size(self, size):
    """格式化文件大小为适当的单位"""
    try:
        size = int(size)  # 尝试将 size 转换为整数
    except (ValueError, TypeError):
        raise ValueError("文件大小必须是一个可转换为整数的值")

    if size < 0:
        raise ValueError("文件大小不能为负值")
    elif size < 1024:
        return f"{size} Bytes"
    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"
    else:
        return f"{size / (1024 ** 3):.2f} GB"