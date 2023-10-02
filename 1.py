import re
import random

class CoffeeMachine():
    """Coffee machine"""
    def __init__(self): 
        self.__state = 'ON'
        self.menu = {
            'espresso': {
                'ingredients': {
                    'coffee': 19,
                    'water': 35,
                },
                'price': 1.99,
            },
            'latte': {
                'ingredients': {
                    'coffee': 24,
                    'water': 50,
                    'milk': 150,
                },
                'price': 2.39,
            },
            'cappuccino': {
                'ingredients':{
                    'coffee': 24,
                    'water': 60,
                    'milk': 50,
                },
                'price': 3.19,
            }
        }

        self.inventory = {
            'coffee': 100,
            'water': 300,
            'milk': 300,
            'money': 0,
        }

    def turn_on(self):
        """turn_on"""
        self.__state = 'ON'
        print('Hello there. I have something here.')
        self.request_coffee()

    def turn_off(self):
        """turn_off"""
        self.__state = 'off'
        print('Bye! Whoop-whoop-whoop.')

    def request_coffee(self):
        """Coffee choice"""
        print(self.report())
        inp = input('What would you like? (espresso/latte/cappuccino):').lower()
        self.handle_input(inp) # decorator

        if inp in ('espresso','latte','cappuccino'):
            self.check_resources(inp)
        else:
            print('wrong input (coffee type).', end='\n\n')
            self.request_coffee()

    # TODO: decorator
    def handle_input(self, inp):
        """make me a decorator!"""
        if inp.lower() == 'off':
            self.turn_off()

    def report(self):
        """Show the current status of the machine"""
        return f'\
            \nWater: {self.inventory["water"]}ml\
            \nMilk: {self.inventory["milk"]}ml\
            \nCoffee: {self.inventory["coffee"]}g\
            \nMoney: ${self.inventory["money"]}\
            \n'

    def check_resource(self, cost: int, ingredient: str) -> bool:
        """True if amount of a resource is enough"""
        amount = self.inventory[ingredient]
        if cost > amount:
            print(f"Nope. Not enough {ingredient}.", end='\n\n')
            return False

        return True

    def transaction(self, coffee_type: str):
        """Proceed a pay"""    
        total = 0
        coins_types = ["quarter", "dime", "nickel", "pennie"]
        coins_values = [0.25, 0.1, 0.05, 0.01]
        coffee_cost = self.menu[coffee_type]["price"]

        inp = input('Insert coins pls (quarter, dimes, nickel, pennies). \n[!] Say "ok" loudly when done.\n').lower()
        self.handle_input(inp) # decorator

        while inp != "ok":
            if self.get_state() != 'ON':
                break
            success = False
            phrases = ['Good.', 'Ok.', 'Aha, hm.', 'So.', 'Took it to account.', 'Ya.']
            for i, coin_type in enumerate(coins_types):
                if inp.find(coin_type) != -1:
                    total += (float(re.search(r'\d+', inp).group()) * coins_values[i])
                    total = round(total, 2)
                    endline = 'Maybe enough?'  if (total > coffee_cost) else random.choice(phrases)
                    print(f'inserted: ${total}.  {endline}')
                    success = True
                    break

            if not success:
                print(f"Nope. {re.search(r'[a-zA-Z]+', inp).group()} isn't a coin. I can eat coins only. Try better.")
            inp = input().lower()
            self.handle_input(inp) # decorator

        if total >= coffee_cost:
            if self.take_resources(coffee_type):
                self.inventory["money"] += coffee_cost
                change = round(total - coffee_cost, 2)
                if change >= 0:
                    print()
                    if change > 0:
                        print(f'Your change, meat bag. ${change}. Ding-ding-ding.')
                    print('=== processing... === ')
                    print(f'Your {coffee_type}.', end='\n\n')
                    print(self.request_coffee())
            else:
                print('You are late. Some ingredients are gone. Sry.')
                self.request_coffee()
        else:
            if self.get_state() == 'ON':
                print("A u kiddin' me? Not enough money. Money refunded.", end='\n\n')
                self.request_coffee()
            elif total > 0:
                print("Ok, scam. Don't forget your coins. Beep. Money refunded.")

    def check_resources(self, coffee_type: str):
        """check_resources"""
        costs = self.menu[coffee_type]["ingredients"]

        for ingredient in costs:
            if not self.check_resource(costs[ingredient], ingredient):
                self.request_coffee()
                break

        self.transaction(coffee_type)

    def take_resources(self, coffee_type: str) -> bool:
        """take_resources"""
        updated_inv = self.inventory
        costs = self.menu[coffee_type]["ingredients"]

        for ingredient in costs:
            if self.check_resource(costs[ingredient], ingredient):
                updated_inv[ingredient] -= costs[ingredient]
            else:
                return False

        self.inventory = updated_inv
        return True

    def get_state(self) -> bool:
        """getter"""
        return self.__state


c_machine_1 = CoffeeMachine()
c_machine_1.turn_on()
