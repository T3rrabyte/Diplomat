from data.classes.diplomat_loadable import DiplomatLoadable
from data.classes.nation import Nation
from data.classes.place import WaterTerritory, LandTerritory, HybridTerritory, Coast

class Unit(DiplomatLoadable):
	def __init__(self, board, identifier, owner_identifier, location_identifier):
		super().__init__(board, identifier)

		self.board.units.append(self)

		if not isinstance(owner_identifier, str):
			raise TypeError('owner_identifier must be a string.')
		if not isinstance(location_identifier, str):
			raise TypeError('location_identifier must be a string.')

		self.owner_identifier = owner_identifier
		self.owner = None

		self.action = None
		self.action_target = None

		self.power = 1

		self.location_identifier = location_identifier
		self.location = None
		self.old_location = None

		self.name = None
		self.old_name = None

	def __str__(self):
		return self.name

	def move_to(self, location):
		raise NotImplementedError('move_to is not implemented.')

	def movable_territories(self):
		raise NotImplementedError('movable_territories is not implemented.')

	def set_owner(self, owner):
		if not isinstance(owner, Nation):
			raise TypeError('owner must be a Nation.')

		if self.owner != None:
			self.owner.places.remove(self)
		self.owner = owner

	def init_relationships(self):
		if not self.owner_identifier in self.board.loadables:
			raise IndexError('self.board.loadables does not contain self.owner_identifier [' + self.owner_identifier + '].')
		owner = self.board.loadables[self.owner_identifier]
		if not isinstance(owner, Nation):
			raise TypeError('owner must be a Nation.')
		self.set_owner(owner)

		if not self.location_identifier in self.board.loadables:
			raise IndexError('self.board.loadables does not contain self.location_identifier [' + self.location_identifier + '].')

class Army(Unit):
	load_from_query_identifier = 'a'

	def __init__(self, board, identifier, owner_identifier, location_identifier):
		super().__init__(board, identifier, owner_identifier, location_identifier)

		self.convoys = []

	def move_to(self, location):
		if not isinstance(location, LandTerritory):
			raise TypeError('location must be a LandTerritory.')

		if self.location != None:
			self.old_location = self.location
		if self.name != None:
			self.old_name = self.name
		self.location = location
		self.name = self.owner.name + ' a ' + self.location.name

	def movable_territories(self):
		adjacent_land = self.location.adjacent_land
		convoy_destinations = list(territory for territory in [convoy.location.adjacent_land for convoy in self.convoys])
		return adjacent_land + convoy_destinations

	def init_relationships(self):
		super().init_relationships()

		location = self.board.loadables[self.location_identifier]
		if not isinstance(location, LandTerritory):
			raise TypeError('location must be a LandTerritory.')
		self.location = location

	@staticmethod
	def load_from_query(board, identifier, query):
		super().load_from_query(query)
		
		# Get owner_identifier.
		if len(query) < 2:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		owner_identifier = query.pop(0)

		# Get location_identifier.
		if len(query) < 1:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		location_identifier = query.pop(0)

		return Army(board, identifier, owner_identifier, location_identifier)

class Fleet(Unit):
	load_from_query_identifier = 'f'

	def move_to(self, location):
		if not (isinstance(location, WaterTerritory) or isinstance(location, HybridTerritory) or isinstance(location, Coast)):
			raise TypeError('location must be a WaterTerritory, HybridTerritory, or Coast.')

		if self.location != None:
			self.old_location = self.location
		if self.name != None:
			self.old_name = self.name
		self.location = location
		self.name = self.owner.name + ' f ' + self.location.name

	def movable_territories(self):
		if isinstance(self.location, WaterTerritory) or isinstance(self.location, HybridTerritory):
			return self.location.adjacent_territories
		elif isinstance(self.location, Coast):
			adjacent_territories_on_coast = list(filter(lambda territory: territory in self.location.territory.adjacent_territories, self.location.adjacent_territories))
			return adjacent_territories_on_coast
		else:
			raise TypeError('self.location must be a WaterTerritory, HybridTerritory, or Coast.')

	def init_relationships(self):
		super().init_relationships()

		location = self.board.loadables[self.location_identifier]
		if not (isinstance(location, WaterTerritory) or isinstance(location, HybridTerritory) or isinstance(location, Coast)):
			raise TypeError('location must be a WaterTerritory, HybridTerritory, or Coast.')
		self.location = location

	@staticmethod
	def load_from_query(board, identifier, query):
		super().load_from_query(query)
		
		# Get owner_identifier.
		if len(query) < 2:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		owner_identifier = query.pop(0)

		# Get location_identifier.
		if len(query) < 1:
			raise IndexError('There are not enough parts in the query to hold the necessary parameters.')
		location_identifier = query.pop(0)

		return Fleet(board, identifier, owner_identifier, location_identifier)
