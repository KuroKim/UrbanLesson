from math import inf


def divide(first, second):
    try:
        return first / second
    except ZeroDivisionError:
        return inf
    except TypeError:
        return "Error: Invalid input type"
    except Exception as e:
        return f"Error: {str(e)}"
