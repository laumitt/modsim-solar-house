import matplotlib.pyplot as plt
import numpy as np

month, week, low, high, low_time, high_time, sun_angle = np.loadtxt('weather.csv', delimiter=',', unpack=True, encoding='utf-8')
lists = [month, week, low, high, low_time, high_time, sun_angle]

class House:
    def __init__(self):
        self.side_length       = 50                      # length of side of house (assuming house is a rectangular prism)
        self.area              = self.side_length**2     # square footage estimate
        self.height            = 25                      # feet tall (2 story house)
        self.volume            = self.area * self.height # in cubic feet
        self.current_temp      = 70                      # start out with room temperature in deg F
        self.pane_surface_area = 0.08 * self.area        # window area as a percent of square footage * house square footage = square feet of window panes
        self.wall_surface_area = (self.side_length * self.height) - self.pane_surface_area
        self.roof_surface_area = self.area               # assuming roof equivalent to being flat
        self.pane_insulation   = 3.4                     # efficiency of pane insulation in retaining heat (R value) (3 (2 pane) - 5(3 pane))
        self.wall_insulation   = 20                      # efficiency of wall insulation in retaining heat (R value) (19-21)
        self.roof_insulation   = 49                      # efficiency of roof insulation in retaining heat (R value) (38-60)
        self.aux_heat_on       = True                    # is aux. heating on
        self.thermostat        = 70                      # what the auxiliary heater will heat to
        self.aux_heat_max      = 40000                   # BTU/hr
        self.max_temp          = 80                      # ideal max of house temperature
        self.min_temp          = 60                      # ideal min of house temperature
        self.release_rate      = 0.352456079             # rate of release of heat in BTU / ft^2 / deg F
        self.thermal_mass_temp = self.current_temp       # start thermal mass at same temperature as rest of house
        self.thermal_mass_area = self.pane_surface_area * 6
        self.stored_heat       = 0                       # initially thermal mass has no heat stored from sun
        self.thermal_capacity  = 1000 * 0.23884589662749592
        # heat capacity in J/kg/K (joules per kilogram per degree Kelvin) converted to BTU/lb/F (BTU per pound per degree F)
        self.thermal_mass      = (3000 * ((self.thermal_mass_area * 0.5) * 0.092903)) / 2.20462
        # thermal mass = floor density in kg/m^3 * ((size of window in square feet * 6 * thickness in feet) converted to m^3)) converted to pounds

    def update(self, timestep, ambient_temp): # timestep is 1 hour
        # heat_transfer in BTU, surface_area in square feet, temps are in F, r_value is square feet * F / BTU
        pane_heat_transfer = (self.pane_surface_area * (self.current_temp - ambient_temp))/(self.pane_insulation)
        wall_heat_transfer = (self.wall_surface_area * (self.current_temp - ambient_temp))/(self.wall_insulation)
        roof_heat_transfer = (self.roof_surface_area * (self.current_temp - ambient_temp))/(self.roof_insulation)
        total_heat_transfer = -((0.30 * pane_heat_transfer) + (0.40 * wall_heat_transfer) + (0.30 * roof_heat_transfer))
        # maybe add floor loss in future (accounts for 15% but for now all others are up by 5%)

        if world.is_sun_out == True:
            insolation = 32 * self.pane_surface_area # BTU available
        else:
            insolation = 0

        direct_heat = 0.4 * (insolation/6) # BTU directly heating house
        total_heat_transfer += direct_heat # direct heat from sun

        captured_heat = 0.6 * (insolation/6) # BTU captured by thermal mass
        self.stored_heat += captured_heat
        print('storing ' + str(self.stored_heat) + ' btu')

        total_heat_transfer += self.release_rate * self.stored_heat
        self.stored_heat -= self.release_rate * self.stored_heat

        if self.aux_heat_on and (self.thermostat >= self.current_temp):
            self.used_aux = True
            aux_heat_energy = self.aux_heat_max * (self.thermostat - self.current_temp) / 60
            total_heat_transfer += aux_heat_energy
        else:
            self.used_aux = False
        self.current_temp += total_heat_transfer / self.thermal_mass
        return self.current_temp

class World:
    def __init__(self):
        self.is_sun_out   = True  # is the sun out
        self.ambient_temp = 60    # deg. fahrenheit

    # various update functions so the world can change over the course of a day
    def flipSun(self):
        self.is_sun_out = (not self.is_sun_out)
    def changeAmbientTemp(self, new_temp):
        self.ambient_temp = new_temp

if __name__ == '__main__':
    # running model once = simulating one day
    house = House()
    world = World()
    timestep = 1
    time_log = []
    house_temp_log = []
    world_temp_log = []
    aux_log = []
    sim_length = len(week) * 7 * 24 # converting days to hours
    week_num = 0
    day_num = 0
    half_days = 0
    days_with_aux = 0
    for i in range(sim_length):
        if i % 12 == 0: # if it's halfway through a day
            if half_days % 2 == 0:
                world.changeAmbientTemp(high[week_num])
                print('changed ambient temp to {}'.format(high[week_num]))
                half_days += 1
                world.is_sun_out = True
            elif half_days % 2 == 1:
                world.changeAmbientTemp(low[week_num])
                print('changed ambient temp to {}'.format(low[week_num]))
                half_days += 1
                world.is_sun_out = False
        house_current_temp = house.update(timestep,world.ambient_temp) # update house temperature
        time_log.append(i)
        house_temp_log.append(house_current_temp)
        world_temp_log.append(world.ambient_temp)
        aux_log.append(house.used_aux)
        print('aux heat used? {}'.format(house.used_aux))
        if house.used_aux == True:
            days_with_aux += 1
        if house.current_temp > house.max_temp:
            print('house is too hot at week {} day {} and time {} house temp {}'.format(week_num, day_num, i, house_current_temp))
        elif house.current_temp < house.min_temp:
            print('house is too cold at week {} day {} and time {} house temp {}'.format(week_num, day_num, i, house_current_temp))
        else:
            print('house is fine at week {} day {} and time {} house temp {}'.format(week_num, day_num, i, house_current_temp))
        if i % 24 == 0 and i != 0: # i is not 0 is very important to get things to line up properly
            day_num += 1
        if day_num % 7 == 0 and day_num != 0: # i is not 0 is very important to get things to line up properly
            week_num += 1
            day_num = 0

    # graphing data
    print('used aux heat {} days out of {}'.format(days_with_aux/24, i/24))
    for x in time_log:
        time_log[x] = time_log[x] / (7 * 24)

    plt.figure(1)
    plt.plot(time_log, world_temp_log, '-', label='World Temperature')
    plt.plot(time_log, house_temp_log, '-', label='House Temperature')
    plt.plot(time_log, aux_log, '--', label='Days with Auxiliary Heat')
    plt.xlabel('Time (days)')
    plt.ylabel('Degrees (F)')
    plt.legend()
    plt.show()

# Assumptions
    # House is cubical (or geometrically equivalent to a cube)
    # Roof is mathematically flat (see above)
    # No auxiliary heating system (yet)
    # Windows are double-paned (triple-paned is expensive)
    # some Wacky stuff going on re: heating efficiency

# Things to Implement
    # Plot more data (configurations)
    # Interpret graphs
