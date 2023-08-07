def skill(func):
    func.__isskill = True
    return func
