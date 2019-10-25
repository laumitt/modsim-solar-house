# house class
    # attributes:
        # pane sq. ft.
        # pane insulation efficiency (percent heat retained)
        # floor thermal mass
        # rate of heat loss - how "leaky" etc. ACH range 0.35 to 0.5
        # wall/floor insulation efficiency (percent heat retained)
        # aux. heating on/off - expansion
        # aux. heating efficiency - expansion
        # volume of air in house
    # functions:
        # toggle aux heating - expansion
        # timestep update
class House:
    def init(self):
        self.side_length       = 50                      # length of side of house (assuming house is a rectangular prism)
        self.area              = self.side_length**2     # square footage estimate
        self.height            = 25                      # feet tall (2 story house)
        self.volume            = self.area * self.height # in cubic feet
        self.current_temp      = 68                      # start out with room temperature in deg F
        self.pane_surface_area = 0.08 * self.area        # window area as a percent of square footage * square footage = square feet of window panes
        self.wall_surface_area = (self.side_length * self.height) - self.pane_surface_area
        self.roof_surface_area = self.area               # assuming roof equivalent to being flat
        self.pane_insulation   = 3.4                     # efficiency of pane insulation in retaining heat (R value) (3 (2 pane) - 5(3 pane))
        self.wall_insulation   = 20                      # efficiency of wall insulation in retaining heat (R value) (19-21)
        self.roof_insulation   = 49                      # efficiency of roof insulation in retaining heat (R value) (38-60)
        # self.concrete_mass     =
        # self.water_mass        =
        self.thermal_mass      = 40                      # in units

    def update(self, timestep, ambient_temp): # timestep is 1 hour or so
        # heat_transfer in BTU/hour, surface_area in square feet, temp_a is larger temp in F, temp_b is smaller temp in F, r_value is square feet * F / BTU
        pane_heat_transfer   = (self.pane_surface_area * abs(self.current_temp - ambient_temp))/(self.pane_insulation)
        wall_heat_transfer   = (self.wall_surface_area * abs(self.current_temp - ambient_temp))/(self.wall_insulation)
        roof_heat_transfer   = (self.roof_surface_area * abs(self.current_temp - ambient_temp))/(self.roof_insulation)
        total_heat_transfer  = (0.30 * pane_heat_transfer) + (0.40 * wall_heat_transfer) + (0.30 * roof_heat_transfer) # maybe add floors in future (accounts for 15% but for now all others are up by 5%)
        self.current_temp    = total_heat_transfer / self.thermal_mass
        return self.current_temp

class World:
    def init(self):
        self.cloudy       = False # is it cloudy today? true/false
        self.sun_angle    = 45    # angle against the movement of the sun (altitude from horizon) - between 24 deg (jan) and 71 deg (jun)
        self.sun_position = 90    # angle with the movement of the sun (from east to west) - between 0 deg (sunrise), 180 deg (sunset), 359 deg (before sunrise)
        self.ambient_temp = 40    # deg. fahrenheit - between 30 deg (jan) and 74 deg (july)

    def flipCloudy(self):
        self.cloudy = (not self.cloudy)
    def changeSunAngle(self, new_angle):
        self.sun_angle = new_angle
    def changeSunPosition(self, new_position):
        self.sun_position = new_position
    def changeAmbientTemp(self, new_temp):
        self.ambient_temp = new_temp

if __name__ == '__main__':
    # running model once = simulating one day
    house = House()
    world = World()
    ambient_temp = 40
    timestep = 1
    house_current_temp = house.update(timestep,ambient_temp)
    print(house_current_temp)

# assumptions we're making
    # cube House
    # roof is flat if you go by the math
    # no aux. heating
    # windows are double-paned

# things to implement
    # actual sun heating
        # thermal mass etc.
    # aux. heating
    # actually taking data
    # plotting/interpreting data
