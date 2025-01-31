"""
Name: Tom Yaeger
ID: 216082867
Assignment: ex7
"""
import csv

# Global BST root
ownerRoot = None

########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    """
    Prompt the user for an integer, re-prompting on invalid input.
    """
    newInput = input(prompt)
    while(True):
        invalid = False
        for character in newInput:
            if(ord(character) < ord('0') or ord(character) > ord('9')):
                print("Invalid input")
                invalid = True
                break
        if(invalid):
            newInput = input(prompt)
            continue
        else:
            break
    return int(newInput)

            

    

def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found.
    """
    global HOENN_DATA
    if(HOENN_DATA[poke_id-1] != None):
        return HOENN_DATA[poke_id-1].copy()
    

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    global HOENN_DATA
    for pokemon in HOENN_DATA:
        if(pokemon["Name"] == name):
            return pokemon.copy()
    return
    

def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    pass

def print_pokemon(pokemon):
    id = pokemon["ID"]
    name = pokemon["Name"]
    _type = pokemon["Type"]
    hp = pokemon["HP"]
    attack = pokemon["Attack"]
    canEvolve = pokemon["Can Evolve"]
    print(f"ID: {id}, Name: {name}, Type: {_type}, HP: {hp}, Attack: {attack}, Can Evolve: {canEvolve}")

########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon=None):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    owner_node = {
        "owner" : owner_name,
        "pokedex" : first_pokemon,
        "left" : None,
        "right" : None
    }
    return owner_node


def insert_owner_bst(root, new_node):
    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """
    if(root == None):
        return new_node
    if(root["owner"] > new_node["owner"]):
        root["left"] = insert_owner_bst(root["left"], new_node)
    else:
        root["right"] = insert_owner_bst(root["right"], new_node)
    return root

def find_owner_bst(root, owner_name):
    """
    Locate a BST node by owner_name. Return that node or None if missing.
    """
    if(root == None or root["owner"].lower() == owner_name.lower()):
        return root
    
    searchLeft = find_owner_bst(root["left"], owner_name)
    if(searchLeft != None):
        return searchLeft

    searchRight = find_owner_bst(root["right"], owner_name)
    if(searchRight != None):
        return searchRight

def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    while(node["left"] != None):
        node = node["left"]
    return node

def delete_owner_bst(root, owner_name):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    compareWith = root["owner"].lower()
    if(root == None):
        return None
    if(owner_name < compareWith):
        root["left"] = delete_owner_bst(root["left"], owner_name)
    elif (owner_name > compareWith):
        root["right"] = delete_owner_bst(root["right"], owner_name)
    else:
        if(root["left"] == None):
            return root["right"]
        elif(root["right"] == None):
            return root["left"]
        minNode = min_node(root["right"])
        root["owner"] = minNode["owner"]
        root["pokedex"] = minNode["pokedex"]
        root["right"] = delete_owner_bst(root["right"], root["owner"])
    return root

def prompt_owner_deletion():
    global ownerRoot
    ownerToDelete = input("Enter owner to delete: ")
    if(find_owner_bst(ownerRoot, ownerToDelete) != None):
        print(f"Deleting {ownerToDelete}'s entire Pokedex...")
        ownerRoot = delete_owner_bst(ownerRoot, ownerToDelete.lower())
        print("Pokedex deleted.")
    else:
        print(f"Owner '{ownerToDelete} not found.")
    print("")
########################
# 3) BST Traversals
########################

def print_owner(ownerNode):
    print("\nOwner:", ownerNode["owner"])
    pokedexSize = len(ownerNode["pokedex"])
    if(pokedexSize == 0):
        print("There are no Pokemons in this Pokedex that match the criteria.")
        return
    for i in range(0, pokedexSize, 1):
        print_pokemon(ownerNode["pokedex"][i])

def bfs_traversal(root):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    if(root == None):
        return
    queue = [root]
    while(len(queue) > 0):
        current = queue.pop(0)

        print_owner(current)
        if(current["left"] != None):
            queue.append(current["left"])
        if(current["right"] != None):
            queue.append(current["right"])

def pre_order(root):
    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    if(root == None):
        return
    print_owner(root)
    pre_order(root["left"])
    pre_order(root["right"])

def in_order(root):
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    if(root == None):
        return
    in_order(root["left"])
    print_owner(root)
    in_order(root["right"])

def post_order(root):
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """
    if(root == None):
        return
    post_order(root["left"])
    post_order(root["right"])
    print_owner(root)



########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    pokemonId = read_int_safe("Enter Pokemon ID to add: ")
    if(pokemonId < 1 or pokemonId > 135):
        print(f"ID {pokemonId} not found in Honen data.")
        return
    
    if(not is_pokemon_in_pokedex(owner_node["pokedex"], pokemonId)):
        newPokemon = get_poke_dict_by_id(pokemonId)
        owner_node["pokedex"].append(newPokemon)
        pokeName = newPokemon["Name"]
        owner_name = owner_node["owner"]
        print(f"Pokemon {pokeName} (ID {pokemonId}) added to {owner_name}'s Pokedex.")
    else:
        print("Pokemon already in the list. No changes made.")
def get_pokemon_index_from_pokedex(pokedex, pokeName):
    pokeName = pokeName.lower()
    for i, pokemon in enumerate(pokedex):
        if(pokemon["Name"].lower() == pokeName):
            return i
    return -1
def release_pokemon_by_name(owner_node):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    pokeName = input("Enter Pokemon Name to release: ").lower()
    index = get_pokemon_index_from_pokedex(owner_node["pokedex"], pokeName)

    realPokeName = owner_node["pokedex"][index]["Name"]
    realOwnerName = owner_node["owner"]
    print(f"Releasing {realPokeName} from {realOwnerName}.")
    owner_node["pokedex"].pop(index)
def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    
    pokeName = input("Enter Pokemon Name to evolve: ")
    i = get_pokemon_index_from_pokedex(owner_node["pokedex"], pokeName)
    
    if(i == -1):
        name = owner_node["owner"]
        print(f"No Pokemon named '{pokeName}' in {name}'s Pokedex.")
    else:
        if(not owner_node["pokedex"][i]["Can Evolve"]):
            print(f"{pokeName} cannot evolve.")
            return
        idOfPrevious = owner_node["pokedex"][i]["ID"]
        name = owner_node["pokedex"][i]["Name"]
        pokemonData = get_poke_dict_by_id(idOfPrevious+1)
        newPokemonName = pokemonData["Name"]
        newId = pokemonData["ID"]
        j = get_pokemon_index_from_pokedex(owner_node["pokedex"], pokemonData["Name"])
        print(f"Pokemon evolved from {name} (ID {idOfPrevious}) to {newPokemonName} (ID {newId}).")
        if(j != -1):
            owner_node["pokedex"].pop(i)
            print(f"{newPokemonName} was already present; releasing it immediately.")
        else:
            owner_node["pokedex"][i] = pokemonData

########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    if(root == None):
        return
    gather_all_owners(root["left"], arr)
    gather_all_owners(root["right"], arr)
    arr.append(root)
    

def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    global ownerRoot
    if(ownerRoot == None):
        print("No owners at all.")
        return
    
    owners = []
    gather_all_owners(ownerRoot, owners)

    sorted = False
    while(True):
        sorted = True
        for i in range(0, len(owners)-1,1):
            if(len(owners[i]["pokedex"]) > len(owners[i+1]["pokedex"])):
                temp = owners[i]
                owners[i] = owners[i+1]
                owners[i+1] = temp
                sorted = False
        if(sorted):
            break


    print("=== The Owners we have, sorted by number of Pokemons ===")
    for i in range(0, len(owners), 1):
        name = owners[i]["owner"]
        amount = len(owners[i]["pokedex"])
        print(f"Owner: {name} (has {amount} Pokemon)")
    print("")


########################
# 6) Print All
########################
def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    global ownerRoot
    print("1) BFS\n"
        "2) Pre-Order\n",
        "3) In-Order\n",
        "4) Post-Order", sep="")
    choice = read_int_safe("Your choice: ")

    if(choice == 1):
        bfs_traversal(ownerRoot)
    elif(choice == 2):
        pre_order(ownerRoot)
    elif(choice == 3):
        in_order(ownerRoot)
    elif(choice == 4):
        post_order(ownerRoot)
    else:
        print("Invalid choice.")
    print("")
########################
# 7) The Display Filter Sub-Menu
########################
def display_filter_sub_menu(pokedex):
    """
    1) Only type X
    2) Only evolvable
    3) Only Attack above
    4) Only HP above
    5) Only name starts with
    6) All
    7) Back
    """
    choice = 0
    while(True):
        print("\n-- Display Filter Menu --\n",
            "1. Only a certain Type\n",
            "2. Only Evolvable\n",
            "3. Only Attack above __\n",
            "4. Only HP above __\n",
            "5. Only names starting with letter(s)\n",
            "6. All of them!\n",
            "7. Back", sep="")
        
        choice = read_int_safe("Your choice: ")
        filteredList = None
        if(choice == 1):
            _type = input("Which Type? (e.g. GRASS, WATER): ")
            filteredList = [pokemon if(pokemon["Type"].lower() == _type.lower()) else None for pokemon in pokedex]
        elif(choice == 2):
            filteredList = [pokemon if(pokemon["Can Evolve"].upper() == "TRUE") else None for pokemon in pokedex]
        elif(choice == 3):
            attackThreshold = read_int_safe("Enter Attack threshold: ")
            filteredList = [pokemon if(pokemon["Attack"] > attackThreshold) else None for pokemon in pokedex]
        elif(choice == 4):
            hpThreshold = read_int_safe("Enter HP threshold: ")
            filteredList = [pokemon if(pokemon["HP"] > hpThreshold) else None for pokemon in pokedex]
        elif(choice == 5):
            startingLetters = input("Starting letter(s): ").lower()
            filteredList = [pokemon if(pokemon["Name"].lower()[0:len(startingLetters)-1] == startingLetters) else None for pokemon in pokedex]
        elif(choice == 6):
            filteredList = pokedex
        elif(choice == 7):
            print("Back to Pokedex Menu.")
            return
        else:
            print("Invalid choice.")
            continue
        noneCounter = 0
        for i, pokemon in enumerate(filteredList):
            if(pokemon == None):
                noneCounter+=1
                continue
            else:
                print_pokemon(pokemon)
        if(noneCounter == len(filteredList)):
            print("There are no Pokemons in this Pokedex that match the criteria.")
    print("")


########################
# 8) Sub-menu & Main menu
########################
def is_pokemon_in_pokedex(pokedex, id):
    for pokemon in pokedex:
        if(pokemon["ID"] == id):
            return True
        
    return False

def existing_pokedex():
    """
    Ask user for an owner name, locate the BST node, then show sub-menu:
    - Add Pokemon
    - Display (Filter)
    - Release
    - Evolve
    - Back
    """
    global ownerRoot
    nameChoice = input("Owner name: ")
    owner_node = find_owner_bst(ownerRoot, nameChoice)
    if(owner_node == None):
        print(f"Owner '{nameChoice}' not found.")
        return
    choice = 0
    realName = owner_node["owner"]
    while(choice != 5):
        print(f"\n-- {realName}'s Pokedex Menu --\n"
            "1. Add Pokemon\n",
            "2. Display Pokedex\n",
            "3. Release Pokemon\n",
            "4. Evolve Pokemon\n",
            "5. Back to Main", sep="")
        choice = read_int_safe("Your choice: ")
        if(choice == 1):
            add_pokemon_to_owner(owner_node)
        elif(choice == 2):
          display_filter_sub_menu(owner_node["pokedex"])
        elif(choice == 3):
            release_pokemon_by_name(owner_node)
        elif(choice == 4):
            evolve_pokemon_by_name(owner_node)
        elif(choice == 5):
            print("Back to Main Menu.")
            break
    print("")

def create_new_owner():
    global ownerRoot
    name = input("Owner name: ")
    if(find_owner_bst(ownerRoot, name) != None):
        print(f"Owner {name} already exists. No new pokedex created.")
        return
    print("Choose your starter Pokemon:")
    starter_pokemons = ["Treecko", "Torchic", "Mudkip"]
    for i, pokemon_name in enumerate(["Treecko", "Torchic", "Mudkip"]):
        print(f"{(i+1)}) {pokemon_name}")
    
    choice = read_int_safe("Your choice: ")
    if(choice > 3 or choice < 1):
        print("Invalid. No new Pokedex created.")
        return
    pokemon_name = starter_pokemons[choice-1]
    pokedex = [get_poke_dict_by_name(pokemon_name)]

    print(f"New Pokedex created for {name} with starter {pokemon_name}.")
    print("")
    return create_owner_node(name, pokedex)

def main_menu():
    """
    Main menu for:
    1) New Pokedex
    2) Existing Pokedex
    3) Delete a Pokedex
    4) Sort owners
    5) Print all
    6) Exit
    """
    global ownerRoot
    while True:
        print(
            "=== Main Menu ===\n",
            "1. New Pokedex\n",
            "2. Existing Pokedex\n",
            "3. Delete a Pokedex\n",
            "4. Display owners by number of Pokemon\n",
            "5. Print All\n",
            "6. Exit"
            ,sep="")
        option = read_int_safe("Your choice: ")
        if(option == 1):
            owner = create_new_owner()
            if(owner != None):
                ownerRoot = insert_owner_bst(ownerRoot, owner)
        elif(option == 2):
            existing_pokedex()
        elif(option == 3):
            prompt_owner_deletion()
        elif(option == 4):
            sort_owners_by_num_pokemon()
        elif(option == 5):
            print_all_owners()
        elif(option == 6):
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

def main():
    main_menu()
if __name__ == "__main__":
    main()
