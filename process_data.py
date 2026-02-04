import os

# Violation: Poor naming, no type hints, hardcoded secret, deep nesting
def p(d):
    k = "SK_LIVE_123456789" # SECRET!
    for i in d:
        if i:
            if i['status'] == 'active':
                if i['val'] > 10:
                    print("found one")
                    # Violation: Bare try/except
                    try:
                        res = i['val'] * 1.1
                        return res
                    except:
                        pass
    return None