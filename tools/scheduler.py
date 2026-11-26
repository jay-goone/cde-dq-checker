"""Small critical path scheduler (working days), enough to make a believable P6 programme.

Activities are dicts with: code, name, wbs, dur (days), cal, type, preds [(code, 'FS'|'SS', lag_days)],
cstr (None | ('SNET', date) | ('FON', date)).
Types follow P6: TT_Task, TT_Mile (start milestone), TT_FinMile (finish milestone).
"""
from datetime import date, timedelta

ONE = timedelta(days=1)


class Calendar:
    def __init__(self, cal_id, name, workdays, holidays=()):
        self.id, self.name = cal_id, name
        self.workdays = set(workdays)          # 0 = Monday
        self.holidays = set(holidays)

    def is_work(self, d):
        return d.weekday() in self.workdays and d not in self.holidays

    def next_work(self, d):                    # first working day on or after d
        while not self.is_work(d):
            d += ONE
        return d

    def prev_work(self, d):                    # last working day on or before d
        while not self.is_work(d):
            d -= ONE
        return d

    def add(self, d, n):                       # d is a working day; move n working days on
        d = self.next_work(d)
        for _ in range(n):
            d = self.next_work(d + ONE)
        return d

    def sub(self, d, n):
        d = self.prev_work(d)
        for _ in range(n):
            d = self.prev_work(d - ONE)
        return d

    def count(self, a, b):                     # working days from a to b, a <= b, excluding a
        n, d = 0, a
        while d < b:
            d += ONE
            if self.is_work(d):
                n += 1
        return n


def topo(acts):
    by = {a["code"]: a for a in acts}
    seen, order = set(), []

    def visit(c, stack=()):
        if c in seen:
            return
        if c in stack:
            raise ValueError("loop at " + c)
        for p, _, _ in by[c]["preds"]:
            if p not in by:
                raise KeyError(f"{c}: unknown predecessor {p}")
            visit(p, stack + (c,))
        seen.add(c)
        order.append(by[c])

    for a in acts:
        visit(a["code"])
    return order


def schedule(acts, cals, start):
    order = topo(acts)
    by = {a["code"]: a for a in acts}
    # forward pass
    for a in order:
        cal = cals[a["cal"]]
        cstr = a.get("cstr")
        if a["type"] == "TT_FinMile":
            ef = date.min
            for p, rel, lag in a["preds"]:
                q = by[p]
                base = q["ef"] if rel == "FS" else q["es"]
                ef = max(ef, cal.add(base, lag) if lag else base)
            if cstr and cstr[0] == "FON":
                if ef > cstr[1]:
                    raise ValueError(f"{a['code']} logic gives {ef}, after its date {cstr[1]}")
                ef = cstr[1]
            a["es"] = a["ef"] = ef
            continue
        es = start
        for p, rel, lag in a["preds"]:
            q = by[p]
            if rel == "FS":
                after = q["es"] if q["type"] == "TT_Mile" else q["ef"] + ONE
                cand = cal.add(cal.next_work(after), lag)
            else:  # SS
                cand = cal.add(cal.next_work(q["es"]), lag)
            es = max(es, cand)
        if cstr and cstr[0] == "SNET":
            es = max(es, cstr[1])
        es = cal.next_work(es)
        if a["type"] == "TT_Mile":
            a["es"] = es
            a["ef"] = es
        else:
            a["es"] = es
            a["ef"] = cal.add(es, a["dur"] - 1)
    finish = max(a["ef"] for a in acts)
    # backward pass
    succs = {a["code"]: [] for a in acts}
    for a in acts:
        for p, rel, lag in a["preds"]:
            succs[p].append((a, rel, lag))
    for a in reversed(order):
        cal = cals[a["cal"]]
        lf = finish
        cstr = a.get("cstr")
        if cstr and cstr[0] == "FON":
            lf = min(lf, cstr[1])
        for s, rel, lag in succs[a["code"]]:
            if rel == "FS":
                if s["type"] == "TT_FinMile":
                    lim = cal.sub(s["lf"], lag) if lag else s["lf"]
                elif a["type"] == "TT_Mile":
                    lim = cal.sub(s["ls"], lag)
                else:
                    lim = cal.prev_work(cals[s["cal"]].sub(s["ls"], lag) - ONE)
                lf = min(lf, lim)
            else:  # SS: my late start no later than successor's late start minus lag
                ls_lim = cals[s["cal"]].sub(s["ls"], lag)
                lf = min(lf, ls_lim if a["dur"] == 0 else cal.add(ls_lim, a["dur"] - 1))
        lf = cal.prev_work(lf) if a["type"] == "TT_Task" else lf
        a["lf"] = lf
        a["ls"] = cal.sub(lf, a["dur"] - 1) if a["type"] == "TT_Task" else lf
        a["tf"] = cal.count(a["ef"], a["lf"]) if a["lf"] >= a["ef"] else -cal.count(a["lf"], a["ef"])
    return finish
