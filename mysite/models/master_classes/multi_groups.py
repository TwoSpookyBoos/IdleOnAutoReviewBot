from math import prod


class MultiGroups:
    def __init__(
        self,
        mga: float,
        mgb: float,
        mgc: float,
        mgd: float,
        mge: float,
        mgf: float,
        mgg: float,
    ):
        self.mga: float = mga
        self.mgb: float = mgb
        self.mgc: float = mgc
        self.mgd: float = mgd
        self.mge: float = mge
        self.mgf: float = mgf
        self.mgg: float = mgg
        self.total: float = prod([mga, mgb, mgc, mgd, mge, mgf, mgg])
