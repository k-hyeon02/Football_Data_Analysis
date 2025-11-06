import module.pass_networkmap_def as pnm
import module.shot_map_def as sm
import module.match_table as mt
import module.eventchain_map as ec

events_file_path = "/Users/kyuhyeon/Documents/data/events/3773457.json"
lineup_file_path = "/Users/kyuhyeon/Documents/data/lineups/3773457.json"

pnm.draw_pass_network(events_file_path, lineup_file_path, side="home")
pnm.draw_pass_network(events_file_path, lineup_file_path, side="away")

##shotmap
sm.draw_shot_map(events_file_path, lineup_file_path, side="home")
sm.draw_shot_map(events_file_path, lineup_file_path, side="away")

## match table
match_data, team_names, possession_percentages = mt.extract_match_data(events_file_path)
mt.create_match_table(match_data, team_names, possession_percentages)

## most player
mt.extract_record_data(events_file_path)

## event chain
ec.draw_event_chain(events_file_path, lineup_file_path, "home")
ec.draw_event_chain(events_file_path, lineup_file_path, "away")
