import json

R = 8.314462618


def load_data_from_json():
    dct = json.loads("specific_heat.json")
    return {item["name"]: item for item in dct}


class Converter:

    def __init__(self, m_mol: float, molecule_type: str, mass: float = None):
        self.molecule_data = load_data_from_json()[molecule_type]
        self.m_mol = m_mol
        self.r_star = R / self.m_mol
        self.cv = self.molecule_data["cv"] * self.r_star
        self.cp = self.molecule_data["cp"] * self.r_star
        self.k = self.cp / self.cv
        self.mass = mass

    def calculate_specific_status(self, values):
        if "V" in values and self.mass is None:
            raise ValueError("Mass not defined")
        if values == {"P", "v"}:
            values["T"] = values["P"] * values["v"] / self.r_star
        elif values == {"P", "V"}:
            values["T"] = values["P"] * values["V"] / (self.r_star * self.mass)
        elif values == {"P", "T"}:
            values["v"] = self.r_star * values["T"] / values["P"]
            if self.mass is not None:
                values["V"] = self.mass * self.r_star * values["T"] / values["P"]
        elif values == {"v", "T"}:
            values["P"] = self.r_star * values["T"] / values["v"]
        elif values == {"V", "T"}:
            values["P"] = self.mass * self.r_star * values["T"] / values["V"]
        else:
            raise ValueError("Malformed Query")
        return values

    # def calculate_transformation(self, start_values, end_values, index = None, isovol = False):
