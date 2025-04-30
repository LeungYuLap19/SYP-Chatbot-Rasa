from rapidfuzz import fuzz

class AirportMapper:
    def __init__(self, data_file):
        self.iata_to_info = {}
        self.index = []

        with open(data_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(" | ")
                if len(parts) >= 4:
                    iata = parts[0].strip().upper()
                    airport = parts[1].strip().lower()
                    city = parts[3].strip().lower()

                    self.iata_to_info[iata] = {"airport": airport, "city": city}
                    self.index.append((iata, airport, city))

    def is_iata_code(self, code):
        return len(code) == 3 and code.upper() in self.iata_to_info

    def find_iata(self, search_term):
        search_term = search_term.strip().lower()

        if self.is_iata_code(search_term):
            return search_term.upper()

        best_score = 0
        best_iata = None

        for iata, airport, city in self.index:
            airport_score = fuzz.partial_token_sort_ratio(search_term, airport)
            city_score = fuzz.partial_token_sort_ratio(search_term, city)

            # Weighted score: prioritize airport name
            total_score = 1.0 * airport_score + 0.6 * city_score

            if total_score > best_score:
                best_score = total_score
                best_iata = iata

        if best_score >= 70:
            return best_iata

        return None
