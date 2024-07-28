# Progress bar of downloading torrents
def progress_bar(progress):
    bars = int(float(progress)) // 5

    return f"{'▣'*bars}{(20-bars)*'▢'}"


# Account space bar
def space_bar(totalSpace, spaceUsed):
    bars = round((spaceUsed / totalSpace) * 20)

    return f"{'▣'*bars}{(20-bars)*'▢'}"
