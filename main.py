import pulp
from pulp import PULP_CBC_CMD
from enum import Enum
from rich import print as rprint
from rich.table import Table
from rich.console import Console
from rich_tools import df_to_table
import pandas as pd
from helper import Class, Type, Faction

# Author's Note: If you are unfamiliar with Linear Programming and wish to know please consult the references section of the README.

# Midnight Tier Slots
tier_slots = ['Head', 'Shoulder', 'Chest', 'Hands', 'Legs']
token_groups = ['cloth', 'leather', 'mail', 'plate']
factions = [Faction.ALLIANCE, Faction.HORDE]

# Pulp DataDicts
current_tier = {} # Current Tier Pieces
vault_options = {} # Vault Tier Options
catalyst_charges = {} # Number of Catalyst Charges
player_weights = {} # Player Weights - The higher these values are set in the raider dictionary, the higher value completing their tier set is given
raider_factions = {} 

####################
#
#   Modify as needed
#
####################
# Raider Information 
# Split by armor type to make it easier to keep the roster straight.

leather_raiders = {
    'Boom': {
        "class" : Class.DRUID,
        "type" : Type.DPS,
        "faction": Faction.ALLIANCE,
        "current_tier": ['Head'],  
        "vault_options": ['Shoulder'],
        "catalyst_charges": 1,
        "player_weights": 2.0
    }, 

    'Charlie': {
        "class" : Class.DRUID,
        "type" : Type.TANK,
         "faction": Faction.ALLIANCE,
        "current_tier": ['Chest', 'Legs'], 
        "vault_options": ['Head'],
        "catalyst_charges": 0,
        "player_weights": 0.5
    },

    'Fka': {
        "class" : Class.DEMON_HUNTER,
        "type" : Type.DPS,
        "faction": Faction.ALLIANCE,
        "current_tier": [],
        "vault_options": ['Chest', 'Legs'],
        "catalyst_charges": 2,
        "player_weights": 2.0
    },

    'Jayken': {
        "class" : Class.ROGUE,
        "type" : Type.DPS,
         "faction": Faction.HORDE,
        "current_tier": ['Shoulder', 'Hands', 'Legs'],
        "vault_options": [],
        "catalyst_charges": 0,
        "player_weights": 2.0
    },

    'Nocth': {
        "class" : Class.DEMON_HUNTER,
        "type" : Type.DPS,
        "faction": Faction.HORDE,
        "current_tier": ['Head', 'Chest'],
        "vault_options": ['Hands'],
        "catalyst_charges": 1,
        "player_weights": 1.0
    },

    'Nymu': {
        "class" : Class.MONK,
        "type" : Type.HEALER,
        "faction": Faction.HORDE,
        "current_tier": ['Head', 'Chest'],
        "vault_options": ['Hands'],
        "catalyst_charges": 1,
        "player_weights": 1.0
    },

    'Puti': {
        "class" : Class.DRUID,
        "type" : Type.HEALER,
        "faction": Faction.HORDE,
        "current_tier": ['Head', 'Chest'],
        "vault_options": ['Hands'],
        "catalyst_charges": 1,
        "player_weights": 1.0
    },

    'Rev': {
        "class" : Class.MONK,
        "type" : Type.DPS,
        "faction": Faction.HORDE,
        "current_tier": ['Head', 'Chest'],
        "vault_options": ['Hands'],
        "catalyst_charges": 1,
        "player_weights": 1.0
    },

    'Vao': {
        "class" : Class.DEMON_HUNTER,
        "type" : Type.DPS,
        "faction": Faction.HORDE,
        "current_tier": ['Head', 'Chest'],
        "vault_options": ['Hands'],
        "catalyst_charges": 1,
        "player_weights": 1.0
    },
}
cloth_raiders = {
     'Bang': {
        "class" : Class.MAGE,
        "type" : Type.DPS,
        "faction": Faction.HORDE,
        "current_tier": ['Head'],  
        "vault_options": ['Shoulder'],
        "catalyst_charges": 1,
        "player_weights": 1.0
    }, 

    'Beef': {
        "class" : Class.PRIEST,
        "type" : Type.HEALER,
        "faction": Faction.HORDE,
        "current_tier": ['Chest', 'Legs'], 
        "vault_options": ['Head'],
        "catalyst_charges": 0,
        "player_weights": 1.0
    },

    'Marcx': {
        "class" : Class.WARLOCK,
        "type" : Type.DPS,
        "current_tier": [],
        "faction": Faction.HORDE,
        "vault_options": ['Chest', 'Legs'],
        "catalyst_charges": 2,
        "player_weights": 1.0
    },

    'Sol': {
        "class" : Class.MAGE,
        "type" : Type.DPS,
        "faction": Faction.HORDE,
        "current_tier": ['Shoulder', 'Hands', 'Legs'],
        "vault_options": [],
        "catalyst_charges": 0,
        "player_weights": 1.0
    },

    'Szardz': {
        "class" : Class.WARLOCK,
        "type" : Type.DPS,
        "faction": Faction.HORDE,
        "current_tier": ['Head', 'Chest'],
        "vault_options": ['Hands'],
        "catalyst_charges": 1,
        "player_weights": 1.0
    },

    'Ulti': {
        "class" : Class.PRIEST,
        "type" : Type.DPS,
        "faction": Faction.HORDE,
        "current_tier": ['Head', 'Chest'],
        "vault_options": ['Hands'],
        "catalyst_charges": 1,
        "player_weights": 1.0
    },
}
mail_raiders={
    'Astra': {
        "class" : Class.EVOKER,
        "type" : Type.HEALER,
        "faction": Faction.ALLIANCE,
        "current_tier": ['Head'],  
        "vault_options": ['Shoulder'],
        "catalyst_charges": 1,
        "player_weights": 1.0
    }, 

    'Brainranger': {
        "class" : Class.HUNTER,
        "type" : Type.DPS,
        "faction": Faction.ALLIANCE,
        "current_tier": ['Chest', 'Legs'], 
        "vault_options": ['Head'],
        "catalyst_charges": 0,
        "player_weights": 1.0
    },

    'Elaine': {
        "class" : Class.EVOKER,
        "type" : Type.DPS,
        "faction": Faction.ALLIANCE,
        "current_tier": [],
        "vault_options": ['Chest', 'Legs'],
        "catalyst_charges": 2,
        "player_weights": 1.0
    },

    'Gibdo': {
        "class" : Class.SHAMAN,
        "type" : Type.DPS,
        "faction": Faction.ALLIANCE,
        "current_tier": ['Shoulder', 'Hands', 'Legs'],
        "vault_options": [],
        "catalyst_charges": 0,
        "player_weights": 1.0
    },

    'Kyle': {
        "class" : Class.SHAMAN,
        "type" : Type.DPS,
        "faction": Faction.ALLIANCE,
        "current_tier": [],
        "vault_options": ['Chest', 'Legs'],
        "catalyst_charges": 2,
        "player_weights": 1.0
    },

    'Regal': {
        "class" : Class.HUNTER,
        "type" : Type.DPS,
        "faction": Faction.ALLIANCE,
        "current_tier": ['Shoulder', 'Hands', 'Legs'],
        "vault_options": [],
        "catalyst_charges": 0,
        "player_weights": 1.0
    },
}
plate_raiders={
    'Devysknight': {
        "class" : Class.DEATH_KNIGHT,
        "type" : Type.DPS,
        "faction": Faction.ALLIANCE,
        "current_tier": ['Head'],  
        "vault_options": ['Shoulder'],
        "catalyst_charges": 0,
        "player_weights": 1.0
    }, 

    'Mekes': {
        "class" : Class.PALADIN,
        "type" : Type.TANK,
        "faction": Faction.ALLIANCE,
        "current_tier": ['Chest', 'Legs'], 
        "vault_options": ['Head'],
        "catalyst_charges": 0,
        "player_weights": 1.0
    },

    'Pjs': {
        "class" : Class.PALADIN,
        "type" : Type.HEALER,
        "faction": Faction.ALLIANCE,
        "current_tier": [],
        "vault_options": ['Chest', 'Legs'],
        "catalyst_charges": 0,
        "player_weights": 1.0
    },

    'Worm': {
        "class" : Class.WARRIOR,
        "type" : Type.DPS,
        "faction": Faction.HORDE,
        "current_tier": ['Shoulder', 'Hands', 'Legs'],
        "vault_options": [],
        "catalyst_charges": 0,
        "player_weights": 1.0
    },
}
 
total_omni_drops_this_week = 2
total_tier_drops_by_type = {
    "cloth" : {
        'Head': 0, 
        'Shoulder': 1, 
        'Chest': 0, 
        'Hands': 0, 
        'Legs': 1
    },
    "leather" : {
        'Head': 1, 
        'Shoulder': 0, 
        'Chest': 0, 
        'Hands': 0, 
        'Legs': 1
    },
    "mail" : {
        'Head': 1, 
        'Shoulder': 1, 
        'Chest': 1, 
        'Hands': 1, 
        'Legs': 1
    },
    "plate" : {
        'Head': 0, 
        'Shoulder': 0, 
        'Chest': 0, 
        'Hands': 0, 
        'Legs': 1
    }

}
lfr_drops_by_faction = {
    Faction.ALLIANCE : {"cloth" : {
        'Head': 0, 
        'Shoulder': 1, 
        'Chest': 0, 
        'Hands': 0, 
        'Legs': 1
    },
    "leather" : {
        'Head': 1, 
        'Shoulder': 0, 
        'Chest': 0, 
        'Hands': 0, 
        'Legs': 1
    },
    "mail" : {
        'Head': 1, 
        'Shoulder': 1, 
        'Chest': 1, 
        'Hands': 1, 
        'Legs': 1
    },
    "plate" : {
        'Head': 0, 
        'Shoulder': 0, 
        'Chest': 0, 
        'Hands': 0, 
        'Legs': 0
    }},

    Faction.HORDE : {"cloth" : {
        'Head': 0, 
        'Shoulder': 1, 
        'Chest': 0, 
        'Hands': 0, 
        'Legs': 1
    },
    "leather" : {
        'Head': 1, 
        'Shoulder': 0, 
        'Chest': 0, 
        'Hands': 0, 
        'Legs': 1
    },
    "mail" : {
        'Head': 1, 
        'Shoulder': 1, 
        'Chest': 1, 
        'Hands': 1, 
        'Legs': 1
    },
    "plate" : {
        'Head': 0, 
        'Shoulder': 0, 
        'Chest': 0, 
        'Hands': 0, 
        'Legs': 0
    }}
}

## Do Not Touch Below

############################
# --- Input Data Setup   ---
############################
rprint("Setting Up Input Data")

# A dictionary to handle the raider name to the armor type
# Ex: 
#   RaiderA: cloth,
#   RaiderB: leather
raider_groups = {}

token_types = {
    "cloth": cloth_raiders, 
    "leather": leather_raiders, 
    "mail": mail_raiders, 
    "plate": plate_raiders}

# Mapping each raider to the various token types
for type in token_types:
    for raider in token_types[type].keys():
        raider_groups[raider] = type

# We combo the entire raid group together again. This is required to handle Omni tokens. Otherwise you can for-loop test each group > for better visuals.
raiders_dict = leather_raiders | cloth_raiders | mail_raiders | plate_raiders

#rprint("Creating pulp dictionaries.")
for raider in raiders_dict:
    current_tier[raider] = raiders_dict[raider]["current_tier"]
    vault_options[raider] = raiders_dict[raider]["vault_options"]
    catalyst_charges[raider] = raiders_dict[raider]["catalyst_charges"]
    player_weights[raider] = raiders_dict[raider]["player_weights"]
    raider_factions[raider] = raiders_dict[raider]["faction"]

# Create Raiders List for Iteration
raiders = raiders_dict.keys()
rprint("Completed Setting Up Input Data.")


rprint("Starting tier token optimization")
# Initialize Linear Program (LP) Problem
prob = pulp.LpProblem("WoW_Tier_Optimizer", pulp.LpMaximize) #For those not familiar with LP, we set this to maximize because we want the most tier sets created

############################
# --- Decision variables ---
############################
# Decision variables (dv) can be considered the choices we're making. In this scenario we care about how each character uses tier, and if they get 4pc.
# You can read more about LP DV's here: https://math.mit.edu/~goemans/18310S15/lpnotes310.pdf

token_dv = pulp.LpVariable.dicts("Token", (raiders, token_groups, tier_slots), cat='Binary')
vault_dv = pulp.LpVariable.dicts("Vault", (raiders, tier_slots), cat='Binary')
catalyst_dv = pulp.LpVariable.dicts("Catalyst", (raiders, tier_slots), cat='Binary')
omni_dv = pulp.LpVariable.dicts("OmniToken", (raiders, tier_slots), cat='Binary')
lfr_dv = pulp.LpVariable.dicts("LFRToken", (raiders, factions, token_groups, tier_slots), cat='Binary')

has_4pc = pulp.LpVariable.dicts("Has_4PC", raiders, cat='Binary')

#####################
# --- Constraints ---
#####################
# Here we define our rules for our problems. Keep in mind these are some form of inequality.

# Tier Token Supply Constraints & Faction Tier Token Supply Constraints
# For each group, and each tier slot, we cannot assign more than the total tier than have been dropped
for group in token_groups:
    for slot in tier_slots:
        prob += pulp.lpSum(token_dv[raider][group][slot] for raider in raiders) <= total_tier_drops_by_type[group][slot]

        # For each faction we cannot assign more than the number of dropped faction tokens to those faction players
        for faction in factions:
            prob += pulp.lpSum(lfr_dv[raider][faction][group][slot] for raider in raiders) <= lfr_drops_by_faction[faction][group][slot]


# Omni Token Supply Constraint - These are not armor specific, we ignore the groups.
# We cannot assign more than have been dropped.
prob += pulp.lpSum(omni_dv[raider][slot] for raider in raiders for slot in tier_slots) <= total_omni_drops_this_week

# Raider Constraints - Great Vault & Catalyst
for raider in raiders:
    current_tier_slots = current_tier[raider]
    current_count = len(current_tier_slots)
    assigned_group = raider_groups[raider]
    raider_faction = raider_factions[raider]
    
    # Great Vault Slots - We can only take 1 item
    prob += pulp.lpSum(vault_dv[raider][slot] for slot in tier_slots) <= 1
    
    # The item must actually exist in their vault
    for slot in tier_slots:
        if slot not in vault_options[raider]:
            prob += vault_dv[raider][slot] == 0
            
    # Catalyst Constraint - Cannot use more than the charges the raider has
    prob += pulp.lpSum(catalyst_dv[raider][slot] for slot in tier_slots) <= catalyst_charges[raider]

    # Slot Constraints
    for slot in tier_slots:

        # Group (Armor Type) Constraint - A player cannot use a armor from another group.
        for group in token_groups:
            if group != assigned_group:
                prob += token_dv[raider][group][slot] == 0
                
                for faction in factions:
                    prob += lfr_dv[raider][faction][group][slot] == 0

        # Faction Constraint
        # A player can only use LFR tier from their faction. - this catches the group (armor type) misses from above
        for faction in factions:
            if faction != raider_faction:
                for group in token_groups:
                    prob += lfr_dv[raider][faction][group][slot] == 0

        # Existing Tier Equipped Constraint
        # Cannot give a token, vault item, or catalyst charge for a slot they already possess
        if slot in current_tier_slots:
            for group in token_groups:
                prob += token_dv[raider][group][slot] == 0
                for faction in factions:
                    prob += lfr_dv[raider][faction][group][slot] == 0

            prob += vault_dv[raider][slot] == 0
            prob += catalyst_dv[raider][slot] == 0
            prob += omni_dv[raider][slot] == 0

        # Slot Specific Allotment Constraint
        # We do not want a raider to use a head token and a catalyst charge on the head slot
        prob += (pulp.lpSum(token_dv[raider][group][slot] for group in token_groups) 
                 + pulp.lpSum(lfr_dv[raider][faction][group][slot] for faction in factions for group in token_groups) 
                 + vault_dv[raider][slot] 
                 + catalyst_dv[raider][slot] 
                 + omni_dv[raider][slot]) <= 1

    # Our maximum total tier_pieces from all content can technically be 5, but for this we only care about maximizing 4-piece
    total_pieces_expr = (current_count 
    + pulp.lpSum(token_dv[raider][group][slot] for group in token_groups for slot in tier_slots) 
    + pulp.lpSum(lfr_dv[raider][faction][group][slot] for faction in factions for group in token_groups for slot in tier_slots) 
    + pulp.lpSum(vault_dv[raider][slot] + catalyst_dv[raider][slot] + omni_dv[raider][slot] for slot in tier_slots))

    prob += total_pieces_expr <= 4

    # Set the 'has_4pc' variable (if total pieces equal 4, has_4pc can scale to 1) 
    # - this is how we tell who has completed 4-piece
    prob += total_pieces_expr >= 4 * has_4pc[raider]


############################
# --- Objective Function ---
############################
# For our overall objective function, we are giving individual items like token, lfr, vault, and omni, high priority, 
# while giving catalyst usage a very low weight. 
# I.E. we prefer to use as many items as possible before we dip into raiders using catalyst.
FOUR_PIECE_BONUS = 100.0

prob += pulp.lpSum(
    (player_weights[raider] * (
        pulp.lpSum(token_dv[raider][group][slot] for group in token_groups) + 
        pulp.lpSum(lfr_dv[raider][faction][group][slot] for faction in factions for group in token_groups) + 
        vault_dv[raider][slot] + omni_dv[raider][slot]
    )) + 
     # Low weighting catalyst charges 
    (player_weights[raider] * 0.99 * catalyst_dv[raider][slot]) for raider in raiders for slot in tier_slots
) + pulp.lpSum(
    FOUR_PIECE_BONUS * has_4pc[raider] for raider in raiders
) 

# Solve
prob.solve(PULP_CBC_CMD(msg=False))

# --- Output Results ---
print(f"Status: {pulp.LpStatus[prob.status]}")
allocation_data = []
for raider in raiders:
    for slot in tier_slots:
        for group in token_groups:
            if token_dv[raider][group][slot].varValue == 1:
                print(token_dv[raider][group][slot])
                allocation_data.append({
                     'Raider': f"[#{raiders_dict[raider]["class"].value[0]}]{raider}[/#{raiders_dict[raider]["class"].value[0]}]", 
                     'Class Pool': group, 
                     'Source': 'Raid Drop Token', 
                     'Slot': slot, 
                     'Faction': ''})
            for faction in factions:
                if lfr_dv[raider][faction][group][slot].varValue == 1:
                    allocation_data.append({
                        'Raider': f"[#{raiders_dict[raider]["class"].value[0]}]{raider}[/#{raiders_dict[raider]["class"].value[0]}]", 
                        'Class Pool': group, 
                        'Source': f'LFR Drop Token ({faction})', 
                        'Slot': slot, 
                        'Faction': raider_factions[raider]})
        if vault_dv[raider][slot].varValue == 1:
            allocation_data.append({
                'Raider': f"[#{raiders_dict[raider]["class"].value[0]}]{raider}[/#{raiders_dict[raider]["class"].value[0]}]",  
                'Class Pool': '', 
                'Source': 'Great Vault', 
                'Slot': slot, 
                'Faction': ''})
        if catalyst_dv[raider][slot].varValue == 1:
            allocation_data.append({
                'Raider': f"[#{raiders_dict[raider]["class"].value[0]}]{raider}[/#{raiders_dict[raider]["class"].value[0]}]", 
                'Class Pool': '', 
                'Source': '⚡ Use Catalyst Charge', 
                'Slot': slot, 
                'Faction': ''})
        if omni_dv[raider][slot].varValue == 1:
            allocation_data.append({
                'Raider': f"[#{raiders_dict[raider]["class"].value[0]}]{raider}[/#{raiders_dict[raider]["class"].value[0]}]", 
                'Class Pool': '', 
                'Source': '🌟 Omni Token', 
                'Slot': slot, 
                'Faction': ''})  
    allocation_data.append({'Raider':"-", 'Class Pool':"-", 'Source': "-", 'Slot':"-", 'Faction': "-"})
results_df = pd.DataFrame(allocation_data)

table = Table(title='Optimal Distribution Table (Drops, Vaults & Catalyst)')
df_to_table(results_df, rich_table=table)
console=Console()
console.print(table)

print("\nSet Bonus Milestones Achieved This Week:")
for raider in raiders:
    if has_4pc[raider].varValue == 1:
        rprint(f"🎉 [#{raiders_dict[raider]["class"].value[0]}]{raider}[/#{raiders_dict[raider]["class"].value[0]}] ({raider_groups[raider]}) has secured their 4-Piece Set Bonus!")

print("\nMissing 4-Piece:")
for raider in raiders:
    if has_4pc[raider].varValue == 0:
        rprint(f"[#{raiders_dict[raider]["class"].value[0]}]{raider}[/#{raiders_dict[raider]["class"].value[0]}] ({raider_groups[raider]})")