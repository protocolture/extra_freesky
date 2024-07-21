import redis

# Connect to Redis
r = redis.StrictRedis(host='192.168.20.71', port=6379, db=0)

# Extract the unique system names from the code_map
system_names = [
    "Reactor", "EnvironmentalSystems", "LifeSupport", "Comms", 
    "DefensiveSystems", "PsychicDiffuser", "Maglev", 
    "AccessControl", "SpiritContainmentField", 
    "status_light_10", "status_light_11", "status_light_12"  # Placeholders
]

# Set default status of all systems to red
for name in system_names:
    r.set(name, "(128, 0, 0)")

# Set default bar graph level to 1%
r.set('bar_graph_level', '1')

r.set('GOSMOKE','0')
r.set('GOSMOKEMORE','0')

