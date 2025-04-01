import re
from fuzzywuzzy import fuzz

class AirportMapper:
  def __init__(self, data_file):
    self.iata_to_info = {}
    self.airport_names = []
    self.city_names = []
    self.all_search_terms = []

    with open(data_file, 'r', encoding='utf-8') as f:
      for line in f:
        line = line.strip()
        if not line: 
          continue

        parts = line.split(' | ')
        if len(parts) >= 3:
          iata = parts[0].strip()
          airport_name = parts[1].strip()
          city = parts[2].strip()

          self.iata_to_info[iata] = {
            'airport': airport_name,
            'city': city
          }

          self.airport_names.append((iata, airport_name))
          self.city_names.append((iata, city))
          self.all_search_terms.append((iata, airport_name))
          self.all_search_terms.append((iata, city))

  def is_iata_code(self, code):
    return len(code) == 3 and code.isalpha()
  
  def find_iata(self, search_term):
    search_term = search_term.strip().lower()

    # already an IATA code, return it
    if self.is_iata_code(search_term) and search_term in self.iata_to_info:
      return search_term.upper()
    
    best_score = 0
    best_iata = None
    
    # fuzzy search
    # try airport names first
    for iata, name in self.airport_names:
      score = fuzz.token_set_ratio(search_term, name)
      if score > best_score:
        best_score = score
        best_iata = iata

    # try city names
    for iata, city in self.city_names:
      score = fuzz.token_set_ratio(search_term, city)
      if score > best_score:
        best_score = score
        best_iata = iata

    if best_score >= 50:  
      return best_iata.upper()
    
    return None