def check_hp(target, heal, mp_heal):
    if target.hp <= 0:
        print(f"{target.name} has perished in battle. They can't be healed.")
        return

    target.hp = min(target.maxhp, target.hp + heal)
    target.mp = min(target.maxmp, target.mp + mp_heal)

class Items:
    def __init__(self, name, effect, quantity, description):
        self.name = name
        self.effect = effect
        self.description = description
        self.quantity = quantity

    def use_item(self, target):
        # Apply the effect of the item on the target
        if self.effect == "heal":
            self.apply_healing(target)
        elif self.effect == "buff":
            self.apply_buff(target)
        elif self.effect == "debuff":
            self.apply_debuff(target)
        else:
            print("Item effect is not recognized.")

    def apply_healing(self, target):
        match self.name:
            case "Healing Potion":
                check_hp(target, heal=100, mp_heal=0)
                self.decrease_quantity(1)

            case "HI-Potion":
                check_hp(target, heal=250, mp_heal=0)
                self.decrease_quantity(1)

            case "Ether":
                check_hp(target, heal=0, mp_heal=50)
                self.decrease_quantity(1)

            case "HI-Ether":
                check_hp(target, heal=0, mp_heal=100)
                self.decrease_quantity(1)

            case "Elixir":
                check_hp(target, heal=200, mp_heal=50)
                self.decrease_quantity(1)

            case "HI-Elixir":
                target.hp = target.maxhp
                target.mp = target.maxmp
                self.decrease_quantity(1)

            case "Phoenix Down":
                if target.hp > 0:
                    print(f"{target.name} isn't dead.")
                else:
                    target.hp = target.maxhp * 0.1
                    print(f"{target.name} is back on their feet.")
                    self.decrease_quantity(1)

            case _:
                print("Unrecognized healing item.")

    def apply_buff(self, target):
        match self.name:
            case "Hermes Shoes":
                target.speed += 10
                self.decrease_quantity(1)

            case "Red Fang":
                target.atk += 10
                self.decrease_quantity(1)

            case "Protect Coat":
                target.df += 10
                self.decrease_quantity(1)

            case "Faerie Bless":
                target.mgk_atk += 10
                self.decrease_quantity(1)

            case "Witch's Hat":
                target.mgk_def += 10
                self.decrease_quantity(1)

            case _:
                print("Unrecognized buff item.")

    def apply_debuff(self, target):
        match self.name:
            case "Slug Bomb":
                target.atk -= 10
                self.decrease_quantity(1)

            case "Acid":
                target.df -= 10
                self.decrease_quantity(1)

            case "Spider Silk":
                target.speed -= 10
                self.decrease_quantity(1)

            case "Moonstone":
                target.mgk_atk -= 10
                self.decrease_quantity(1)

            case "Dragon Spit":
                target.mgk_def -= 10
                self.decrease_quantity(1)

            case _:
                print("Unrecognized debuff item.")

    def increase_quantity(self, amount):
        self.quantity += amount

    def decrease_quantity(self, amount):
        self.quantity = max(0, self.quantity - amount)

    def __str__(self):
        return f"    {self.name} : {self.description}: x{self.quantity}"

