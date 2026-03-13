import random


#The menu function runs continuously until the user loses enough crystals or gains enough to win the game.
#It controls when the game and rules functions are run, handles replays, and counts rounds/crystals as well.
def menu(crystal_count):

    # Track how many completed game rounds the player has gone through.
    round_count = 0
    print(f"Current Crystal Count: {crystal_count}")

    while True:
        #Checks for win/lose conditions
        if crystal_count <= 5:
            print(f"You lost all your crystals in {round_count} rounds! You are now alien food.")
            return
        elif crystal_count >= 300:
            print(f"You reached 300 crystals in {round_count} rounds! Time to escape!")
            return
        
        
        # Show the available activities before asking the user what to do next.
        print("\nOptions:\n")
        print("1: Asteroid Mining\n2: Alien Duel\n3: Rules\n")
        selection = input("Please make selection: ")
        selection = check_selection(selection, "menu")

        # Send the player to the selected game or display the rules menu.
        match selection:
            case "asteroid mining":
                crystal_count = mining(crystal_count)
            case "alien duel":
                crystal_count = blackjack(crystal_count)
            case "rules":
                rules()
                continue

        round_count = round_count + 1

        while True:
            # Stop asking for a replay if the game has already been won or lost.
            if crystal_count <= 5 or crystal_count >= 300: break
            print(f"Current Crystal Count: {crystal_count}")
            replay = input("Enter yes to replay this game, or no to choose a new one: ")
            replay = check_selection(replay, "replay")

            # Replay the same game immediately, or return to the main menu.
            match replay:
                case "yes":
                    match selection:
                        case "asteroid mining":
                            crystal_count = mining(crystal_count)
                            round_count = round_count + 1
                        case "alien duel":
                            crystal_count = blackjack(crystal_count)
                            round_count = round_count + 1
                case "no":
                    break

#The blackjack function runs alien duel, which is a computerized, blackjack inspired game.
def blackjack(crystal_count):
    # Deduct the entry fee before the player places a bet for the round.
    crystal_count = crystal_count - 5
    bet = input("Place bet here: ")
    bet = check_bet(bet, crystal_count)

    # Start both scores at zero before the opening rolls.
    user_score = 0
    computer_score = 0

    # Give the player the first two rolls automatically, similar to an opening hand.
    for i in range(2):
        roll, user_score = roll_die(user_score)
        print(f"You rolled {roll}")

    while True:
        # Let the player keep rolling until they stand or the round ends immediately.
        print(f"\nYour score is {user_score}.")
        hit_stand = input("To hit, enter hit. To stand, enter stand: ")
        hit_stand = check_selection(hit_stand, "blackjack")

        match hit_stand:
            case "hit":
                roll, user_score = roll_die(user_score)
                print(f"\nYou rolled {roll}. Your score is now {user_score}.")

                # Resolve the round immediately if the player busts or hits 21 exactly.
                if user_score > 21:
                    crystal_count = crystal_count - bet
                    print(f"Bust! You lost this round.")
                    return crystal_count
                
                elif user_score == 21:
                    crystal_count = crystal_count + bet + 5
                    print("Plasma blast! You win this round.")
                    return crystal_count
            case "stand":
                break
    
    # Once the player stands, the computer rolls until it reaches the stand threshold.
    while computer_score < 17:
        roll, computer_score = roll_die(computer_score)
        print(f"The computer rolled {roll}. It's score is now {computer_score}.")

        # End the round immediately if the computer busts or lands on 21.
        if computer_score > 21:
            crystal_count = crystal_count + bet + 5
            print("The computer busted! You win this round.")
            return crystal_count
        
        elif computer_score == 21:
            crystal_count = crystal_count - bet
            print("The computer got a plasma blast! You lose this round.")
            return crystal_count
    
    # Compare final scores only if neither side won automatically earlier.
    print(f"Your score: {user_score}\nComputer Score: {computer_score}")

    if user_score > computer_score:
        print("You win this round!")
        crystal_count = crystal_count + bet + 5
        return crystal_count
    else:
        crystal_count = crystal_count - bet
        print("You lose this round!")
        return crystal_count

#Mining allows the user to open 1 of 5 boxes, chosen randomly, and receive or lose coins based on the effects of the box.
def mining(crystal_count):
    # Prevent the player from entering the game without the minimum crystal amount.
    if crystal_count < 10:
        print("You do not have enough crystals to play this game!")
        return crystal_count
    
    # Randomly choose which hidden box outcome the player receives.
    box = random.randint(1,5)

    match box:
        case 1:
            crystal_count = crystal_count + 50
            print("You gained 50 crystals!")
        case 2:
            # Box 2 has a second random outcome that can help or hurt the player.
            give_or_take = random.randint(1,2)

            if give_or_take == 1:
                crystal_count = crystal_count + 100
                print("You gained 100 crystals!")
            else:
                crystal_count = crystal_count - 100
                print("You lost 100 crystals.")
        case 3:
            crystal_count = crystal_count - 25
            print("You lost 25 crystals.")
        case 4:
            crystal_count = 0
            print("You lost all your crystals!")
        case 5:
            print("Nothing happened.")

    return crystal_count

#Strips, converts to lowercase, and verifies string selection inputs for various phases of the program. Constantly reprompts until the string is valid.
def check_selection(selection, phase):
    # Normalize the first user entry before validation begins.
    selection = selection.strip()
    selection = selection.lower()

    while True:
        # Re-normalize after every reprompt so extra spaces or capitals do not matter.
        selection = selection.strip()
        selection = selection.lower()

        match phase:
            case "menu":
                if selection in ["asteroid mining", "alien duel", "rules"]:
                    return selection
                else:
                    selection = input("Please enter a valid selection: ")
            case "blackjack":
                if selection in ["hit", "stand"]:
                    return selection
                else:
                    selection = input("Please enter a valid selection: ")
            case "replay":
                if selection in ["yes", "no"]:
                    return selection
                else:
                    selection = input("Please enter a valid selection: ")

#Converts bet to int, checks bet against crystal count, checks for negative/0 bets, and outputs bet. If bet can't be converted to int, or bet is otherwise invalid, program reprompts.
def check_bet(bet, crystal_count):
    while True:
        # Keep asking until the user enters a whole-number bet.
        try:
            bet = int(bet)
        except ValueError:
            bet = input("Please enter a valid bet: ")
            continue

        # Accept only positive bets that the player can actually afford.
        if bet > 0 and bet <= crystal_count:
            return bet

        bet = input("Please enter a valid bet: ")

#Simulates roll of a die. If 0 is hit, 10 points added to score. If 1 is hit, either 1 or 11 points added to score, depending on if score is 10 or greater.
def roll_die(score):
    # Roll a single digit to act as the game's custom die.
    roll = random.randint(0,9)

    match roll:
        case 0:
            score = score + 10
            return roll, score
        case 1:
            # Treat a 1 like an ace when it would not immediately cause a bust.
            if score <= 10:
                score = score + 11
                return roll, score
            
    # All other values add their face value to the current score.
    score = score + roll
    return roll, score
        
#Prints rules for each game
def rules():
            # Display the instructions for both mini-games in one place.
            print("Alien duel rules: ")
            print("You and the computer take turns rolling dice (0-9), trying to get as close to 21 as possible.")
            print("Hitting 21 exactly is a plasma blast, which is an automatic win for the player or computer.")
            print("Going over 21 causes a bust, which is an automatic loss for the player or computer.")
            print("If both the player and the computer stand under 21, their scores will be compared.")
            print("If you have a higher score. you win. Otherwise, the computer wins.")

            print("Asteroid Mining Rules:")
            print("In this game, the player randomly opens 1 out of 5 boxes.")
            print("The effect of opening each box is listed below:")
            print("1: Gain 50 Crystals\n2: Gain or lose 100 crystals\n3: Lose 25 crystals\n4: Lose all crystals\n5: Nothing.")



