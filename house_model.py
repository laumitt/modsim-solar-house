# house class
    # attributes:
        # window sq. ft.
        # window insulation efficiency (percent heat retained)
        # floor thermal mass
        # rate of heat loss - how "leaky" etc. ACH range 0.35 to 0.5
        # wall/floor insulation efficiency (percent heat retained)
        # aux. heating on/off
        # aux. heating efficiency
        # volume of air in house
    # functions:
        # toggle aux heating
        # timestep update
class House:
    def init(self):
        self.window_percentage = 2.22 # window size as a percentage of sq. footage
        self.window_insulation = 
        self.thermal_mass      =
        self.heat_loss         =
        self.wall_insulation   =
        self.area              = 2500 # square feet
        self.volume            = 63000 # cubic feet
        self.current_heat      =
    def update(self, timestep):
        self.current_heat = self.
# world class
    # attributes:
        # cloud cover (true/false)
        # time of year
        # sun position
        # ambient temp.
    # functions:
        # update cloud cover
        # update time of year
        # update sun position
        # change ambient temp.

# global stuff
    # time of day
