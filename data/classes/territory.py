from data.classes.diplomat_loadable import DiplomatLoadable
from data.classes.nation import Nation

class Territory(DiplomatLoadable):
	def __init__(self, board, identifier, names, owner_identifier, adjacent_territory_identifiers, is_supply_center):
		super().__init__(board, identifier, names)

		self.board.territories.append(self)

		if not isinstance(owner_identifier, str):
			raise TypeError('owner_identifier must be a string.')
		if not isinstance(adjacent_territory_identifiers, list):
			raise TypeError('adjacent_territory_identifiers must be a list.')
		for identifier in adjacent_territory_identifiers:
			if not isinstance(identifier, str):
				raise TypeError('adjacent_territory_identifiers must contain only strings.')
		if not isinstance(is_supply_center, bool):
			raise TypeError('is_supply_center must be a boolean.')

		self.owner_identifier = owner_identifier
		self.owner = None

		self.adjacent_territory_identifiers = adjacent_territory_identifiers
		self.adjacent_territories = []
		self.adjacent_land = []
		self.adjacent_water = []

		self.is_supply_center = is_supply_center

		self.units = []

	def set_owner(self, owner):
		if not isinstance(owner, Nation):
			raise TypeError('owner must be a Nation.')

		if self.owner != None:
			self.owner.territories.remove(self)
		self.owner = owner
		self.owner.territories.append(self)

	def view_string(self):
		return_string = str(self) + ': ' + str(self.names) + '\nOwner: ' + str(self.owner) + '\nAdjacent land:'
		for land in self.adjacent_land:
			return_string += ',\t' + str(land)
		return_string += '\nAdjacent water:'
		for water in self.adjacent_water:
			return_string += ',\t' + str(water)
		return_string += '\nSupply center: ' + str(self.is_supply_center) + '\nUnits:'
		for unit in self.units:
			return_string += ',\t' + str(unit)
		return return_string

	def init_relationships(self):
		super().init_relationships()
		
		for identifier in self.adjacent_territory_identifiers:
			if not identifier in self.board.loadables:
				raise IndexError('self.board.loadables does not contain identifier [' + identifier + '].')
			territory = self.board.loadables[identifier]
			if not isinstance(territory, Territory):
				raise TypeError('territory must be a Territory.')
			self.adjacent_territories.append(territory)

		self.adjacent_land = list(filter(lambda territory: isinstance(territory, LandTerritory) or isinstance(territory, HybridTerritory), self.adjacent_territories))
		self.adjacent_water = list(filter(lambda territory: isinstance(territory, WaterTerritory) or isinstance(territory, HybridTerritory), self.adjacent_territories))

		if self.owner_identifier == '-':
			return
		if not self.owner_identifier in self.board.loadables:
			raise IndexError('self.board.loadables does not contain self.owner_identifier [' + self.owner_identifier + '].')
		owner = self.board.loadables[self.owner_identifier]
		if not isinstance(owner, Nation):
			raise TypeError('owner must be a Nation.')
		self.set_owner(owner)

class WaterTerritory(Territory):
	load_from_query_identifier = 'w'

	@staticmethod
	def load_from_query(board, identifier, query):
		DiplomatLoadable.load_from_query(board, identifier, query)
		
		# Get names.
		if len(query) < 8:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		if query[0] != '[':
			raise SyntaxError('Expected an opening bracket.')
		query.pop(0)
		names = []
		current = query.pop(0)
		while current != ']' and len(query) > 0:
			if current != '-':
				names.append(current)
			current = query.pop(0)
		if current != ']':
			raise SyntaxError('Expected a closing bracket.')

		# Get owner_identifier.
		if len(query) < 5:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		owner_identifier = query.pop(0)

		# Get adjacent_territory_identifiers.
		if len(query) < 4:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		if query[0] != '[':
			raise SyntaxError('Expected an opening bracket.')
		query.pop(0)
		adjacent_territory_identifiers = []
		current = query.pop(0)
		while current != ']' and len(query) > 0:
			if current != '-':
				adjacent_territory_identifiers.append(current)
			current = query.pop(0)
		if current != ']':
			raise SyntaxError('Expected a closing bracket.')

		# Get is_supply_center.
		if len(query) < 1:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		is_supply_center = query.pop(0)
		if is_supply_center.startswith('t'):
			is_supply_center = True
		else:
			is_supply_center = False

		return WaterTerritory(board, identifier, names, owner_identifier, adjacent_territory_identifiers, is_supply_center)

class LandTerritory(Territory):
	load_from_query_identifier = 'l'

	def __init__(self, board, identifier, names, owner_identifier, adjacent_territory_identifiers, is_supply_center):
		super().__init__(board, identifier, names, owner_identifier, adjacent_territory_identifiers, is_supply_center)

		self.coasts = []

	@staticmethod
	def load_from_query(board, identifier, query):
		DiplomatLoadable.load_from_query(board, identifier, query)
		
		# Get names.
		if len(query) < 8:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		if query[0] != '[':
			raise SyntaxError('Expected an opening bracket.')
		query.pop(0)
		names = []
		current = query.pop(0)
		while current != ']' and len(query) > 0:
			if current != '-':
				names.append(current)
			current = query.pop(0)
		if current != ']':
			raise SyntaxError('Expected a closing bracket.')

		# Get owner_identifier.
		if len(query) < 5:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		owner_identifier = query.pop(0)

		# Get adjacent_territory_identifiers.
		if len(query) < 4:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		if query[0] != '[':
			raise SyntaxError('Expected an opening bracket.')
		query.pop(0)
		adjacent_territory_identifiers = []
		current = query.pop(0)
		while current != ']' and len(query) > 0:
			if current != '-':
				adjacent_territory_identifiers.append(current)
			current = query.pop(0)
		if current != ']':
			raise SyntaxError('Expected a closing bracket.')

		# Get is_supply_center.
		if len(query) < 1:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		is_supply_center = query.pop(0)
		if is_supply_center.startswith('t'):
			is_supply_center = True
		else:
			is_supply_center = False

		return LandTerritory(board, identifier, names, owner_identifier, adjacent_territory_identifiers, is_supply_center)

class HybridTerritory(LandTerritory):
	load_from_query_identifier = 'h'

	@staticmethod
	def load_from_query(board, identifier, query):
		DiplomatLoadable.load_from_query(board, identifier, query)
		
		# Get names.
		if len(query) < 8:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		if query[0] != '[':
			raise SyntaxError('Expected an opening bracket.')
		query.pop(0)
		names = []
		current = query.pop(0)
		while current != ']' and len(query) > 0:
			if current != '-':
				names.append(current)
			current = query.pop(0)
		if current != ']':
			raise SyntaxError('Expected a closing bracket.')

		# Get owner_identifier.
		if len(query) < 5:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		owner_identifier = query.pop(0)

		# Get adjacent_territory_identifiers.
		if len(query) < 4:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		if query[0] != '[':
			raise SyntaxError('Expected an opening bracket.')
		query.pop(0)
		adjacent_territory_identifiers = []
		current = query.pop(0)
		while current != ']' and len(query) > 0:
			if current != '-':
				adjacent_territory_identifiers.append(current)
			current = query.pop(0)
		if current != ']':
			raise SyntaxError('Expected a closing bracket.')

		# Get is_supply_center.
		if len(query) < 1:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		is_supply_center = query.pop(0)
		if is_supply_center.startswith('t'):
			is_supply_center = True
		else:
			is_supply_center = False

		return HybridTerritory(board, identifier, names, owner_identifier, adjacent_territory_identifiers, is_supply_center)
