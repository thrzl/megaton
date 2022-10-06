async def get_time(seconds: int):
    timedict = {}
    if seconds > 59:
        minutes = seconds // 60
        seconds = seconds % 60
        if seconds != 0:
            timedict["seconds"] = round(seconds, 2)
        timedict["minutes"] = minutes
        if minutes > 59:
            hours = minutes // 60
            minutes = minutes % 60
            if minutes != 0:
                timedict["minutes"] = round(minutes, 2)
            timedict["hours"] = hours
            if hours > 23:
                days = hours // 24
                hours = hours % 24
                if hours != 0:
                    timedict["hours"] = round(hours, 2)
                timedict["days"] = round(days, 2)

    return timedict
