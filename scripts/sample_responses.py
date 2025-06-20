#!/usr/bin/env python3
"""
Ad-hoc script to call all DataGolf API endpoints and capture sample responses
for understanding response structures to write better tests.
"""
import json
import time
from datetime import datetime
from datagolf.request import RequestHandler

def capture_endpoint_responses():
    """Call all endpoints and capture their responses."""
    
    try:
        request_handler = RequestHandler()
    except Exception as e:
        print(f"Failed to initialize RequestHandler: {e}")
        print("Make sure you have API key configured in secrets.json")
        return
    
    responses = {
        'timestamp': datetime.now().isoformat(),
        'endpoints': {}
    }
    
    endpoints = [
        ('player_list', 'Player List & IDs'),
        ('field_updates', 'Field Updates'), 
        ('tour_schedules', 'Tour Schedules'),
        ('data_golf_rankings', 'Data Golf Rankings'),
        ('pre_tournament_predictions', 'Pre-Tournament Predictions'),
        ('pre_tournament_predictions_archive', 'Pre-Tournament Predictions Archive'),
        ('player_skill_decompositions', 'Player Skill Decompositions'),
        ('player_skill_ratings', 'Player Skill Ratings'),
        ('detailed_approach_skill', 'Detailed Approach Skill'),
        ('live_model_predictions', 'Live Model Predictions'),
        ('live_tournament_stats', 'Live Tournament Stats'),
        ('live_hole_scoring_distributions', 'Live Hole Scoring Distributions'),
        ('fantasy_projection_defaults', 'Fantasy Projection Defaults'),
        ('outright_odds', 'Outright Odds'),
        ('matchup_odds', 'Match-Up & 3-Ball Odds'),
        ('matchup_odds_all_pairings', 'Match-Up & 3-Ball All Pairings'),
        ('historical_raw_data_event_ids', 'Historical Raw Data Event IDs'),
        ('historical_round_scoring_data', 'Historical Round Scoring Data'),
        ('historical_odds_event_ids', 'Historical Odds Event IDs'),
        ('historical_outright_odds', 'Historical Outright Odds'),
        ('historical_matchup_odds', 'Historical Matchup Odds'),
        ('historical_dfs_event_ids', 'Historical DFS Event IDs'),
        ('historical_dfs_points_salaries', 'Historical DFS Points & Salaries'),
    ]
    
    print(f"Starting to capture responses from {len(endpoints)} endpoints...")
    print("This may take a few minutes due to API rate limiting...")
    
    for method_name, description in endpoints:
        print(f"\nCalling {method_name} ({description})...")
        
        try:
            method = getattr(request_handler, method_name)
            response = method()
            
            responses['endpoints'][method_name] = {
                'description': description,
                'success': True,
                'response_type': type(response).__name__,
                'response': response,
                'error': None
            }
            
            if isinstance(response, dict):
                print(f"  ✓ Success - Dict with keys: {list(response.keys())}")
                if len(str(response)) > 1000:
                    responses['endpoints'][method_name]['response'] = {
                        'keys': list(response.keys()),
                        'sample_truncated': True,
                        'first_few_chars': str(response)[:500] + "..."
                    }
            elif isinstance(response, list):
                print(f"  ✓ Success - List with {len(response)} items")
                if response and len(response) > 0:
                    first_item = response[0]
                    if isinstance(first_item, dict):
                        responses['endpoints'][method_name]['response'] = {
                            'list_length': len(response),
                            'first_item_keys': list(first_item.keys()) if isinstance(first_item, dict) else None,
                            'sample_items': response[:3]
                        }
                    else:
                        responses['endpoints'][method_name]['response'] = {
                            'list_length': len(response),
                            'sample_items': response[:10]
                        }
            else:
                print(f"  ✓ Success - {type(response).__name__}: {response}")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            responses['endpoints'][method_name] = {
                'description': description,
                'success': False,
                'response_type': None,
                'response': None,
                'error': str(e)
            }
        
        time.sleep(1)
    
    output_file = 'api_responses_sample.json'
    try:
        with open(output_file, 'w') as f:
            json.dump(responses, f, indent=2, default=str)
        print(f"\n✓ Responses saved to {output_file}")
    except Exception as e:
        print(f"\n✗ Failed to save responses: {e}")
    
    successful = sum(1 for endpoint in responses['endpoints'].values() if endpoint['success'])
    failed = len(endpoints) - successful
    
    print(f"\nSummary:")
    print(f"  Successful: {successful}/{len(endpoints)}")
    print(f"  Failed: {failed}/{len(endpoints)}")
    
    if failed > 0:
        print(f"\nFailed endpoints:")
        for method_name, data in responses['endpoints'].items():
            if not data['success']:
                print(f"  - {method_name}: {data['error']}")
    
    return responses

if __name__ == "__main__":
    capture_endpoint_responses()