from pprint import pprint
import pandas as pd

# --
# -- when a new event enter the system 
# -- it triggers the machine to move 1-step fwd
# -- once the machine settle in a state, 
# -- it triggers action of that state
# --
def print_statemachine(machine_spec):
	statemap = pd.DataFrame(
		index=machine_spec['state_names'],
		columns=machine_spec['state_names'],
		data=machine_spec['pathways']
	)
	print(statemap)

def new_machine_rt(*,prev_state=None,curr_state=0,curr_event=None,events=[]):
	return {
		'prev_state' : prev_state,
		'curr_state' : curr_state,
		'curr_event' : curr_event,
		'events' : events,
	}

def fetch_next_step(spec,rt):
	new_event = rt['events'].pop(0)
	# --
	possible_paths = spec['pathways'][rt['curr_state']]
	new_state = possible_paths.index(new_event)
	# --
	possible_actions = spec['action_vector']
	new_action = possible_actions[new_state]
	# --
	return (new_event, new_action, new_state)

def execute_machine(spec,rt):
	events = rt['events']
	while( rt['curr_state'] not in spec['terminal_states'] ):
		try:
			(new_event, new_action, new_state) = fetch_next_step(spec,rt)
			rt['prev_state'] = rt['curr_state']
			rt['curr_state'] = new_state
			rt['curr_event'] = new_event
			# --
			signals = new_action(rt)
			if(signals is None):
				return 1
			events.extend(signals)
		except BaseException as err:
			rt['err'] = err
			events.insert(0,"ERR")
	return 0
