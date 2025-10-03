from src.locations import loc_A,loc_B



#Rules for your Task2
feedingRules = {
    # Single percept sequences - first encounter
    (loc_A, 'Empty'): 'MoveRight',
    (loc_B, 'Empty'): 'MoveLeft', 
    (loc_A, 'MilkHere'): 'Drink',
    (loc_B, 'MilkHere'): 'Drink',
    (loc_A, 'SausageHere'): 'Eat',
    (loc_B, 'SausageHere'): 'Eat',

}
